from functools import partial
from random import random
from threading import Thread
import time
import datetime

from bokeh.models import ColumnDataSource
from bokeh.models import DatetimeTickFormatter
from bokeh.models import DataRange1d
from bokeh.plotting import curdoc, figure

from tornado import gen

# this must only be modified from a Bokeh session callback
source = ColumnDataSource(data=dict(x=[], y=[]))

# This is important! Save curdoc() to make sure all threads
# see the same document.
doc = curdoc()


# Function to interact between websocket thread and
# bokeh thread
@gen.coroutine
def update(x, y):
    source.stream(dict(x=[x], y=[y]))


# Simulates getting data from the websocket
# TODO Replace this with actual websocket code
def blocking_task():
    while True:
        # do some blocking computation
        time.sleep(0.01)
        y = 100 + random() * 10
        x = datetime.datetime.now()

        # but update the document from callback
        doc.add_next_tick_callback(partial(update, x=x, y=y))

p = figure(
    x_axis_label='Time',
    x_axis_type='datetime',
    y_axis_label='Data Value',
    y_range=[0, 110]
)

l = p.line(x='x', y='y', source=source)

p.xaxis.formatter = DatetimeTickFormatter(seconds=["%H:%M:%S"])

# Format x range for better following the data as it is recieved
# Docs: https://bokeh.pydata.org/en/latest/docs/reference/models/ranges.html
p.x_range = DataRange1d(
    follow="end",
    follow_interval=3000,
    range_padding=-0.5,
    default_span=3000,
    min_interval=3000,
    max_interval=5000
)

doc.add_root(p)

# Start websocket thread
thread = Thread(target=blocking_task)
thread.start()
