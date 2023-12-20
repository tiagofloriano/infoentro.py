#!/usr/bin/python3
# -*- coding: latin-1 -*-

'''Calculates information entropy of dataset from MRT files
Usage:
    Run the file in the root of the directory where the directories containing the MRT files are located.
Author:
    Tiago Floriano - 2023-12-15
License:
    GNU GPL v3 License
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

import numpy as np
import pandas as pd
import collections
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

def calculate_entropy(time_series):
    n = len(time_series)
    counter = collections.Counter(time_series)
    probabilities = [count / n for count in counter.values()]
    entropy = -sum(p * np.log2(p) for p in probabilities)
    return entropy

time_series = [4, 5, 6, 5, 4, 5, 6]

entropy = calculate_entropy(time_series)
print("Information Entropy:", entropy)

data = pd.Series(time_series)

model = ARIMA(data, order=(1, 1, 1))

fit_model = model.fit()

steps=4
forecast = fit_model.forecast(steps)

print("Prediction for the next {} numbers:".format(steps))
print(forecast)
