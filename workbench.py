import matplotlib.pyplot as plt
import requests
from services import Indicator, my_plotter


urlstring = "http://stock.eugenkraft.com"
data = requests.get(urlstring+"/price/1").json()
dates = data["Datum"]
price = data["Preis"]
timeframe = "daily"

indicator_object = Indicator(dates, price, timeframe)
bollinger_bands = indicator_object.compute_bolinger_bands()
cleaned_dates = indicator_object.get_timeframed_dates()
cleaned_prices = indicator_object.get_timeframed_prices()
keltner_tunnel = indicator_object.compute_keltner_tunnel()
chande_momentums = indicator_object.compute_chande_momentum()
ema8 = indicator_object.compute_ema(8)
ema21 = indicator_object.compute_ema(21)
ema200 = indicator_object.compute_ema(200)

n = 5
fig, (ax1, ax2) = plt.subplots(1, 2)
fig.subplots_adjust(bottom=0.14)

i = -200
my_plotter(ax1, cleaned_dates[i:i+200-1], bollinger_bands["bb_oben"][i:i+200-1], {"label": "bb_oben", "c": "orange"})
my_plotter(ax1, cleaned_dates[i:i+200-1], bollinger_bands["bb_mitte"][i:i+200-1], {"label": "bb_mitte", "c": "orange"})
my_plotter(ax1, cleaned_dates[i:i+200-1], bollinger_bands["bb_unten"][i:i+200-1], {"label": "bb_unten", "c": "orange"})
my_plotter(ax1, cleaned_dates[i:i+200-1], keltner_tunnel["kt_oben"][i:i+200-1], {"label": "kt_oben", "c": "blue"})
my_plotter(ax1, cleaned_dates[i:i+200-1], keltner_tunnel["kt_unten"][i:i+200-1], {"label": "kt_unten", "c": "blue"})
my_plotter(ax1, cleaned_dates[i:i+200-1], keltner_tunnel["kt_mitte"][i:i+200-1], {"label": "kt_mitte", "c": "blue"})
my_plotter(ax1, cleaned_dates[i:i+200-1], cleaned_prices[i:i+200-1], {"label": "price", "c": "green"})
my_plotter(ax2, cleaned_dates[i:i+200-1], cleaned_prices[i:i+200-1], {"label": "price", "c": "green"})
my_plotter(ax2, cleaned_dates[i:i+200-1], ema8[i:i+200-1], {"label": "ema8", "c": "red"})
my_plotter(ax2, cleaned_dates[i:i+200-1], ema21[i:i+200-1], {"label": "ema21", "c": "blue"})
my_plotter(ax2, cleaned_dates[i:i+200-1], ema200[i:i+200-1], {"label": "ema200", "c": "black"})

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
