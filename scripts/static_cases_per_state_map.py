import pandas as pd
import geopandas as gpd
import json
import plotly.express as px
import plotly.graph_objects as go

from utils import get_mode



if __name__ == "__main__":
    au_population = pd.read_csv("/home/hoshi/ME/Coding/DAV-COVID-19-project/data/AU_population.csv", header=0)
    mean_population = au_population.drop(columns=['Date', 'Australia']).mean()

    df = mean_population.reset_index()
    df.columns = ['state', 'population']
    df['population'] = df['population'].astype(int)
    
    state_cases = pd.read_csv('/home/hoshi/ME/Coding/DAV-COVID-19-project/data/AU_state_cases.csv', header=0)
    state_cases = state_cases.groupby('state', as_index=False)['confirmed'].sum().rename(columns={'confirmed': 'cases'})
    df = pd.merge(df, state_cases, on='state')
    
    geo_url = 'https://raw.githubusercontent.com/tonywr71/GeoJson-Data/master/australian-states.json'
    geo_df = gpd.read_file(geo_url)
    
    point_df = pd.DataFrame({
        'x': geo_df.centroid.x,
        'y': geo_df.centroid.y,
        'state': geo_df.STATE_NAME,
        'pt_size': [mean_population[state]/1e5 for state in geo_df.STATE_NAME]
    })

    df = pd.merge(df, point_df, on='state')
    df['cases_per_100k'] = (df['cases'] / df['population']) * 100000
    

    # Add ID field to match GeoJSON
    df['id'] = df['state']  # Adjust if needed

    # Convert to GeoJSON
    geojson_data = json.loads(geo_df.to_json())

    # Create the choropleth map
    fig = px.choropleth(
        df,
        geojson=geojson_data,
        featureidkey="properties.STATE_NAME",
        locations="state",
        color="state",
        color_discrete_sequence=px.colors.qualitative.Pastel1,
        title="Cases per 100k People with Bubble Size Scaled by Population",
        labels={'state': "State"}
    )
    fig.update_layout(
        showlegend=False,
        title_font=dict(size=30),
    )

    fig.add_trace(go.Scattergeo(
        lon=df['x'],
        lat=df['y'],
        text=df['state'],
        mode='markers+text',
        marker=dict(
            size=df['pt_size'],
            color=df['cases_per_100k'],
            colorscale='Reds',
            colorbar=dict(title="Cases per 100k"),
            cmin=df['cases_per_100k'].min(),
            cmax=df['cases_per_100k'].max(),
            opacity=0.9,
            line=dict(width=1, color='white')
        ),
        name='Cases per 100k',
        textposition='top center',
        textfont=dict(size=20, color='black'),
        showlegend=False,
        hovertemplate=(
            "<b>%{text}</b><br>" +
            "Cases: %{customdata[0]}<br>" +
            "Population: %{customdata[1]:,}<br>" +
            "Cases per 100k: %{customdata[2]:.2f}<extra></extra>"
        ),
        customdata=df[['cases', 'population', 'cases_per_100k']].values,
    ))

    fig.update_geos(
        fitbounds="locations",
        visible=False,
    )

    mode = get_mode()
    if mode == 0:
        fig.show()
    elif mode == 2:
        fig.update_layout(
            showlegend=False,
            title_font=dict(size=24),
        )
        fig.write_html("/home/hoshi/ME/Coding/DAV-COVID-19-project/images/static_cases_per_state_map.html")
    elif mode ==1:
        fig.write_image("/home/hoshi/ME/Coding/DAV-COVID-19-project/images/static_cases_per_state_map.png",
                        width=1500,
				        height=1000
                        )