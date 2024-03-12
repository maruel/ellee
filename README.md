# Esphome Lambda Light Effect Emulator (ellee)

Creating a new effect for an addressable light in esphome can be tedious. To try
a new lambda you just created, you have to compile, upload, have the device
reboot, then switch the effect on ... just to realize nothing happens because
the esp8266 or esp32 crashed. 😩 It's really hard to debug when a lambda causes
a crash! 💣

What about emulating the effect on your local terminal instead and be able to
debug locally? This project does exactly that! 🎉

Ellee loads an [esphome.io](https://esphome.io) configuration yaml file, finds
the [addressable_lambda effect](https://esphome.io/components/light/index.html#addressable-lambda-effect)
and generates a standalone C++ executable that emulates a LED strip for faster
iteration!

Crank these animations! ⏩

## Prerequisites

- On linux or Windows under WSL, run: `sudo apt install g++`
- On macOS, install Xcode.

Install python dependencies with: `./setup.sh; source venv/bin/activate`

## Usage

ellee requires a esphome.git checkout to get the C++ source files to build your
lambda. Then pass both the path to esphome.git and your esphome yaml file
containing a `addressable_lambda` to generate an executable that will output the
effect at the terminal when run. For example:

```
git clone https://github.com/esphome/esphome ../esphome

# A simple count down timer that can be used in meetings to alert partitipant
# that time is up.
./ellee.py samples/timer.yaml
./30s_count_down

# Compare different sinus implementations by looking that the raw values in HEX.
./ellee.py --as-hex --once samples/sin.yaml
./half_sin8
./sin16_c
./sinf
```

Ctrl-C out to stop the animation.

## Tips

Explore the [samples/](samples/) directory for ideas how to make the best use of
this tool. ellee tolerates underspecified effect (e.g.
[`print_then_exit.yaml`](samples/print_then_exit.yaml)) for quicker iteration.
