#!/usr/bin/env python3
# Copyright 2024 Marc-Antoine Ruel. All rights reserved.
# Use of this source code is governed under the Apache License, Version 2.0
# that can be found in the LICENSE file.

"""Runs a display effect locally for faster iteration."""

import argparse
import os
import subprocess
import sys

import yaml

def generate_effect(esphome, name, code):
  with open("run.cc", "wt") as f:
    f.write("#include <stdio.h>\n")
    f.write('#include "esphome/components/light/addressable_light.h"\n')
    f.write("using namespace esphome;\n")
    f.write("using namespace esphome::light;\n")
    f.write("void update(AddressableLight &it) {\n")
    f.write(code)
    f.write("}\n")
    f.write("int main() {\n")
    f.write("  return 0;\n")
    f.write("}\n")
  # We need to inject a little bit of code.
  files = [
      "run.cc",
      os.path.join(esphome, "esphome/components/light/esp_range_view.cpp"),
      os.path.join(esphome, "esphome/core/color.cpp"),
  ]
  subprocess.check_call([
    "g++",
    "-I.",
    "-I" + esphome,
    ] + files)
  print("Run ./a.out")

def parse_light(esphome, item):
  if "effects" not in item:
    return
  for e in item["effects"]:
    for t, data in e.items():
      if t != "addressable_lambda":
        continue
      generate_effect(esphome, data["name"], data["lambda"])

def main():
  parser = argparse.ArgumentParser(description=sys.modules[__name__].__doc__)
  parser.add_argument(
      "file", type=argparse.FileType("r"), help="esphome yaml file to parse")
  parser.add_argument(
      "--esphome", required=True,
      metavar="path/to/esphome.git",
      help="Path to esphome source code")
  args = parser.parse_args()
  if not os.path.isfile(os.path.join(args.esphome, "esphome", "core", "color.cpp")):
    print("--esphome must point to a checkout of https://github.com/esphome/esphome", file=sys.stderr)
    return 1
  # Use BaseLoader to not have to resolve !include.
  data = yaml.load(args.file, Loader=yaml.BaseLoader)
  for item in data.get("display", []):
    parse_light(args.esphome, item)
  for item in data.get("light", []):
    parse_light(args.esphome, item)
  return 0

if __name__ == "__main__":
  sys.exit(main())
