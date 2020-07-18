import itertools
from pprint import pprint
import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt

df = pd.read_csv('obesity/childhood-obesity-borough-filtered.csv', header=0, index_col=1)

df['Unhealthy Weight Index'] = df['Reception Overweight'] + 2 * df['Reception Obese'] \
    + 1.5 * df['Year 6 Overweight'] + 3 * df['Year 6 Obese']

valid_bors = dict.fromkeys(df['Local Authority'])
p_vals = {}

def do_perm_test(year_low, year_high, data):
    n_years = year_high - year_low + 1
    n_years_comp = len(data) - n_years
    test_stat = sum(data.loc[year_low:year_high, 'Unhealthy Weight Index']) / n_years \
        - sum(data.drop(index=np.arange(year_low, year_high+1))['Unhealthy Weight Index']) / n_years_comp
    all_stats = []
    for comb in itertools.combinations(list(range(2006, 2019)), n_years):
        stat = sum(data.loc[comb, 'Unhealthy Weight Index']) / n_years \
            - sum(data.drop(index=list(comb))['Unhealthy Weight Index']) / n_years_comp
        all_stats.append(stat)
    all_stats = np.array(all_stats)
    return np.sum(all_stats <= test_stat) / len(all_stats)

def do_t_test(year, data):
    pass

for borough in valid_bors:
    bor_df = df[df['Local Authority'] == borough]
    p_vals[borough] = do_perm_test(2012, 2018, bor_df)

pprint(p_vals)
p_df = pd.DataFrame(list(p_vals.items()), columns=['NAME', 'p_vals'])


map_df = gpd.read_file('statistical-gis-boundaries-london/statistical-gis-boundaries-london/ESRI/London_Borough_Excluding_MHW.shp')
map_df = map_df.sort_values('NAME').reset_index(drop=True)
upper_f = lambda x: " ".join([w[0].upper() + w[1:] for w in x.split(" ")])
map_df['NAME'] = map_df['NAME'].apply(upper_f)

merged = map_df.set_index('NAME').join(p_df.set_index('NAME'), how='inner')

vmin, vmax = 0, 1
merged.plot(column='p_vals', cmap='Blues', linewidth=0.8, edgecolor='0.8')
plt.show()
