#!/bin/bash
# Copyright 2024 Marc-Antoine Ruel. All rights reserved.
# Use of this source code is governed under the Apache License, Version 2.0
# that can be found in the LICENSE file.

set -eu

if [ ! -d venv ]; then
  python3 -m venv venv
fi

source venv/bin/activate

pip3 install -r requirements.txt
