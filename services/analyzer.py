from math import sqrt
from datetime import datetime
from copy import copy


class Indicator:

    def __init__(self, dates, prices, timeframe, index=None):

        self._orig_dates = dates[:]
        self._orig_prices = prices[:]

        self._timeframe = timeframe
        self._index = index

        selected_data = self.__time_conduit()
        self._dates = selected_data["dates"][:]
        self._prices = selected_data["prices"][:]

        if not self._index:
            self._index = self.__ask_date()

    def __time_conduit(self):

        clean_dates = []
        clean_prices = []
        timeframes = ["minutely", "hourly", "daily", "weekly", "monthly"]
        dateobj_prev = None
        p = 0.0

        def append_data(dateobject, price):

            clean_dates.append(dateobject.strftime("%Y-%m-%d %H:%M:%S"))
            clean_prices.append(price)

        for d, p in zip(self._orig_dates, self._orig_prices):

            dateobj = datetime.strptime(d, "%a, %d %b %Y %H:%M:%S %Z")

            if dateobj_prev is None:
                dateobj_prev = dateobj
                continue

            if self._timeframe == timeframes[0] or (self._timeframe == timeframes[1] and dateobj_prev.minute == 0):

                append_data(dateobj_prev, p)

            elif self._timeframe == timeframes[2]:

                if dateobj.day != dateobj_prev.day:
                    append_data(dateobj_prev, p)

            elif self._timeframe == timeframes[3] and dateobj.day != dateobj_prev.day:

                if dateobj_prev.weekday() >= 4:

                    if dateobj.day != dateobj_prev.day:
                        append_data(dateobj_prev, p)

            elif self._timeframe == timeframes[-1] and dateobj.month != dateobj_prev.month:

                append_data(dateobj_prev, p)

            dateobj_prev = dateobj

        append_data(dateobj_prev, p)
        return {"dates": clean_dates, "prices": clean_prices}

    def __compute_std(self, closes, avarage, period):

        """closes: list[float]; avarage:int or float; period:int
        closes have to be the same length as period."""

        sum_up = 0

        for number in closes:
            sum_up += pow(number - avarage, 2)
        varianz = sum_up / period

        return round(sqrt(varianz), 2)

    def __compute_sma_std(self, closes, period):

        """Returns with the prices and period int given, the sma and Standardabweichung back."""

        sma = []
        stds = []
        quantity = []
        counter = 0

        for price in closes:
            counter += 1

            if len(quantity) < period and counter <= period:
                quantity.append(price)
                sma.append(None)
                stds.append(None)

            elif len(quantity) >= period:

                avarage = round(sum(quantity) / period, 2)
                std = self.__compute_std(quantity, avarage, period)
                quantity.pop(0)
                quantity.append(price)
                sma.append(avarage)
                stds.append(std)

        return {"sma": sma, "std": stds}

    def __ask_date(self):

        """Date String without Seconds (%Y-%m-%d %H:%M)"""

        while True:

            try:
                print("You can also type in 'last' or 'first' for the first or last 200 records")
                rough_answer = input(f"desired date for {self._timeframe} timeframe in (yyyy-mm-dd hh:mm) ")

                if rough_answer == 'last':
                    return {'start': -200 or 0, 'end': self._dates.index(self._dates[-1])}
                if rough_answer == 'first':
                    return {'start': 0, 'end': 200 or self._dates.index(self._dates[-1])}

                custom_date_obj = datetime.strptime(rough_answer, "%Y-%m-%d %H:%M")
                custom_date = custom_date_obj.strftime("%Y-%m-%d %H:%M")

            except ValueError as valerr:
                print(valerr)
                print("Try again!")
                continue

            for i, date in enumerate(self._dates):

                custom_timestamp = int(custom_date_obj.timestamp())
                database_timestamp = int(datetime.strptime(date, "%Y-%m-%d %H:%M:%S").timestamp())

                if database_timestamp > custom_timestamp:
                    result = {'start': i}
                    end_index = i + 200

                    try:
                        try_val = self._dates[end_index]
                        result.update({'end': end_index})
                    except IndexError:
                        end_index = self._dates.index(self._dates[-1])
                        result.update({'end': end_index})

                    return result

            print(f"Not such date: {custom_date}!")
            continue

    def compute_bolinger_bands(self, period=20, factor=2):

        datadict = self.__compute_sma_std(closes=self._prices, period=period)

        smas = datadict["sma"]
        stds = datadict["std"]

        bb_oben = []
        bb_mitte = []
        bb_unten = []

        for ma, std in zip(smas, stds):

            if ma is None:

                bb_mitte.append(ma)
                bb_oben.append(ma)
                bb_unten.append(ma)
                continue

            else:

                q = (factor * std)

                bb_mitte.append(ma)

                oben = round(ma + q, 2)
                bb_oben.append(oben)

                unten = round(ma - q, 2)
                bb_unten.append(unten)

        return {"bb_oben": bb_oben, "bb_mitte": bb_mitte, "bb_unten": bb_unten}

    def compute_ema(self, period):

        avarages = []
        emas = []
        smoothfactor = 2 / (period + 1)
        counter = 0

        for price in self._prices:

            if len(avarages) < period:

                avarages.append(price)
                emas.append(None)

            elif len(avarages) >= period:

                if counter < 1:

                    ema = price * smoothfactor + (sum(avarages) / period) * (1 - smoothfactor)
                    emas.append(round(ema, 2))
                    counter += 1

                elif counter >= 1:

                    real_ema = price * smoothfactor + emas[-1] * (1 - smoothfactor)
                    emas.append(round(real_ema, 2))
        if self._index:
            return emas[self._index['start']:self._index['end']]
        return emas

    def compute_keltner_tunnel(self, period=20, factor=1.5):

        typical_prices = []
        trading_margins = []
        timestamp_list = []
        counter = 0

        middle_band = []
        lower_band = []
        upper_band = []

        for date in self._dates:

            dateobject = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            timestamp_list.append(int(dateobject.timestamp()))

            if len(timestamp_list) > 1:

                point_to_point_values = []

                for orig_date, orig_price in zip(self._orig_dates[counter:], self._orig_prices[counter:]):

                    orig_dateobject = datetime.strptime(orig_date, "%a, %d %b %Y %H:%M:%S %Z")
                    orig_timestamp = int(orig_dateobject.timestamp())

                    if timestamp_list[-2] < orig_timestamp < timestamp_list[-1]:
                        point_to_point_values.append(orig_price)

                    elif orig_timestamp >= timestamp_list[-1]:
                        point_to_point_values.append(orig_price)
                        typical_price = round((max(point_to_point_values) + min(point_to_point_values) +
                                               point_to_point_values[-1]) / 3, 2)
                        typical_prices.append(typical_price)
                        trading_margin = round((max(point_to_point_values) - min(point_to_point_values)) * factor, 2)
                        trading_margins.append(trading_margin)
                        break

                    counter += 1

            if len(typical_prices) >= period:

                middle_line = round(sum(typical_prices[-abs(period):]) / period, 2)
                middle_band.append(middle_line)
                upper_line = round(middle_line + sum(trading_margins[-abs(period):]) / period, 2)
                upper_band.append(upper_line)
                lower_line = round(middle_line - sum(trading_margins[-abs(period):]) / period, 2)
                lower_band.append(lower_line)

            elif len(typical_prices) < period:

                middle_band.append(None)
                lower_band.append(None)
                upper_band.append(None)

        return {"kt_oben": upper_band, "kt_mitte": middle_band, "kt_unten": lower_band}

    def compute_chande_momentum(self, period=12):

        up_diffs = []
        down_diffs = []
        chande_momentums = []
        prev_price = 0

        for price in self._prices:

            if len(up_diffs) >= period:
                sum_up = sum(up_diffs[-abs(period):])
                sum_down = sum(down_diffs[-abs(period):])
                chande_momentum = round(100 * ((sum_up - sum_down) / (sum_up + sum_down)), 2)
                chande_momentums.append(chande_momentum)

            if len(up_diffs) < period:
                chande_momentums.append(None)

            if prev_price == 0:
                prev_price = copy(price)

            if price > prev_price:
                up_diffs.append(price - prev_price)
                down_diffs.append(0)

            if price < prev_price:
                down_diffs.append(prev_price - price)
                up_diffs.append(0)

            prev_price = copy(price)

        return chande_momentums

    def get_timeframed_dates(self):

        if self._index:
            return self._dates[self._index['start']:self._index['end']]
        return self._dates

    def get_timeframed_prices(self):

        if self._index:
            return self._prices[self._index['start']:self._index['end']]
        return self._prices

    def get_orig_dates(self):

        return self._orig_dates
