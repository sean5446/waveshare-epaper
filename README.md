# Raspberry Pi Zero W ePaper Hat

## Background
For this project, I was using the 2.13inch e-Paper HAT (G) from Waveshare

It takes about 20 seconds to update the G HAT. The datasheets says its about 25 seconds. The datasheet says the 3 color screens (no yellow) refresh in about 15 seconds. The white/black screens have a partial refresh that is fast. 

## Stock Graph
Notice the jitter and moving text to try to prevent burn-in

![Loading animation](animated_graph.gif)

## Precautions
The screen should be refreshed at least once every 24 hours, with a minimum refresh interval of 180 seconds. To prevent damage, it should not stay powered on for extended periods. After displaying content, the screen should be put into sleep mode. When not in use, the screen should either be set to sleep mode or powered off.

https://www.waveshare.com/wiki/2.13inch_e-Paper_HAT_(G)_Manual#Precautions


## Setup
To import the `waveshare_epd` library, you need to install the library first:

Get library and font from Waveshare. I recommend not trying to clone the entire ~1GB repo onto a raspi. Use another computer and copy the `Separate_Program` folder over or selectively clone the folder.

https://github.com/waveshareteam/e-Paper/tree/master/E-paper_Separate_Program/2in13_e-Paper_G/RaspberryPi_JetsonNano/python

Their code currently does not have a `setup.py`, so make `lib/setup.py` file with the following contents:

```python
import setuptools
setuptools.setup(name="waveshare_epd", version='0.1', packages=["waveshare_epd"])
```

Then install it with: `pip install -e lib/`

Move the font file `pic/Font.ttc ` to the same directory as the python scripts

## Running
To quickly mess around with the code and see what the results look like, use:

`python3 stock_test_screens.py`

To run indefintely on the raspi, use:

`nohup python3 epaper.py > /dev/null &`
