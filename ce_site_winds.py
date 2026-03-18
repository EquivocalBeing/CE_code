import pandas as pd
import numpy as np
print("thinking...")
from matplotlib import pyplot as plt




data = pd.read_csv("/ligo/home/carlos.campos/Downloads/CE_wind_stations/A00018-23162-2024", delimiter='\s+') 

data.columns = ["Year", "Month", "Day", "Hour", "Air Temp", "Dew Point", "Pressure (MSL)", "Wind Direction", "Wind Speed", "Sky Condition", "Liquid Precipitation 1 hr", "Liquid Precipitation 6 hr"]


wind = data["Wind Speed"]  # m
year = data["Year"]
month = data["Month"]
day = data["Day"]
hour = data["Hour"]

date = []

for i in range(0, len(year)):
    date_x = str(year[i]) + ","  + str(month[i]) + "," + str(day[i]) + "."  + str(hour[i])
    date.append(date_x)


wind = [0 if item == -9999 else item for item in wind]

wind = np.array(wind)

print(date[0])
print(len(hour))

plt.plot(date, wind/10)
plt.xlim(date[0], date[-1])
plt.xlabel("Date")
plt.ylabel("Wind Speed [m/s]")
plt.show()