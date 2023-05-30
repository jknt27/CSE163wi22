"""
Nghi Huynh, Minh Mai, Joseph Tran
CSE 163
This program implements functions that uses datasets to visualize gun violence
around the world.
"""


import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt


def plot_world(shp_file_name, csv_file_name):
    """
    Plots two maps of the world, one with the mortality rate and the
    other with gun ownership rate. Figure is saved as a png format.
    """
    # read data
    world = gpd.read_file(shp_file_name)
    gunv = pd.read_csv(csv_file_name)

    # merge
    world_data = world.merge(gunv, left_on='COUNTRY', right_on='country')

    # get necessary columns and dissolve
    world_data = world_data[['COUNTRY', 'mortality_rate', 'ownership_rate',
                             'geometry']]

    # plot
    fig, [ax1, ax2] = plt.subplots(nrows=2, figsize=(20, 10))
    world.plot(color='#EEEEEE', ax=ax1)
    world_data.plot(column='mortality_rate', legend=True, ax=ax1)

    world.plot(color='#EEEEEE', ax=ax2)
    world_data.plot(column='ownership_rate', legend=True, ax=ax2)

    # labels
    ax1.set_title('Mortality Rates by Country')
    ax2.set_title('Gun Ownership Rates by Country')

    # save and close
    plt.savefig('Output/plot_world.png', bbox_inches='tight')
    plt.close()


def charts(csv_file_name):
    """
    Plots a bar graph of countries with high mortality and gun ownership rates.
    Saves plot as a png format.
    """
    # read data
    data = pd.read_csv(csv_file_name)
    data = data[['country', 'mortality_rate', 'ownership_rate']]
    data = data[data['mortality_rate'] > 5]

    # chart
    x_axis = np.arange(len(data['country']))
    plt.bar(x_axis - 0.2, data['mortality_rate'], 0.4, label='Mortality Rate')
    plt.bar(x_axis + 0.2, data['ownership_rate'], 0.4, label='Ownership Rate')

    # labels
    plt.title('Countries vs Mortality and Gun Ownership Rates')
    plt.xticks(x_axis, data['country'], rotation=90)
    plt.xlabel('Countries')
    plt.ylabel('Rates')
    plt.legend()

    # save and close
    plt.savefig('Output/world_chart.png', bbox_inches='tight')
    plt.close()
