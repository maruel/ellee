# Esphome Lambda Light Effect Emulator (ellee)

Creating a new effect for an addressable light in esphome can be tedious. You
try a new tweak, compile, upload, have the device reboot, then switch the effect
on ... just to realize nothing happens because the esp8266 or esp32 crashed. 😩
It's really hard to debug when a lambda causes a crash! 💣

What about emulating the effect on your local terminal instead and be able to
debug locally? This project does exactly that! 🎉

Ellee loads an [esphome.io](https://esphome.io) configuration yaml file, finds
the [addressable_lambda effect](https://esphome.io/components/light/index.html#addressable-lambda-effect)
and generates a standalone C++ executable that emulates a LED strip for faster
iteration!

Crank these animations! ⏩

## Usage

```
git clone https://github.com/esphome/esphome ../esphome
./ellee.py --esphome ../esphome sample.yaml
./a.out
```

Ctrl-C out to stop the animation.
