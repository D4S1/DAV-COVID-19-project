import folium
import pandas as pd
import argparse
from random import randint
from folium.plugins import TimeSliderChoropleth
import branca.colormap as cm
import geopandas as gpd

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", help="Plot mode 0 - show in browser, 1 - save to HTML only", type=int)
    args = parser.parse_args()

    # Load GeoJSON
    geo_url = 'https://raw.githubusercontent.com/tonywr71/GeoJson-Data/master/australian-states.json'
    geo_df = gpd.read_file(geo_url)

    # Now export GeoJSON with
    geo_json = geo_df.to_json()

    # Load COVID data
    url = 'https://raw.githubusercontent.com/M3IT/COVID-19_Data/master/Data/COVID_AU_state.csv'
    df_au = pd.read_csv(url)

    # Configure data
    df_au['population'] = [randint(20000, 500000) for _ in range(len(df_au))]

    population_min = df_au['population'].min()
    population_max = df_au['population'].max()

    start = df_au['date'].min()
    end = df_au['date'].max()

    # Create daily datetime index
    datetime_index = pd.date_range(start=start, end=end, freq="D")
    dt_index_epochs = datetime_index.astype("int64") // 10 ** 9
    dt_index = dt_index_epochs.astype("U10")

    # Colormap
    colormap = cm.linear.YlGnBu_09.scale(population_min, population_max)
    colormap.caption = 'Population'

    n_periods = len(dt_index)

    styledata = {}

    for _, state in enumerate(geo_df.STATE_NAME):
        df_state = df_au[df_au.state == state]

        df = pd.DataFrame(
            {
                "color": df_state.population.apply(colormap).values,
                "opacity": [0.7] * n_periods,
            },
            index=dt_index,
        )
        styledata[_] = df

    styledict = {
        str(state): data.to_dict(orient='index') for state, data in styledata.items()
    }

    # Create the folium map
    m = folium.Map(location=[-25, 135], zoom_start=4)

    # Add TimeSliderChoropleth
    TimeSliderChoropleth(
        data=geo_json,
        styledict=styledict,
    ).add_to(m)

    # Add additional GeoJson layer for borders and tooltips
    folium.GeoJson(
        data=geo_json,
        style_function=lambda x: {
            'fillColor': 'transparent',
            'color': 'black',
            'weight': 0.5,
            'fillOpacity': 0,
        },
        tooltip=folium.GeoJsonTooltip(
            fields=['STATE_NAME'],
            aliases=['State:'],
            labels=True,
            sticky=True
        )
    ).add_to(m)

    # Add color legend
    colormap.add_to(m)

    # Save or show
    if args.mode == 0:
        m.show_in_browser()
    elif args.mode == 1:
        output_path = "images/map.html"
        m.save(output_path)
        print(f"Map saved to {output_path}")
    else:
        print(f"Unrecognized plot mode. Expected 0 (show) or 1 (save), got {args.mode}")
