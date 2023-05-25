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
n = 5

for ax, indi in zip(subplots, indicators):
    my_plotter(ax, indi.get_timeframed_dates()[-abs(i):-abs(i)+i-1], indi.get_timeframed_prices()[-abs(i):-abs(i)+i-1], {"label": "price", "c": "green"})

plt.show() # Bis hier hin klappt es
"""
cleaned_dates = indicator_object.get_timeframed_dates()
cleaned_prices = indicator_object.get_timeframed_prices()
ema8 = indicator_object.compute_ema(8)
ema21 = indicator_object.compute_ema(21)
ema200 = indicator_object.compute_ema(200)


my_plotter(ax1, cleaned_dates[-abs(i):-abs(i)+i-1], cleaned_prices[-abs(i):-abs(i)+i-1], {"label": "price", "c": "green"})
my_plotter(ax2, cleaned_dates[-abs(i):-abs(i)+i-1], cleaned_prices[-abs(i):-abs(i)+i-1], {"label": "price", "c": "green"})
my_plotter(ax2, cleaned_dates[-abs(i):-abs(i)+i-1], ema8[-abs(i):-abs(i)+i-1], {"label": "ema8", "c": "red"})
my_plotter(ax2, cleaned_dates[-abs(i):-abs(i)+i-1], ema21[-abs(i):-abs(i)+i-1], {"label": "ema21", "c": "blue"})
my_plotter(ax2, cleaned_dates[-abs(i):-abs(i)+i-1], ema200[-abs(i):-abs(i)+i-1], {"label": "ema200", "c": "black"})

ax1.legend()
ax2.legend()
ax1.tick_params(axis='x', labelrotation=90)
ax2.tick_params(axis='x', labelrotation=90)
ax1.grid(True)
ax2.grid(True)

for index, label in enumerate(ax1.xaxis.get_ticklabels()):
    if index % n != 0:
        label.set_visible(False)

for index, label in enumerate(ax2.xaxis.get_ticklabels()):
    if index % n != 0:
        label.set_visible(False)

plt.title("DAX - " + timeframe.title())
plt.show()
print("Anzahl der Daten:", len(cleaned_dates))
"""