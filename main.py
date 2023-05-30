"""
Nghi Huynh, Minh Mai, Joseph Tran
CSE 163
This program implements functions that uses datasets to visualize gun violence
within the United States and the world.
"""


import us_visual
import world

US_GV_FILE = 'project_data/gun_violence_data.csv'
US_CITY_FILE = 'project_data/uscities.csv'
US_SHP_FILE = 'project_data/States_shapefile.shp'
WORLD_CSV_FILE = 'project_data/gun_violence.csv'
WORLD_SHP_FILE = 'project_data/1fdd5bd6-3068-4741-aac4-51b6a5e947a92020328' \
           '-1-1wu6yf6.89k6.SHP'


def main():
    # Plot US
    gun_stats = us_visual.load_csv(US_GV_FILE)
    us_visual.plot_gunv_incidents_map(gun_stats)
    us_visual.top_50_cities(US_CITY_FILE, gun_stats)
    us_visual.plot_gun_statistics(gun_stats)
    us_visual.plot_incidents_data(gun_stats)
    us_visual.plot_yearly_data(gun_stats)
    us_visual.plot_48death_map(gun_stats, US_SHP_FILE)

    # Plot World
    world.plot_world(WORLD_SHP_FILE, WORLD_CSV_FILE)
    world.charts(WORLD_CSV_FILE)


if __name__ == '__main__':
    main()
