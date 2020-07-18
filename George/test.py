import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('london_sports_participation.csv', header=0)

df['sports_participation'].replace({
    "zero": 0,
    "one+": 1,
    "three+": 2}, inplace=True)

year_map = lambda x: int(x[:4])
df['year'] = df['year'].apply(year_map)

w_df = df[df['area'] == 'London']
w_df = w_df.sort_values(by=['year', 'sports_participation'])

years = w_df['year'].to_numpy()[::3]
low_sports = w_df['percentage'].to_numpy()[::3]
mid_sports = w_df['percentage'].to_numpy()[1::3] - w_df['percentage'].to_numpy()[2::3]
high_sports = w_df['percentage'].to_numpy()[2::3]

plt.figure(1)
plt.plot(years, low_sports)
plt.plot(years, mid_sports)
plt.plot(years, high_sports)
plt.legend(('Proportion no sports', 'Proportion 1-2 sports', 'Proportion 3+ sports'))
plt.show()


