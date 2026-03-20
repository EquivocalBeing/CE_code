import pandas as pd
import numpy as np
#print("thinking...")
from matplotlib import pyplot as plt


station = "A00018-23162"

data = pd.read_csv(r"C:\Users\cacam\Documents\CE_wind_stations\\" + station + "-2024.", delimiter='\s+') 

data.columns = ["Year", "Month", "Day", "Hour", "Air Temp", "Dew Point", "Pressure (MSL)", "Wind Direction", "Wind Speed", "Sky Condition", "Liquid Precipitation 1 hr", "Liquid Precipitation 6 hr"]


wind = data["Wind Speed"]  # m
year = data["Year"]
month = data["Month"]
day = data["Day"]
hour = data["Hour"]
#print("thinking...")

dates = []

for i in range(0, len(year)):
    date = str(year[i]) + ","  + str(month[i]) + "," + str(day[i]) + "."  + str(hour[i])
    dates.append(date)


wind = [0 if item == -9999 else item for item in wind]

wind = np.array(wind)
#print("thinking...")

plt.figure(figsize = (20, 8))
plt.plot(dates, wind/10)


plt.title(station, fontweight = 'bold' , fontsize = 25)
plt.xlabel("Date", fontweight = 'bold' , fontsize = 20)
plt.ylabel("Wind Speed [m/s]", fontweight = 'bold' , fontsize = 20)

plt.grid(True)
plt.tight_layout()

plt.yticks(fontsize = 20, fontweight = "bold")
plt.xlim(dates[0], dates[-1])
plt.savefig(station + ".png")