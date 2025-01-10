#!/usr/bin/env python3


from waveshare_epd import epd2in13g


epd = epd2in13g.EPD()
epd.init()
epd.Clear()
epd.sleep()
