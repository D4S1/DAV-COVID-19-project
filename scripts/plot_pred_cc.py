from statsmodels.tsa.arima.model import ARIMA
from statsmodels.stats.outliers_influence import summary_table
from statsmodels.tsa.stattools import adfuller
import pandas as pd
import plotly.graph_objects as go
from utils import *
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.dates as mdates
from matplotlib.ticker import AutoMinorLocator
import seaborn as sns

def main():
	args = parse_args("plot_pred_cc")
	if args:
		# common parts
		data=pd.read_csv(args[17])[["date","Australia"]]
		data = data.loc[(data["Australia"].isna()==False)].reset_index()
		start_pred = data.index[((data['date'] <= '2021-12-17') & (data['date'] > '2021-12-10'))].values[0]
		end_pred = data.index[((data['date'] <= '2023-01-8') & (data['date'] > '2023-01-01'))].values[0]
		data.set_index("date", inplace=True)
		ymin=0
		ymax=data["Australia"].max()
		data=data.rename(columns={"Australia":"New deaths"})

		# make prediction


		result = adfuller(data["New deaths"])

		print(f"ADF statistic = {result[0]:.3f}, p-value = {result[1]:.3f}")

		df_diff = data["New deaths"].dropna() # .diff().dropna() # .pct_change().dropna()

		# split data to training and testing datasets:
		n = len(df_diff)
		df_diff1=df_diff.iloc[:start_pred].reset_index()["New deaths"]
		df_diff2=df_diff.iloc[start_pred:end_pred].reset_index()["New deaths"]
		# make full model
		p=5
		s=1
		d=5
		w = 0
		t = "c"

		model_fit,code1 = make_SARIMA(df_diff1, p,s,d,w,t)


		pred = model_fit.get_prediction(start=0, end=len(data.index))
		pred_summary = pred.summary_frame(alpha=0.05)
		pred_summary=pred_summary.iloc[1:]
		pred_summary.index=data.index

		# for second prediction
		p=3 # [1,2,3,7,8,9,10] #10
		s=0
		d=2
		w = 0
		t = "c"
		model_fit,code2 = make_SARIMA(df_diff2, p,s,d,w,t)

		pred = model_fit.get_prediction(start=0, end=len(data.index)-start_pred-1)
		pred_summary2 = pred.summary_frame(alpha=0.05)
		pred_summary2=pred_summary2.iloc[1:]
		pred_summary2.index=data.index[start_pred+1:]

		if args[1]<3:

			# change bottom/upper to delta_bottom / delta_upper
			pred_summary["mean_ci_lower"]=pred_summary["mean"] -pred_summary["mean_ci_lower"]
			pred_summary["mean_ci_upper"]=pred_summary["mean_ci_upper"]-pred_summary["mean"]
			pred_summary2["mean_ci_lower"]=pred_summary2["mean"] -pred_summary2["mean_ci_lower"]
			pred_summary2["mean_ci_upper"]=pred_summary2["mean_ci_upper"]-pred_summary2["mean"]
			fig = go.Figure()

			# real data
			fig.add_trace(go.Scatter(x=data.index, y=data["New deaths"].values,
					mode='lines+markers',
					name='Australia',
					line=dict(color='rgb(0,100,0)'),))

			# prediction
			fig.add_trace(go.Scatter(x=pred_summary.index, y=pred_summary["mean"].values,
					mode='lines+markers',
					name=f'Prediction 1\n({code1})',
					line=dict(color='rgb(250,0,0)'),
					marker=dict(size=1,)))

			fig.add_trace(go.Scatter(x=pred_summary2.index, y=pred_summary2["mean"].values,
					mode='lines+markers',
					name=f'Prediction 2\n({code2})',
					line=dict(color='rgb(0,0,250)'),
					marker=dict(size=1,)))

			# confidence intervals
			fig.add_trace(go.Scatter(x=pred_summary.index, y=pred_summary["mean"]-pred_summary["mean_ci_lower"],
					mode='lines',
					name='Prediction - upper bond ci95',
					showlegend=False,
	#				fill='tonexty',
					fillcolor="rgba(250,0,0,0.3)" ,
					line_color = 'rgba(0,0,0,0)',
					line=dict(width=0)))
			fig.add_trace(go.Scatter(x=pred_summary.index, y=pred_summary["mean"]+pred_summary["mean_ci_upper"],
					mode='lines',
					name='Prediction- lower bond ci95',
					showlegend=False,
					fill='tonexty',
					fillcolor="rgba(250,0,0,0.3)" ,
					line_color = 'rgba(0,0,0,0)',
					line=dict(width=0)))
			fig.add_trace(go.Scatter(x=pred_summary2.index, y=pred_summary2["mean"]-pred_summary2["mean_ci_lower"],
					mode='lines',
					name='Prediction - upper bond ci95',
					showlegend=False,
	#				fill='tonexty',
					fillcolor="rgba(0,0,250,0.3)" ,
					line_color = 'rgba(0,0,0,0)',
					line=dict(width=0)))
			fig.add_trace(go.Scatter(x=pred_summary2.index, y=pred_summary2["mean"]+pred_summary2["mean_ci_upper"],
					mode='lines',
					name='Prediction- lower bond ci95',
					showlegend=False,
					fill='tonexty',
					fillcolor="rgba(0,0,250,0.3)" ,
					line_color = 'rgba(0,0,0,0)',
					line=dict(width=0)))


			# Add waves of COVID
			d=10
			"""
			fig.add_trace(go.Scatter(x=['2020-11-1','2020-11-1'], y=[ymin-d,ymax+d],
					mode='lines',
					hovertext='End of wave 2',
					showlegend=False,
					line=dict(width=1,color='rgb(0,0,250)',dash='dash')))
			fig.add_trace(go.Scatter(x=['2021-6-16','2021-6-16'], y=[ymin-d,ymax+d],
					mode='lines',
					hovertext='Start of Delta Wave',
					showlegend=False,
					line=dict(width=1,color='rgb(0,0,250)',dash='dash')))
			"""
			fig.add_vline(x=data.index[start_pred],
					name="Start of prediction 1",
	#				hovertext='Start of prediction 1,\n2021-12-14',
					showlegend=True,
					line=dict(width=1,color='rgb(0,0,250)',dash='dash'))
			fig.add_vline(x=data.index[end_pred], 
					name="Start of prediction 2",
	#				hovertext='Start of prediction 2,\n2023-01-04',
					showlegend=True,
					line=dict(width=1,color='rgb(0,0,250)',dash='dash'))
			"""
			fig.add_trace(go.Scatter(x=['2023-12-14','2023-12-14'], y=[ymin-d,ymax+d],
					mode='lines',
					hovertext='End of Omicron Wave',
					showlegend=False,
					line=dict(width=1,color='rgb(0,0,250)',dash='dash')))
			"""
			## add retrangulars
			""" 
			fig.add_vrect(x0 = '2021-6-16',x1 = '2021-12-14',  
					annotation_text="Delta Wave",annotation_position="top right",
					fillcolor="blue", opacity=0.25, line_width=0,
					annotation=dict(font_size=20  ), #, font_family="Times New Roman")
					)
			"""
			fig.add_vrect(x0 = '2021-12-14',x1 = '2023-12-14',  
					annotation_text="Omicron Wave",annotation_position="top right",
					fillcolor="yellow", opacity=0.25, line_width=0,
					annotation=dict(font_size=20) # , font_family="Times New Roman")
					)

			fig.update_layout(
				xaxis=dict(
					title=dict(text='Date'),
					tickfont = dict(size=15),
				),
				yaxis=dict(
					title=dict(text='Cumulative cases per milion'),
					tickfont = dict(size=15)
				),
				legend=dict(
					title=dict(
						text="Elements"
					)
				),
				font=dict(
					size=20,
				),
				title=dict(
					text='Total number of cases per milion of Australia population',
					font=dict(size=30),
					x=0.5,
					xanchor='center',
				),			
			)


		else:
			values=data["Australia"].values
			names=["Australia","prediction1","prediction2"]
			code = ["AUS", "AR1","AR2"]
			dates=data["date"].copy().values
			xs =data["date"].copy().values
			for d in range(len(dates)):
				dates[d] = mdates.datestr2num(dates[d])
				xs[d]=str(xs[d])
			xdata = []
			ydata=[[] for i in range(len(names))]
			yCIdata=[[[],[]] for i in range(len(names))]
			omi_w_start = mdates.datestr2num('2021-12-14')
			omi_w_end = mdates.datestr2num('2023-12-14')
			delta_w_start = mdates.datestr2num('2021-6-16')
			last=[0 for x in range(len(ydata))]

	#		print(f"number of steps: {len(dates)}\nshape of values:\t{values.shape}\t\n" )#shape of CI:\t{CI[0].shape}\t{CI[1].shape}\nymin = {ymin}\tymax = {ymax}")
			sns.set_theme(style="darkgrid")
			fig, ax = plt.subplots(figsize=(10,7.5))   


			lplot = ax.plot(np.array(dates[0]),np.array([[0],[0],[0]]).T,label=names)
#			fplot1 = ax.fill_between(np.array(dates[0]),np.array([0]),np.array([0]))
#			fplot2 = ax.fill_between(np.array(dates[0]),np.array([0]),np.array([0]))
			fig.legend(bbox_to_anchor=(0.9,0.88),title="Countries",fontsize=15,title_fontsize=18) # 
			ymin=ymin-10
			ymax=ymax*1.1
			yval=[]
			ylab=[]
			for i in range(6):
				yval.append(i*20)
				ylab.append(i*20)
			def init():
				ax.set_ylim(ymin, ymax)
				ax.set_xlim(dates[0],dates[-1]+60)
				ax.set_xlabel('Date',size=18)
				ax.set_ylabel('Cumulative cases per milion',size=18)
				del xdata[:]
				for i in range(len(ydata)):
					del ydata[i][:]
#					for j in range(len(yCIdata[i])):
#						del yCIdata[i][j][:]
				t = ax.text(dates[65], yval[-1]*0.74  ,xs[0], size=30, va="center", ha="center",)
				last=[0,0,0]
				return lplot,t

			def update(frame):
				ax.cla()

				xdata.append(dates[frame])
				for i in range(len(ydata)):
					ydata[i].append(values[frame][i])
					
					if ydata[i] is None:
						y=last[i]
					else:
						y=ydata[i][-1]
						last[i] =ydata[i][-1]
					ax.text(xdata[-1]+0.5, y ,code[i], size=15, va="center", ha="left")

#					for j in range(2):
#						yCIdata[i][j].append(CI[i][frame][j])

#				print(f"x = {xdata}\ny = {ydata}\nCI: {yCIdata}")
				
#				fplot1 = ax.fill_between(np.array(xdata),np.array(yCIdata[0][0]),np.array(yCIdata[0][1]),alpha=0.3,color="C0")
#				fplot2 = ax.fill_between(np.array(xdata),np.array(yCIdata[1][0]),np.array(yCIdata[1][1]),alpha=0.3,color="C1")
				wplot1 = ax.fill_betweenx([ymin,ymax],delta_w_start,omi_w_start,alpha=0.3,color="tab:green")
				wplot2 = ax.fill_betweenx([ymin,ymax],omi_w_start,omi_w_end,alpha=0.3,color='tab:olive')
				ax.text((delta_w_start+omi_w_start)/2, yval[-1] ,f"Delta\nWave", size=15, va="center", ha="center",)
				ax.text((omi_w_end+omi_w_start)/2, yval[-1] ,f"Omicron Wave", size=15, va="center", ha="center",)
				for i in range(len(ydata)):
					tmp=np.array(ydata[i]).astype(np.double)
					mask = np.isfinite(tmp)
#					print(f"frame = {frame},\ti = {i}\ntmp = {tmp.shape}\nmask = {mask.shape}\ndata={len(xdata)}\nnewY = {tmp[mask]}")
					lplot = ax.plot(np.array(xdata)[mask],tmp[mask],linestyle='-', marker='o',label=names[i],ms=0.5)
				ax.set_title('Daily deaths per milion of population',size=20)
	#			ax.set_xticks(years_idx,use_names,size=15)
				ax.set_xlabel('Date',size=18)
				ax.set_ylabel('New deaths per milion',size=18)
				ax.set(ylim=[ymin, ymax])
				ax.set_xlim(dates[0],dates[-1]+120)
				ax.set_yticks(np.array(yval), ylab,size=12)
				t=ax.text(dates[-50], yval[-1]*0.75 ,f"{xs[frame]}", size=25, va="center", ha="left",)
				
				# you can not use grid:
				ax.grid()  
				ax.grid(axis="both",which='major', color='white', linewidth=1.2)
				ax.grid(axis="both",which='minor', color='white', linewidth=0.5)
				ax.minorticks_on()
				# Now hide the minor ticks (but leave the gridlines).
				ax.xaxis.set_major_locator(mdates.YearLocator())
				ax.xaxis.set_minor_locator(mdates.MonthLocator(bymonth=[3,6,9,12]))
				ax.xaxis.set_major_formatter(mdates.DateFormatter('\n%Y'))
				ax.xaxis.set_minor_formatter(mdates.DateFormatter('%b'))

				return (lplot,t)
				
			ani = animation.FuncAnimation(fig=fig, func=update, frames=len(dates), interval=100,init_func=init)
			plt.show()


		if args[1]==2:
			fig.update_layout(
				width=1000,
				height=580)
			fig.write_html(f'{args[0]}', auto_open=False)
			print(args[0])
		elif args[1]==1:
			fig.update_layout(
				width=1500,
				height=1000)
			fig.write_image(f"{args[0]}")
		elif args[1]==3:
			writergif = animation.PillowWriter(fps=13)
			ani.save(args[0], writer=writergif)
		else:
	#		fig.write_html(f'{args[1]}', auto_open=True)
			fig.show()	



if __name__ == "__main__":
	main()