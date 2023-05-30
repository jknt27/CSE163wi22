"""
Nghi Huynh, Minh Mai, Joseph Tran
CSE 163
This program implements functions that uses datasets to visualize gun violence
within the United States.
"""


import pandas as pd
import altair as alt
from vega_datasets import data
import geopandas as gpd
import matplotlib.pyplot as plt


def load_csv(filename):
    """
    Processes the gun violence CSV and gets rid of all the missing values.
    Returns a dataframe of the gun violence data.
    """
    gv_data = pd.read_csv(filename)
    gv_data[['year', 'month', 'day']] = gv_data['date'].str \
        .split('-', expand=True)
    gv_data = gv_data[['state', 'city_or_county', 'n_killed', 'n_injured',
                       'latitude', 'longitude', 'year']]
    gv_data = gv_data.dropna()
    return gv_data


def plot_gunv_incidents_map(gv_data):
    """
    Plots a US map and all the gun related incidents from the given data frame.
    Plot is then saved as an html  format.
    """
    states = alt.topo_feature(data.us_10m.url, feature='states')
    # plot background of states
    background = alt.Chart(states).mark_geoshape(fill='lightgray',
                                                 stroke='white') \
        .project('albersUsa').properties(width=1400, height=1000)
    # plot points
    points = alt.Chart(gv_data).mark_circle() \
        .encode(longitude='longitude', latitude='latitude',
                size=alt.value(1.5), tooltip='city_or_county') \
        .properties(title='Gun Violence Incidents (2013-2018)')

    gv_map = (background + points).configure_title(fontSize=30)
    gv_map.save('Output/gv_cases.html')


def top_50_cities(filepath, gv_data):
    """
    Plots a US map and all the gun related incidents from the given data frame.
    Additionally, it plots the 50 most populated cities in the US.
    Plot is then saved as an html format.
    """
    city_location_data = pd.read_csv(filepath)
    city_location_data = city_location_data[['city', 'state_name', 'state_id',
                                            'population', 'lat', 'lng']]
    city_location_data = city_location_data.loc[:50]

    # plot states
    states = alt.topo_feature(data.us_10m.url, feature='states')
    # plot background
    background = alt.Chart(states, title='Gun Violence Incidents '
                                         '(2013-2018) & Top 50 Most '
                                         'Populated US Cities') \
        .mark_geoshape(fill='lightgray', stroke='white').project('albersUsa') \
        .properties(width=1400, height=1000)
    # plot of the largest city
    large_cities = alt.Chart(city_location_data).mark_circle() \
        .encode(longitude='lng', latitude='lat', size=alt.value(200),
                tooltip='city', opacity=alt.value(0.5), color=alt.value('red'))
    # plot of gun related incidents
    points = alt.Chart(gv_data).mark_circle() \
        .encode(longitude='longitude', latitude='latitude',
                size=alt.value(1.5), tooltip='city_or_county')
    # plots all ontop of each other
    gv_map = (background + points + large_cities).configure_title(fontSize=30)
    gv_map.save('Output/gv_cases_and_largest_cities.html')


def plot_gun_statistics(gv_data):
    """
    Plots two bar charts from the given data frame, one about total people
    killed and the other about total people injured.
    Plot is then saved in an html format.
    """
    gun_data = gv_data.groupby('state')[['n_killed', 'n_injured']].sum()
    gun_data = gun_data.reset_index()
    gun_data['total dead and injured'] = gun_data['n_killed'] + \
        gun_data['n_injured']
    # Plot
    num_killed = alt.Chart(gun_data).mark_bar().encode(
        alt.X('state', sort='-y', title='US States'),
        alt.Y('n_killed', title='Number of People Killed'),
        tooltip=[alt.Tooltip('state', title='State'),
                 alt.Tooltip('n_killed', title='People Killed')]
    ).properties(title='People Killed per State')
    # plot
    num_injured = alt.Chart(gun_data).mark_bar().encode(
        alt.X('state', sort='-y', title='US States'),
        alt.Y('n_injured', title='Number of People Injured'),
        tooltip=[alt.Tooltip('state', title='State'),
                 alt.Tooltip('n_injured', title='People Injured')]
    ).properties(title='People Injured per State')
    # Combine Plots
    plot = alt.vconcat(num_killed, num_injured).configure_title(fontSize=25)
    plot.save('Output/deaths_vs_injured.html')


def plot_incidents_data(gv_data):
    """
    Plots a bar graph of the given data frame regarding the total gun related
    incidents and the total number of deaths and injuries.
    Plot is then saved in an html format.
    """
    gun_data = gv_data.groupby('state')[['n_killed', 'n_injured']].sum()
    gun_data = gun_data.reset_index()
    gun_data['total dead and injured'] = gun_data['n_killed'] + \
        gun_data['n_injured']
    # total incidents
    incidents = gv_data['state'].value_counts().to_frame('total incidents')
    incidents = incidents.reset_index().rename(columns={'index': 'state'})
    sorting = alt.SortField(field='total incidents', order='descending')
    num_incidents = alt.Chart(incidents).mark_bar() \
        .encode(alt.X('state', sort=sorting, title='US States'),
                alt.Y('total incidents',
                title='Number of Incidents & Total (Death/Injuries)'),
                tooltip=[alt.Tooltip('state', title='State'),
                alt.Tooltip('total incidents',
                            title='Total gun related incidents')])
    # total death and injuries
    num_total = alt.Chart(gun_data).mark_bar(color='red') \
        .encode(alt.X('state', sort=sorting, title='US States'),
                alt.Y('total dead and injured'),
                tooltip=[alt.Tooltip('state', title='State'),
                alt.Tooltip('total dead and injured',
                            title='Total dead and injured')])
    # combine total incidents and total death and injuries
    plot = alt.layer(num_incidents + num_total) \
        .resolve_scale(x='independent') \
        .properties(title='Total Gun Related Incidents per State')
    plot = plot.configure_title('right', fontSize=20)
    plot.save('Output/incidents_vs_total.html')


def plot_yearly_data(gv_data):
    """
    Plots a bar graph with the given data frame of the number of
    deaths and injuries per year. Plot is then saved in an html format.
    """
    gun_data = gv_data.groupby('year')[['n_killed', 'n_injured']].sum()
    gun_data = gun_data.reset_index()
    gun_data = gun_data.rename(columns={'n_killed': 'People Killed',
                                        'n_injured': 'People Injured'})
    # plot
    plot = alt.Chart(gun_data) \
        .transform_fold(['People Killed', 'People Injured'],
                        as_=['Type', 'Number of People']) \
        .mark_bar(size=20).encode(x='year:T', y='Number of People:Q',
                                  color='Type:N').interactive() \
        .properties(title='Number of People Killed/Injured per Year')
    plot.configure_title(fontSize=30)
    plot.save('Output/gun_violence_by_year.html')


def plot_48death_map(gv_data, geodata):
    """
    Plots the 48 mainland US states and the number of people killed
    and injured. Plot is saved as a png format.
    """
    gv_data = gv_data.groupby('state')[['n_killed', 'n_injured']].sum()
    gv_data = gv_data.reset_index()
    mask = (gv_data['state'] != 'Alaska') & (gv_data['state'] != 'Hawaii')
    gv_data = gv_data[mask]
    gv_data['state'] = gv_data['state'].str.upper()
    geodata = gpd.read_file(geodata)
    gun_data = geodata.merge(gv_data, left_on='State_Name', right_on='state')
    gun_data = gun_data[['state', 'geometry', 'n_killed', 'n_injured']]
    fig, [ax1, ax2] = plt.subplots(nrows=2, figsize=(20, 10))
    death_data = gun_data[['n_killed', 'geometry']]
    injured_data = gun_data[['n_injured', 'geometry']]
    gun_data.plot(ax=ax1, color='#EEEEEE')
    gun_data.plot(ax=ax2, color='#EEEEEE')
    death_data.plot(ax=ax1, column='n_killed', legend=True)
    injured_data.plot(ax=ax2, column='n_injured', legend=True)
    ax1.set_title('US Gun Related Deaths (2013-2018)')
    ax2.set_title('US Gun Injuries Deaths (2013-2018)')
    fig.savefig('Output/US_Gun_Deaths.png', bbox_inches='tight')
    plt.close()
