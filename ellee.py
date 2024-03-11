#!/usr/bin/env python3
# Copyright 2024 Marc-Antoine Ruel. All rights reserved.
# Use of this source code is governed under the Apache License, Version 2.0
# that can be found in the LICENSE file.

"""Runs a display effect locally for faster iteration."""

import argparse
import os
import shutil
import subprocess
import sys
import textwrap
import threading

import yaml

HEADER = r"""// Generated by ellee.py

#include "esphome/components/light/addressable_light_effect.h"

using namespace esphome;

"""

PREAMBLE = """
void update(esphome::light::AddressableLight &it, bool initial_run) {
  using namespace esphome::light;
  // Beginning of lambda.
"""

FOOTER = r"""
  // End of lambda.
}

// Support code.

class ElleeLight : public esphome::light::AddressableLight {
  public:
    ElleeLight() {
      correction_.calculate_gamma_table(1);
    }
    virtual esphome::light::LightTraits get_traits() {
      auto traits = esphome::light::LightTraits();
      traits.set_supported_color_modes({esphome::light::ColorMode::RGB});
      return traits;
    }
    virtual int32_t size() const {
      return NUMLIGHTS;
    }
    virtual void clear_effect_data() {
      memset(effect_data_, 0, sizeof(effect_data_));
    }
    virtual esphome::light::ESPColorView get_view_internal(int32_t index) const {
      return esphome::light::ESPColorView(
          &pixels_[3*index], &pixels_[3*index+1], &pixels_[3*index+2],
          nullptr, (uint8_t*)&effect_data_, &correction_);
    }
    virtual void write_state(esphome::light::LightState *state) {
      if (AS_HEX) {
        write_hex();
      } else {
        write_ansi();
      }
      fflush(stdout);
    }
    void write_ansi() {
      printf("\r");
      printf("\x1b[0m");
      if (SHOW_MILLIS) {
        printf("%- 11d ", millis());
      }
      for (int i = 0; i < size(); i++) {
        printf("\x1b[38;2;%d;%d;%dm\u2588", pixels_[3*i], pixels_[3*i+1], pixels_[3*i+2]);
      }
      printf("\x1b[0m ");
      if (ONE_PER_LINE) {
        printf("\n");
      }
    }
    void write_hex() {
      printf("\r");
      if (SHOW_MILLIS) {
        printf("%- 11d ", millis());
      }
      for (int i = 0; i < size(); i++) {
        printf("%02x%02x%02x", pixels_[3*i], pixels_[3*i+1], pixels_[3*i+2]);
        if (i != size()-1) {
          printf(" ");
        }
      }
      if (ONE_PER_LINE) {
        printf("\n");
      }
    }

    mutable uint8_t pixels_[3*NUMLIGHTS];
    mutable uint8_t effect_data_[NUMLIGHTS];
};

ElleeLight it;
bool g_initial_run = true;

void setup() {
}

void loop() {
  update(it, g_initial_run);
  g_initial_run = false;
  it.write_state(nullptr);
  if (ONCE) {
    printf("\n");
    fflush(stdout);
    exit(0);
  }
  esphome::delay(INTERVAL);
}
"""

def escape(r):
  return r.replace("\\", "\\\\").replace("\"", "\\\"")

class Thread(threading.Thread):
  def __init__(self, **kwargs):
    self.returned = None
    oldtarget = kwargs.pop("target")
    def hook(*args, **kwargs):
      self.returned = oldtarget(*args, **kwargs)
    super().__init__(target=hook, **kwargs)

def generate_effect(
    esphome, outdir,
    min_interval, one_per_line, as_hex, show_millis, once,
    componentname, numlights, effectname, interval, code):
  exe = os.path.join(outdir, effectname.translate(str.maketrans({x: "_" for x in " []{}\\/^$*?"})))
  print("Compiling effect \"%s/%s\" to %s " % (componentname, effectname, exe))
  if not interval:
    interval = 50
  elif interval.endswith("ms"):
    interval = int(interval[:-2])
  elif interval.endswith("s"):
    interval = int(interval[:-1]) * 1000
  else:
    print(f"Unknown interval {interval}", file=sys.stderr)
    return False
  interval = max(min_interval, interval)
  injected = (
      f"// Configuration\n" +
      f"const bool AS_HEX = {str(as_hex).lower()};\n" +
      f"const int INTERVAL = {interval};\n"
      f"const int NUMLIGHTS = {int(numlights)};\n"
      f"const bool ONCE = {str(once).lower()};\n" +
      f"const bool ONE_PER_LINE = {str(one_per_line).lower()};\n" +
      f"const bool SHOW_MILLIS = {str(show_millis).lower()};\n")
  if once:
    injected += "#define millis() 42\n"
  with open(exe+".cc", "wt") as f:
    f.write(HEADER)
    f.write(injected)
    f.write(PREAMBLE)
    f.write(textwrap.indent(code.rstrip(), "  "))
    f.write(FOOTER)
  # We need to inject a little bit of code.
  files = [
      exe+".cc",
      os.path.join(esphome, "esphome/components/host/core.cpp"),
      os.path.join(esphome, "esphome/components/host/preferences.cpp"),
      os.path.join(esphome, "esphome/components/light/addressable_light.cpp"),
      os.path.join(esphome, "esphome/components/light/esp_color_correction.cpp"),
      os.path.join(esphome, "esphome/components/light/esp_hsv_color.cpp"),
      os.path.join(esphome, "esphome/components/light/esp_range_view.cpp"),
      os.path.join(esphome, "esphome/components/light/light_call.cpp"),
      os.path.join(esphome, "esphome/components/light/light_output.cpp"),
      os.path.join(esphome, "esphome/components/light/light_state.cpp"),
      os.path.join(esphome, "esphome/core/application.cpp"),
      os.path.join(esphome, "esphome/core/color.cpp"),
      os.path.join(esphome, "esphome/core/component.cpp"),
      os.path.join(esphome, "esphome/core/entity_base.cpp"),
      os.path.join(esphome, "esphome/core/helpers.cpp"),
      os.path.join(esphome, "esphome/core/scheduler.cpp"),
  ]
  try:
    subprocess.check_call(["g++", "-ggdb", "-o", exe, "-DUSE_HOST", "-I.", "-I" + esphome] + files)
  except subprocess.CalledProcessError as e:
    print("Compilation failed:", e, file=sys.stderr)
    return False
  print(f"Run \"{exe}\" or \"gdb {exe}\" to diagnose a crash")
  return True

def parse_light(esphome, outdir, min_interval, one_per_line, as_hex,
                show_millis, once, filename, component):
  if "effects" not in component:
    return True
  threads = []
  for effectentry in component["effects"]:
    for effecttype, effectdata in effectentry.items():
      if effecttype != "addressable_lambda":
        continue
      componentname = component.get("name") or os.path.basename(filename).rsplit(".", 2)[0]
      effeectname = effectdata.get("name") or componentname
      t = Thread(
          target=generate_effect,
          args=(
              esphome, outdir,
              min_interval, one_per_line, as_hex, show_millis, once,
              componentname, component.get("num_leds", 70),
              effeectname,
              effectdata.get("update_interval", "100ms"),
              effectdata["lambda"]))
      t.start()
      threads.append(t)
  for t in threads:
    t.join()
  return min(t.returned for t in threads) if threads else True

def main():
  # TODO(maruel): Make it nice for Windows and macOS users.
  if not shutil.which("g++"):
    print("Install g++ first", file=sys.stderr)
    return 1
  parser = argparse.ArgumentParser(description=sys.modules[__name__].__doc__)
  parser.add_argument(
      "file", type=argparse.FileType("r"), help="esphome yaml file to parse")
  parser.add_argument(
      "--esphome", required=True,
      metavar="path/to/esphome.git",
      help="Path to esphome source code")
  parser.add_argument(
      "--outdir", default=".", metavar=".",
      help="Directory to store generated source and executabe")
  parser.add_argument(
      "--interval", type=int, default=0, help="Minimal interval in ms to use")
  parser.add_argument(
      "--show-millis", action="store_true",
      help="Display time in millis before the colors")
  parser.add_argument(
      "--as-hex", action="store_true",
      help="Display hex values instead of using ANSI colors")
  parser.add_argument(
      "--one-per-line", action="store_true",
      help="Draw each update on a new line")
  parser.add_argument(
      "--once", action="store_true",
      help="Draw one update then exit")
  args = parser.parse_args()
  if not os.path.isfile(os.path.join(args.esphome, "esphome", "core", "color.cpp")):
    print("--esphome must point to a checkout of https://github.com/esphome/esphome", file=sys.stderr)
    return 1
  # Use BaseLoader to not have to resolve !include.
  data = yaml.load(args.file, Loader=yaml.BaseLoader)
  threads = []
  for item in data.get("light", []):
    t = Thread(
        target=parse_light,
        args=(args.esphome, args.outdir, args.interval, args.one_per_line,
              args.as_hex, args.show_millis, args.once, args.file.name, item))
    t.start()
    threads.append(t)
  for t in threads:
    t.join()
  return int(not (min(t.returned for t in threads) if threads else True))

if __name__ == "__main__":
  sys.exit(main())
