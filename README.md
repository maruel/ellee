# Esphome Lambda Light Effect Emulator (ellee)

Creating a new effect for an addressable light in esphome can be tedious. You
try a new tweak, compile, upload, have the device reboot, then switch the effect
on. What about emulating the effect on the terminal instead? This project does
exactly that!

Ellee loads an [esphome.io](https://esphome.io) configuration yaml file, finds
the [addressable_lambda
effect](https://esphome.io/components/light/index.html#addressable-lambda-effect)
and generate a standalone C++ executable that emulates it, for faster iteration.
