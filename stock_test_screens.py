#!/usr/bin/env python3

import os
import random
import sys

# pip install Pillow requests
from PIL import Image, ImageDraw, ImageFont
from stock import Stock


# Defined in epd library
WHITE = 16777215
BLACK = 0
YELLOW = 65535
RED = 255

# Get fonts
cur_dir = os.path.dirname(os.path.realpath(__file__))
font_file = os.path.join(cur_dir, 'Font.ttc')
font15 = ImageFont.truetype(font_file, 15)
font18 = ImageFont.truetype(font_file, 18)
font24 = ImageFont.truetype(font_file, 24)
font40 = ImageFont.truetype(font_file, 40)

# Dimensions of the screen
width, height = 250, 122

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

num_prices = graph_right // 4 # = 62
# 7 horus * 60 mins / 62 = check every 406 seconds

close, price = get_stock_quote(stock, stock_symbol)

# Generate a random list of prices 
prices = [round(random.uniform(price, price+15), 2) for _ in range(num_prices)]

# Make a bunch of graphs to simulate a trading day
images = []
for i in range(0, num_prices):
    image = Image.new('RGB', (width, height), WHITE)
    draw = ImageDraw.Draw(image)
    # Increase width of the printable area, try to prevent burn-in by setting graph_left 0/1
    draw_line_graph(draw, stock_symbol, prices[:i+2], graph_left=i%2, graph_width=i*4)
    images.append(image)

# Save the images as a gif
output_file = 'animated_graph.gif'
images[0].save(output_file,
               save_all=True,
               append_images=images[1:],
               duration=200,  # Frame duration (in milliseconds)
               loop=0)  # Loop the GIF infinitely

# Open the file with the default image viewer
os.startfile(output_file)
