import itertools
from pprint import pprint
import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt

sports_df = pd.read_csv('london_sports_participation.csv', header=0)
london_boroughs = {'Kensington And Chelsea', 'Lambeth', 'Hammersmith And Fulham',
    'Westminster', 'Richmond Upon Thames', 'Havering', 'Camden', 'Ealing', 'Brent', 
    'Bexley', 'Waltham Forest', 'City Of London', 'Redbridge', 'Sutton', 
    'Kingston Upon Thames', 'Croydon', 'Lewisham', 'Haringey', 'Merton', 
    'Islington', 'Wandsworth', 'Bromley', 'Southwark', 'Greenwich', 'Hillingdon', 
    'Hackney', 'Newham', 'Enfield', 'Tower Hamlets', 'Hounslow', 
    'Barking And Dagenham', 'Barnet', 'Harrow'}

sports_df = sports_df[sports_df['area'].isin(london_boroughs)].reset_index(drop=True)

sports_df['sports_participation'].replace({
    "zero": 0,
    "one+": 1,
    "three+": 2}, inplace=True)

sports_df['year'] = sports_df['year'].apply(lambda x: int(x[:4]))
sports_df = sports_df.dropna()
sports_df = sports_df.sort_values(['area', 'year', 'sports_participation'])

mod_df = pd.DataFrame(columns=['area', 'year', 'area_code', 'sports_participation', 'percentage'])

for name, group in sports_df.groupby(['area', 'year']):
    if len(group) == 3:
        group = group.loc[:, ['area', 'year', 'area_code', 'sports_participation', 'percentage']].reset_index(drop=True)
        group.loc[1, 'percentage'] -= group.loc[2, 'percentage']
        response_rate = group['percentage'].sum()
        group['percentage'] /= response_rate
        mod_df = mod_df.append(group)
mod_df = mod_df.reset_index(drop=True)

# p_vals = {}

# def do_perm_test(year_low, year_high, data):
#     n_years = year_high - year_low + 1
#     n_years_comp = len(data) - n_years
#     test_stat = sum(data.loc[year_low:year_high, 'Unhealthy Weight Index']) / n_years \
#         - sum(data.drop(index=np.arange(year_low, year_high+1))['Unhealthy Weight Index']) / n_years_comp
#     all_stats = []
#     for comb in itertools.combinations(list(range(2006, 2019)), n_years):
#         stat = sum(data.loc[comb, 'Unhealthy Weight Index']) / n_years \
#             - sum(data.drop(index=list(comb))['Unhealthy Weight Index']) / n_years_comp
#         all_stats.append(stat)
#     all_stats = np.array(all_stats)
#     return np.sum(all_stats <= test_stat) / len(all_stats)

# def do_t_test(year, data):
#     pass

# for borough in valid_bors:
#     bor_df = df[df['Local Authority'] == borough]
#     p_vals[borough] = do_perm_test(2012, 2018, bor_df)

# pprint(p_vals)
# p_df = pd.DataFrame(list(p_vals.items()), columns=['NAME', 'p_vals'])


# map_df = gpd.read_file('statistical-gis-boundaries-london/statistical-gis-boundaries-london/ESRI/London_Borough_Excluding_MHW.shp')
# map_df = map_df.sort_values('NAME').reset_index(drop=True)
# upper_f = lambda x: " ".join([w[0].upper() + w[1:] for w in x.split(" ")])
# map_df['NAME'] = map_df['NAME'].apply(upper_f)

# merged = map_df.set_index('NAME').join(p_df.set_index('NAME'), how='inner')

# vmin, vmax = 0, 1
# merged.plot(column='p_vals', cmap='Blues', linewidth=0.8, edgecolor='0.8')
# plt.show()
