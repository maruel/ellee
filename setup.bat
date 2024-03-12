@echo off
:: Copyright 2024 Marc-Antoine Ruel. All rights reserved.
:: Use of this source code is governed under the Apache License, Version 2.0
:: that can be found in the LICENSE file.

cd "%~dp0"

set PATH=%PATH%;C:\msys64\ucrt64\bin
if not exist c:\msys64\ucrt64\bin\g++.exe (
    echo "Downloading MSYS2"
    curl -LO https://github.com/msys2/msys2-installer/releases/download/2024-01-13/msys2-x86_64-20240113.exe
    echo "Installing MSYS2"
    msys2-x86_64-20240113.exe in --confirm-command --accept-messages --root C:/msys64
    del msys2-x86_64-20240113.exe
    echo "Installing g++"
    C:\msys64\usr\bin\pacman -S --noconfirm --needed base-devel mingw-w64-ucrt-x86_64-toolchain
)

pip3 install -r requirements.txt
