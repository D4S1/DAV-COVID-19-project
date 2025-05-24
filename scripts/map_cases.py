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
    df_states = pd.read_csv(url)
    df_states['date'] = pd.to_datetime(df_states['date'])
    df_states['date'] = df_states['date'].dt.to_period('D')
    df_states = df_states[['date', 'state', 'confirmed_cum']]

    cases_min = df_states['confirmed_cum'].min()
    cases_max = df_states['confirmed_cum'].max()


    # Create daily datetime index
    start = df_states.date.min()
    end = df_states.date.max()
    datetime_index = pd.period_range(start=start, end=end, freq='D')
    dt_index_epochs = datetime_index.to_timestamp().astype("int64") // 10**9
    dt_index = dt_index_epochs.astype("U10")

    # Colormap
    colormap = cm.linear.Set2_03.scale(cases_min, cases_max)
    colormap.caption = 'Number of COVID cases'

    n_periods = len(dt_index)

    styledata = {}

    for _, state in enumerate(geo_df.STATE_NAME):
        df_state = df_states[df_states.state == state]

        df = pd.DataFrame(
            {
                "color": df_state.confirmed_cum.apply(colormap).values,
                "opacity": [0.7]*n_periods,
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
        output_path = "/home/hoshi/ME/Coding/DAV-COVID-19-project/images/map_cases.html"
        m.save(output_path)
        print(f"Map saved to {output_path}")
    else:
        print(f"Unrecognized plot mode. Expected 0 (show) or 1 (save), got {args.mode}")
