# import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
from pprint import pprint


def handling_ticket():
    data_return = {}
    data = pd.read_csv('data/data.txt', sep=",", header=None,
                       names=["price", "time", "flightNumber"])
    data.fillna(value='0')

    data['time_info'] = pd.to_datetime(data['time'])
    data['Hour'] = data['time_info'].apply(lambda time: time.hour)
    data['Month'] = data['time_info'].apply(lambda time: time.month)
    data['Day of Week'] = data['time_info'].apply(lambda time: time.dayofweek)
    data['Day'] = data['time_info'].apply(lambda time: time.day)
    data['year'] = data['time_info'].apply(lambda time: time.year)

    # ticket of day
    data_return["day"] = data.groupby([data['Day']])['flightNumber'].count().to_dict()

    return data_return


print("handling_ticket", handling_ticket())
