#!/usr/bin/env python3
# Copyright 2024 Marc-Antoine Ruel. All rights reserved.
# Use of this source code is governed under the Apache License, Version 2.0
# that can be found in the LICENSE file.

import glob
import os
import shutil
import subprocess
import sys
import tempfile

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(THIS_DIR)

EXPECTATIONS = {
    "printf_then_exit.yaml": {
      "unnamed": b'127\n',
    },
    "sin.yaml": {
      "half_sin8": b'\r000000 020202 060606 080808 0c0c0c 0e0e0e 121212 141414 181818 1a1a1a 1e1e1e 202020 242424 262626 2a2a2a 2c2c2c 303030 343434 363636 3a3a3a 3c3c3c 404040 424242 464646 484848 4c4c4c 4e4e4e 525252 545454 585858 5a5a5a 5e5e5e 606060 646464 666666 6a6a6a 6c6c6c 6e6e6e 727272 747474 767676 7a7a7a 7c7c7c 808080 828282 848484 888888 8a8a8a 8e8e8e 909090 929292 949494 969696 9a9a9a 9c9c9c 9e9e9e a0a0a0 a2a2a2 a4a4a4 a8a8a8 aaaaaa acacac aeaeae b0b0b0 b4b4b4 b6b6b6 b8b8b8 bababa bcbcbc bebebe c0c0c0 c2c2c2 c4c4c4 c6c6c6 c8c8c8 cacaca cccccc cecece d0d0d0 d2d2d2 d4d4d4 d6d6d6 d6d6d6 d8d8d8 dadada dcdcdc dcdcdc dedede e0e0e0 e0e0e0 e2e2e2 e4e4e4 e6e6e6 e6e6e6 e8e8e8 eaeaea ececec ececec eeeeee eeeeee f0f0f0 f0f0f0 f0f0f0 f2f2f2 f2f2f2 f4f4f4 f4f4f4 f6f6f6 f6f6f6 f6f6f6 f8f8f8 f8f8f8 fafafa fafafa fafafa fafafa fcfcfc fcfcfc fcfcfc fcfcfc fcfcfc fcfcfc fcfcfc fcfcfc fefefe fefefe fefefe fefefe fefefe fefefe fefefe fefefe fefefe fcfcfc fcfcfc fcfcfc fcfcfc fcfcfc fcfcfc fcfcfc fcfcfc fafafa fafafa fafafa fafafa f8f8f8 f8f8f8 f6f6f6 f6f6f6 f6f6f6 f4f4f4 f4f4f4 f2f2f2 f2f2f2 f0f0f0 f0f0f0 eeeeee eeeeee eeeeee ececec eaeaea eaeaea e8e8e8 e6e6e6 e4e4e4 e4e4e4 e2e2e2 e0e0e0 e0e0e0 dedede dcdcdc dadada dadada d8d8d8 d6d6d6 d6d6d6 d2d2d2 d0d0d0 cecece cccccc cccccc cacaca c8c8c8 c6c6c6 c4c4c4 c2c2c2 c0c0c0 bebebe bcbcbc bababa b8b8b8 b6b6b6 b2b2b2 b0b0b0 aeaeae acacac aaaaaa a8a8a8 a4a4a4 a2a2a2 a0a0a0 9e9e9e 9c9c9c 989898 969696 949494 929292 909090 8c8c8c 8a8a8a 888888 848484 828282 7e7e7e 7c7c7c 7a7a7a 767676 747474 727272 6e6e6e 6c6c6c 686868 666666 646464 606060 5e5e5e 5a5a5a 585858 545454 525252 4e4e4e 4c4c4c 484848 464646 424242 404040 3c3c3c 3a3a3a 363636 343434 303030 2c2c2c 2a2a2a 262626 242424 202020 1e1e1e 1a1a1a 181818 141414 101010 0e0e0e 0a0a0a 080808 040404 020202\n',
      "sin16_c": b'\r000000 020202 050505 080808 0b0b0b 0e0e0e 111111 151515 181818 1b1b1b 1e1e1e 212121 242424 272727 2a2a2a 2d2d2d 303030 343434 373737 3a3a3a 3d3d3d 404040 434343 464646 494949 4c4c4c 4f4f4f 525252 555555 585858 5b5b5b 5e5e5e 616161 646464 676767 696969 6c6c6c 6f6f6f 727272 747474 777777 7a7a7a 7d7d7d 7f7f7f 828282 858585 888888 8a8a8a 8d8d8d 909090 929292 959595 979797 999999 9c9c9c 9e9e9e a0a0a0 a3a3a3 a5a5a5 a8a8a8 aaaaaa acacac afafaf b1b1b1 b3b3b3 b6b6b6 b8b8b8 bababa bcbcbc bebebe c0c0c0 c2c2c2 c4c4c4 c6c6c6 c8c8c8 cacaca cccccc cdcdcd cfcfcf d1d1d1 d3d3d3 d6d6d6 d7d7d7 d8d8d8 dadada dbdbdb dddddd dedede e0e0e0 e1e1e1 e3e3e3 e4e4e4 e5e5e5 e7e7e7 e8e8e8 eaeaea ebebeb ededed eeeeee efefef efefef f0f0f0 f1f1f1 f2f2f2 f3f3f3 f4f4f4 f5f5f5 f6f6f6 f6f6f6 f7f7f7 f8f8f8 f9f9f9 fafafa fbfbfb fbfbfb fbfbfb fcfcfc fcfcfc fcfcfc fcfcfc fdfdfd fdfdfd fdfdfd fdfdfd fefefe fefefe fefefe fefefe ffffff fefefe fefefe fefefe fefefe fdfdfd fdfdfd fdfdfd fdfdfd fcfcfc fcfcfc fcfcfc fcfcfc fbfbfb fbfbfb fbfbfb fbfbfb f9f9f9 f8f8f8 f7f7f7 f7f7f7 f6f6f6 f5f5f5 f4f4f4 f3f3f3 f2f2f2 f1f1f1 f0f0f0 f0f0f0 efefef eeeeee ededed ececec eaeaea e8e8e8 e7e7e7 e6e6e6 e4e4e4 e3e3e3 e1e1e1 e0e0e0 dedede dddddd dcdcdc dadada d9d9d9 d7d7d7 d6d6d6 d4d4d4 d2d2d2 d0d0d0 cecece cccccc cacaca c8c8c8 c6c6c6 c4c4c4 c2c2c2 c0c0c0 bebebe bcbcbc bababa b8b8b8 b6b6b6 b5b5b5 b1b1b1 afafaf adadad aaaaaa a8a8a8 a5a5a5 a3a3a3 a1a1a1 9e9e9e 9c9c9c 9a9a9a 979797 959595 929292 909090 8e8e8e 8b8b8b 888888 858585 828282 808080 7d7d7d 7a7a7a 777777 757575 727272 6f6f6f 6c6c6c 6a6a6a 676767 646464 616161 5e5e5e 5b5b5b 585858 555555 525252 4f4f4f 4c4c4c 494949 464646 434343 404040 3d3d3d 3a3a3a 373737 343434 313131 2d2d2d 2a2a2a 272727 242424 212121 1e1e1e 1b1b1b 181818 151515 121212 0f0f0f 0c0c0c 090909 060606 030303\n',
      "sinf": b'\r000000 030303 060606 090909 0c0c0c 0f0f0f 121212 151515 181818 1c1c1c 1f1f1f 222222 252525 282828 2b2b2b 2e2e2e 313131 343434 373737 3a3a3a 3d3d3d 404040 444444 474747 4a4a4a 4d4d4d 4f4f4f 525252 555555 585858 5b5b5b 5e5e5e 616161 646464 676767 6a6a6a 6d6d6d 6f6f6f 727272 757575 787878 7a7a7a 7d7d7d 808080 838383 858585 888888 8b8b8b 8d8d8d 909090 929292 959595 979797 9a9a9a 9c9c9c 9f9f9f a1a1a1 a4a4a4 a6a6a6 a8a8a8 ababab adadad afafaf b2b2b2 b4b4b4 b6b6b6 b8b8b8 bababa bcbcbc bfbfbf c1c1c1 c3c3c3 c5c5c5 c7c7c7 c9c9c9 cacaca cccccc cecece d0d0d0 d2d2d2 d4d4d4 d5d5d5 d7d7d7 d9d9d9 dadada dcdcdc dddddd dfdfdf e0e0e0 e2e2e2 e3e3e3 e5e5e5 e6e6e6 e7e7e7 e9e9e9 eaeaea ebebeb ececec ededed efefef f0f0f0 f1f1f1 f2f2f2 f3f3f3 f4f4f4 f4f4f4 f5f5f5 f6f6f6 f7f7f7 f8f8f8 f8f8f8 f9f9f9 fafafa fafafa fbfbfb fbfbfb fcfcfc fcfcfc fdfdfd fdfdfd fdfdfd fefefe fefefe fefefe fefefe fefefe fefefe fefefe ffffff fefefe fefefe fefefe fefefe fefefe fefefe fefefe fdfdfd fdfdfd fdfdfd fcfcfc fcfcfc fbfbfb fbfbfb fafafa fafafa f9f9f9 f8f8f8 f8f8f8 f7f7f7 f6f6f6 f5f5f5 f4f4f4 f4f4f4 f3f3f3 f2f2f2 f1f1f1 f0f0f0 efefef ededed ececec ebebeb eaeaea e9e9e9 e7e7e7 e6e6e6 e5e5e5 e3e3e3 e2e2e2 e0e0e0 dfdfdf dddddd dcdcdc dadada d9d9d9 d7d7d7 d5d5d5 d4d4d4 d2d2d2 d0d0d0 cecece cccccc cacaca c9c9c9 c7c7c7 c5c5c5 c3c3c3 c1c1c1 bfbfbf bcbcbc bababa b8b8b8 b6b6b6 b4b4b4 b2b2b2 afafaf adadad ababab a8a8a8 a6a6a6 a4a4a4 a1a1a1 9f9f9f 9c9c9c 9a9a9a 979797 959595 929292 909090 8d8d8d 8b8b8b 888888 858585 838383 808080 7d7d7d 7a7a7a 787878 757575 727272 6f6f6f 6d6d6d 6a6a6a 676767 646464 616161 5e5e5e 5b5b5b 585858 555555 525252 4f4f4f 4d4d4d 4a4a4a 474747 444444 404040 3d3d3d 3a3a3a 373737 343434 313131 2e2e2e 2b2b2b 282828 252525 222222 1f1f1f 1c1c1c 181818 151515 121212 0f0f0f 0c0c0c 090909 060606 030303\n',
    },
    "timer.yaml": {
      "30s_count_down": b'\r00ff00 00ff00 00ff00 00ff00 00ff00 00ff00 00ff00 00ff00 00ff00 00ff00 00ff00 00ff00 00ff00 00ff00 00ff00 00ff00 00ff00 00ff00 00ff00 00ff00 00ff00 00ff00 00ff00 00ff00 00ff00 00ff00 00ff00\n',
		},
}

def run(esphome, name, effects):
  print(name)
  tmpdir = tempfile.mkdtemp(prefix="elllee")
  try:
    # Compile.
    subprocess.check_output(
        [sys.executable, "ellee.py", name, "--once", "--outdir", tmpdir, "--esphome", esphome, "--as-hex"])
    # Make sure the generated source files and executables match the
    # expectations.
    want = set(list(effects) + list(e + ".cc" for e in effects))
    got = set(os.listdir(tmpdir))
    if want != got:
      print(f"Unexpected effects found in {name}", file=sys.stderr)
      unexpected = got - want
      if unexpected:
        print(f"New effect without expectations: {', '.join(unexpected)}", file=sys.stderr)
      missing = got - want
      if missing:
        print(f"Expectations without effect: {', '.join(missing)}", file=sys.stderr)
      return False
    # Run each effect.
    for execname, want in effects.items():
      got = subprocess.check_output([os.path.join(tmpdir, execname)])
      if got != want:
        print("Want: %r" % want, file=sys.stderr)
        print("Got : %r" % got, file=sys.stderr)
        return False
  finally:
    shutil.rmtree(tmpdir)
  return True

def main():
  actual = set(glob.glob("samples/*.yaml"))
  expected = set(os.path.join("samples", i) for i in EXPECTATIONS)
  if actual != expected:
    unexpected = actual - expected
    if unexpected:
      print(f"New samples without expectations: {', '.join(unexpected)}", file=sys.stderr)
    missing = actual - expected
    if missing:
      print(f"Expectations without sample: {', '.join(missing)}", file=sys.stderr)
    return 1
  esphome = "../esphome"
  for sample, effects in EXPECTATIONS.items():
    if not run(esphome, os.path.join("samples", sample), effects):
      return 1
  return 0

if __name__ == "__main__":
  sys.exit(main())