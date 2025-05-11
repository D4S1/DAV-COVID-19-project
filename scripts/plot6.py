<<<<<<< HEAD
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
=======
import pandas as pd
import plotly.graph_objects as go
from utils import *
import plotly.express as px
import io
import PIL

def main():
	args = parse_args("plot6")
	if args:
		if args[1]<3 :
			
			data=pd.read_csv(args[8])
			data["ced_95_top"]=data["cumulative_estimated_daily_excess_deaths_ci_95_top"]-data["cumulative_estimated_daily_excess_deaths"]
			data["ced_95_bot"]= data["cumulative_estimated_daily_excess_deaths"]-data["cumulative_estimated_daily_excess_deaths_ci_95_bot"]
			ymin=data["cumulative_estimated_daily_excess_deaths"].min()
			ymax=data["cumulative_estimated_daily_excess_deaths"].max()
			fig = go.Figure()
			fig.add_trace(go.Scatter(x=data["date"].values, y=data["cumulative_estimated_daily_excess_deaths"].values,
					mode='lines',
					name='Australia',
					line=dict(color='rgb(0,100,0)'),))
			fig.add_trace(go.Scatter(x=data["date"].values, y=data["cumulative_estimated_daily_excess_deaths"].values+data["ced_95_top"].values,
					mode='lines',
					name='Australia - upper bond ci95',
					showlegend=False,
					fillcolor="rgb(0,100,0,0.5)" ,
					line=dict(width=0)))
			fig.add_trace(go.Scatter(x=data["date"].values, y=data["cumulative_estimated_daily_excess_deaths"].values-data["ced_95_bot"].values,
					mode='lines',
					name='Australia - lower bond ci95',
					showlegend=False,
					fillcolor="rgb(0,100,0,0.5)",
					line=dict(width=0)))
			data=pd.read_csv(args[9])
			data["ced_95_top"]=data["cumulative_estimated_daily_excess_deaths_ci_95_top"]-data["cumulative_estimated_daily_excess_deaths"]
			data["ced_95_bot"]= data["cumulative_estimated_daily_excess_deaths"]-data["cumulative_estimated_daily_excess_deaths_ci_95_bot"]
			ymin=min(data["cumulative_estimated_daily_excess_deaths"].min(),ymin)
			ymax=max(ymax,data["cumulative_estimated_daily_excess_deaths"].max())
			fig.add_trace(go.Scatter(x=data["date"].values, y=data["cumulative_estimated_daily_excess_deaths"].values,
					mode='lines',
					name='Poland',
					line=dict(color='rgb(250,0,0)'),))
			fig.add_trace(go.Scatter(x=data["date"].values, y=data["cumulative_estimated_daily_excess_deaths"].values+data["ced_95_top"].values,
					mode='lines',
					name='Poland- upper bond ci95',
					showlegend=False,
					fillcolor="rgb(100,0,0,0.5)" ,
					line=dict(width=0)))
			fig.add_trace(go.Scatter(x=data["date"].values, y=data["cumulative_estimated_daily_excess_deaths"].values-data["ced_95_bot"].values,
					mode='lines',
					name='Poland - lower bond ci95',
					showlegend=False,
					fillcolor="rgb(100,0,0,0.5)",
					line=dict(width=0)))
			# Add waves of COVID
			fig.add_trace(go.Scatter(x=['2020-11-1','2020-11-1'], y=[ymin-1000,ymax+1000],
					mode='lines',
					hovertext='End of wave 2',
					showlegend=False,
					line=dict(width=1,color='rgb(0,0,250)',dash='dash')))
			fig.add_trace(go.Scatter(x=['2021-6-16','2021-6-16'], y=[ymin-1000,ymax+1000],
					mode='lines',
					hovertext='Start of Delta Wave',
					showlegend=False,
					line=dict(width=1,color='rgb(0,0,250)',dash='dash')))
			fig.add_trace(go.Scatter(x=['2021-12-14','2021-12-14'], y=[ymin-1000,ymax+1000],
					mode='lines',
					hovertext='End of Delta Wave\nStart of Omicron Wave',
					showlegend=False,
					line=dict(width=1,color='rgb(0,0,250)',dash='dash')))
			fig.add_trace(go.Scatter(x=['2023-12-14','2023-12-14'], y=[ymin-1000,ymax+1000],
					mode='lines',
					hovertext='End of Omicron Wave',
					showlegend=False,
					line=dict(width=1,color='rgb(0,0,250)',dash='dash')))
			## add retrangulars 
			fig.add_vrect(x0 = '2021-6-16',x1 = '2021-12-14',  
					annotation_text="Delta Wave",annotation_position="top right",
					fillcolor="blue", opacity=0.25, line_width=0,
					annotation=dict(font_size=20  ), #, font_family="Times New Roman")
					)
			fig.add_vrect(x0 = '2021-12-14',x1 = '2023-12-14',  
					annotation_text="Omicron Wave",annotation_position="top right",
					fillcolor="green", opacity=0.25, line_width=0,
					annotation=dict(font_size=20) # , font_family="Times New Roman")
					)

		else:
			pass
			"""
			data=pd.read_csv(args[4])

			data=data.drop(['new_cases', 'new_deaths',  'total_cases'],axis=1)
			data=data.rename(columns={"total_deaths":"Australia (weekly)"})
			data2=pd.read_csv(args[7])
			data2=data2.drop(['new_cases', 'new_deaths',  'total_cases'],axis=1)
			data2=data2.rename(columns={"total_deaths":"Poland (weekly)"})
			data = pd.merge(data, data2,how="left", on=["date"])

			data2=pd.read_csv(args[2])
			data2=data2.drop(['confirmed' ,'deaths' ,'confirmed_cum', 'tests', 'tests_cum', 'positives' ,'positives_cum' ,'recovered', 'recovered_cum',
				'hosp', 'hosp_cum', 'icu' ,'icu_cum' ,'vent', 'vent_cum', 'vaccines', 'vaccines_cum'],axis=1)
			data2=data2.rename(columns={"deaths_cum":"Australia (daily)"})
			data = pd.merge(data, data2,how="outer", on=["date"])

			data2=pd.read_csv(args[5])
			data2=data2.drop(['confirmed' ,'deaths' ,'confirmed_cum', 'tests', 'tests_cum', 'positives' ,'positives_cum' ,'recovered', 'recovered_cum'],axis=1)
			data2=data2.rename(columns={"deaths_cum":"Poland (daily)"})

			data = pd.merge(data, data2,how="outer", on=["date"])
			data=data.sort_values("date")
			data['date'] = pd.to_datetime(data['date'])

			ymax=max(data[['Australia (weekly)', 'Australia (daily)', 'Poland (weekly)', 'Poland (daily)']].max())+1000000

			df = pd.DataFrame() # container for df with new datastructure
			for i in range(len(data["date"])):
				dfa = data.head(i).copy()
#				print(dfa)
				dfa['ix']=i
				df = pd.concat([df, dfa],  ignore_index=True)
			df=df.sort_values(["ix","date"]).reset_index()
#			print(df['ix']==155)
			fig = px.line(df, x = 'date', y = ['Australia (weekly)', 'Australia (daily)', 'Poland (weekly)', 'Poland (daily)'],
						  animation_frame='ix',
						  width=1200, height=900,range_x=[data["date"].min(),data["date"].max()],range_y=[0,ymax])
			fig.layout.updatemenus[0].buttons[0]['args'][1]['frame']['redraw'] = True
			"""
			""" # works very slowly, looking for other options to save gif.
			frames = []
			for s, fr in enumerate(fig.frames):
				print(f"{s}/{len(data)}")
				# set main traces to appropriate traces within plotly frame
				fig.update(data=fr.data)
				# move slider to correct place
				fig.layout.sliders[0].update(active=s)
				# generate image of current state
				frames.append(PIL.Image.open(io.BytesIO(fig.to_image(format="png"))))
				
			"""


		fig.update_layout(
			xaxis=dict(
				title=dict(text='Date'),
				tickfont = dict(size=15),
			),
			yaxis=dict(
				title=dict(text='Cumulative excess of COVID-related deaths'),
				tickfont = dict(size=15)
			),
			legend=dict(
				title=dict(
					text="Country"
				)
			),
			font=dict(
				size=20,
			),
			title=dict(
				text='Total excess of COVID - related deaths (compared to normal times, cumulative)',
				font=dict(size=30),
				x=0.5,
				xanchor='center',
			),			
		)


		if args[1]==2:
			fig.update_layout(
				width=1200,
				height=900)
			fig.write_html(f'{args[0]}', auto_open=False)
			print(args[0])
		elif args[1]==1:
			fig.update_layout(
				width=1500,
				height=1000)
			fig.write_image(f"{args[0]}")
		elif args[1]==3:

			"""
			# create animated GIF
			frames[0].save(
					f"{args[0]}",
					save_all=True,
					append_images=frames[1:],
					optimize=True,
					duration=500,
					loop=0,
				)
			"""
			fig.show()
		else:
	#		fig.write_html(f'{args[1]}', auto_open=True)
			fig.show()	



if __name__ == "__main__":
	main()
>>>>>>> 1eb593986e39910c6c68af7b8ae085ef51341da1
