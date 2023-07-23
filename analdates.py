import matplotlib.pyplot as plt
import requests
from services import Indicator, my_plotter


urlstring = "http://stock.eugenkraft.com"
data = requests.get(urlstring+"/price/1").json()
dates = data["Datum"]
prices = data["Preis"]
timeframes = ["minutely", "hourly", "daily", "weekly"]
indicators = [Indicator(dates, prices, tf) for tf in timeframes]

fig = plt.figure(layout='constrained')
ax1 = fig.add_subplot(221, title=timeframes[0])
ax2 = fig.add_subplot(222, title=timeframes[1])
ax3 = fig.add_subplot(223, title=timeframes[2])
ax4 = fig.add_subplot(224, title=timeframes[3])
subplots = [ax1, ax2, ax3, ax4]

i = 200

for ax, indi in zip(subplots, indicators):
    my_plotter(ax, indi.get_timeframed_dates(), indi.get_timeframed_prices(), {"label": "price", "c": "green"}) # Das hat geklappt
    my_plotter(ax, indi.get_timeframed_dates(), indi.compute_ema(8), {"label": "ema8", "c": "red"}) # Das nicht Warum? Wegen den Emas, die müssen auch noch modifiziert werden!
    my_plotter(ax, indi.get_timeframed_dates(), indi.compute_ema(21), {"label": "ema21", "c": "blue"})
    my_plotter(ax, indi.get_timeframed_dates(), indi.compute_ema(200), {"label": "ema200", "c": "black"})

    ax.legend()
    ax.tick_params(axis='x', labelrotation=90)
    ax.grid(True)

    for index, label in enumerate(ax.xaxis.get_ticklabels()):
        if index % 5 != 0:
            label.set_visible(False)

plt.show()
