#!/usr/bin/env python3

import sys
import os
import time
import logging
import random

# Raspi should come with Pillow and requests
from PIL import Image, ImageDraw, ImageFont
from waveshare_epd import epd2in13g
from stock import Stock


# Initialize logging, screen
logging.basicConfig(level=logging.DEBUG)
epd = epd2in13g.EPD()

# Constants so code is more interchangeable with test script that doesn't import epd
RED = epd.RED
WHITE = epd.WHITE
YELLOW = epd.YELLOW
BLACK = epd.BLACK

# Get fonts
cur_dir = os.path.dirname(os.path.realpath(__file__))
font_file = os.path.join(cur_dir, 'Font.ttc')
font15 = ImageFont.truetype(font_file, 15)
font18 = ImageFont.truetype(font_file, 18)
font24 = ImageFont.truetype(font_file, 24)
font40 = ImageFont.truetype(font_file, 40)

# not sure why these are backwards
width, height = epd.height, epd.width

# Graph dimensions
graph_left = 1
graph_top = 30
graph_right = width - 2
graph_bottom = height - 2
graph_width = graph_right - graph_left
graph_height = graph_bottom - graph_top

stock = Stock()
stock_symbol = 'SPY'


def get_stock_quote(stock, stock_symbol):
    info = stock.get_quote(stock_symbol)
    details = info['quoteSummary']['result'][0]['summaryDetail']
    close = float(details['previousClose']['raw'])
    bid = float(details['bid']['raw'])
    return close, bid


def draw_line_graph(draw, stock, prices, graph_left=graph_left, graph_width=graph_width):
    # Find the minimum, maximum, and number of prices
    min_price, max_price, num_prices = min(prices), max(prices), len(prices)

    # Calculate the range of the prices, +0.01 to prevent div by 0
    price_range = max_price - min_price + 0.01

    # Calculate the horizontal and vertical scale
    x_scale = graph_width / (num_prices - 1)
    y_scale = graph_height / price_range

    # Determine the color and print the stock and percentage change
    color = BLACK if prices[-1] > prices[0] else RED
    plus_minus = '+' if prices[-1] > prices[0] else ''
    pct_change = ((prices[-1] - prices[0]) / prices[0]) * 100
    text = f'{stock} {prices[-1]} {plus_minus}{pct_change:.2f}%'
    draw.text((num_prices, num_prices%2), text, font=font24, fill=color)

    # Plot the prices
    for i in range(num_prices - 1):
        x1 = graph_left + i * x_scale
        y1 = graph_bottom - (prices[i] - min_price) * y_scale
        x2 = graph_left + (i + 1) * x_scale
        y2 = graph_bottom - (prices[i + 1] - min_price) * y_scale
        draw.line((x1, y1, x2, y2), fill=color, width=2)


stock.get_cookie_crumb()
prices = []

# need at least 2 prices to draw a line
close, bid = get_stock_quote(stock, stock_symbol)
prices.append(bid)

while True:
    try:
        logging.debug("Initialize and clear screen...")
        epd.init()
        epd.Clear()

        logging.debug("Generate and display image...")
        image = Image.new('RGB', (epd.height, epd.width), WHITE)  
        draw = ImageDraw.Draw(image)
        close, bid = get_stock_quote(stock, stock_symbol)
        prices.append(bid)
        if len(prices) > 62:
            prices = prices[-62:]
        draw_line_graph(draw, stock_symbol, prices, graph_left=len(prices)%2, graph_width=len(prices)*4)
        epd.display(epd.getbuffer(image))

        logging.debug("Power down screen...")
        epd.sleep()

        logging.debug("Sleep...")
        # if time is after 4pm sleep for 17.5 hours
        if time.localtime().tm_hour >= 16:
            time.sleep(17.5 * 60 * 60)
        else:
            time.sleep(405)

    except Exception as e:
        logging.error("ERROR")
        logging.error(e)
        epd.Clear()
        epd2in13g.epdconfig.module_exit(cleanup=True)
