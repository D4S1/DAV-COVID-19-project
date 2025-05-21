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
	args = parse_args("plot22")
	if args:



		col_name= 'Daily hospital occupancy per million'
		ylabel='Daily number of hospitalised people (per M)'
		ptitle='Daily number of hospitalised people per milion of citizens'
		data=pd.read_csv(args[15])
#		print(data.columns)
#		print(data[["country", 'Daily hospital occupancy per million','Daily hospital occupancy']])
		ymin=data[col_name].min()
		ymax=data[col_name].max()
		if args[1]<3 :
			
			fig = go.Figure()
			for i,c in enumerate(["Australia","Poland"]):
				if i:
					col = 'rgb(250,0,0)'
				else:
					col = 'rgb(0,100,0)'

				tmp = data.loc[data["country"]==c]
				fig.add_trace(go.Scatter(x=tmp["date"], y=tmp[col_name],
						mode='lines',
						name=c,
						line=dict(color=col,),
				))


			# Add waves of COVID
			d=10
			"""
			fig.add_vline(x='2020-11-1', 
					showlegend=False,
					line=dict(width=1,color='rgb(0,0,250)',dash='dash'))
			"""
			fig.add_vline(x='2021-6-16', 
					showlegend=False,
					line=dict(width=1,color='rgb(0,0,250)',dash='dash'))
			fig.add_vline(x='2021-12-14', 
					showlegend=False,
					line=dict(width=1,color='rgb(0,0,250)',dash='dash'))
			fig.add_vline(x='2023-12-14', 
					showlegend=False,
					line=dict(width=1,color='rgb(0,0,250)',dash='dash'))
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
			fig.add_trace(go.Scatter(x=['2021-12-14','2021-12-14'], y=[ymin-d,ymax+d],
					mode='lines',
					hovertext='End of Delta Wave\nStart of Omicron Wave',
					showlegend=False,
					line=dict(width=1,color='rgb(0,0,250)',dash='dash')))
			fig.add_trace(go.Scatter(x=['2023-12-14','2023-12-14'], y=[ymin-d,ymax+d],
					mode='lines',
					hovertext='End of Omicron Wave',
					showlegend=False,
					line=dict(width=1,color='rgb(0,0,250)',dash='dash')))
			"""
			## add retrangulars 
			fig.add_vrect(x0 = '2021-6-16',x1 = '2021-12-14',  
					annotation_text="Delta Wave",annotation_position="top right",
					fillcolor="blue", opacity=0.25, line_width=0,
					annotation=dict(font_size=20  ), #, font_family="Times New Roman")
					)
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
					title=dict(text=ylabel),
					tickfont = dict(size=15),
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
					text=ptitle,
					font=dict(size=30),
					x=0.5,
					xanchor='center',
				),
	
			)

		else:


			dataAU = data.loc[data["country"]=="Australia",["date",col_name]].rename(columns = {col_name:"Australia"})
			dataPL = data.loc[data["country"]=="Poland",["date",col_name]].rename(columns = {col_name:"Poland"})

			data = pd.merge(dataAU, dataPL, on="date",how="outer")
			values=[data["Australia"].values,data["Poland"].values]
			names=["Australia","Poland"]
			code = ["AUS","POL"]



			dates=sorted(list(set(data["date"].copy().values)))
			xs =sorted(list(set(data["date"].copy().values)))
			for d in range(len(dates)):
				dates[d] = mdates.datestr2num(dates[d])
				xs[d]=str(xs[d])
			xdata = []
			ydata=[[],[]]
			xmask=[[],[]]
			omi_w_start = mdates.datestr2num('2021-12-14')
			omi_w_end = mdates.datestr2num('2023-12-14')
			delta_w_start = mdates.datestr2num('2021-6-16')

#			print(f"number of steps: {len(dates)}\nshape of values:\t{values[0].shape}\t{values[1].shape}\n\nymin = {ymin}\tymax = {ymax}")
			sns.set_theme(style="darkgrid")
			fig, ax = plt.subplots(figsize=(10,7.5))   


			lplot = ax.plot(np.array(dates[0]),np.array([[0],[0]]).T,label=names)
			fig.legend(bbox_to_anchor=(0.32,0.88),title="Countries",fontsize=15,title_fontsize=18) # 
			ymin=ymin-1e3
			ymax=ymax*1.1
			yval=[]
			ylab=["0"]
			xlast=[0 for x in range(len(ydata))]
			ylast=[0 for x in range(len(ydata))]
			for i in range(8):
				yval.append(i*5000)
				if i:
					ylab.append(f"{i*5}k")

			def init():
				ax.set_ylim(ymin, ymax)
				ax.set_xlim(dates[0],dates[-1]+60)
				ax.set_xlabel('Date',size=18)
				ax.set_ylabel(ylabel,size=18)
				xlast=[0 for x in range(len(ydata))]
				ylast=[0 for x in range(len(ydata))]
				del xdata[:]
				for i in range(len(ydata)):
					del ydata[i][:]
					del xmask[i][:]
				t = ax.text(dates[65], yval[-1]  ,xs[0], size=30, va="center", ha="center",)
				return lplot,t

			def update(frame):
				ax.cla()

				xdata.append(dates[frame])

				
	#			print(ylast)
				for i in range(len(ydata)):
					ydata[i].append(values[i][frame])
	#				print(ydata)

					if not np.isnan(ydata[i][-1]):
	#					print( ydata[i][-1] )
						ylast[i]=ydata[i][-1]
						xlast[i]=xdata[-1]
						xmask[i].append(True)
					else:
						xmask[i].append(False)
					y=ylast[i]
					x=xlast[i]
					if x and y:

						ax.text(x+0.5, y ,code[i], size=15, va="center", ha="left")

	#			print(f"x = {xdata},\n y ={ydata},\nmask = {xmask}")
				ax.text((delta_w_start+omi_w_start)/2, yval[-1] ,f"Delta\nWave", size=15, va="center", ha="center",)
				ax.text((omi_w_end+omi_w_start)/2, yval[-1] ,f"Omicron Wave", size=15, va="center", ha="center",)
				lplot1 = ax.plot(np.array(xdata)[np.array(xmask[0])],np.array(ydata[0])[np.array(xmask[0])].T,"-o",label=names[0],color="C0",ms = 1)
				lplot2 = ax.plot(np.array(xdata)[np.array(xmask[1])],np.array(ydata[1])[np.array(xmask[1])].T,"-o",label=names[1],color="C1",ms = 1)
				wplot1 = ax.fill_betweenx([ymin,ymax],delta_w_start,omi_w_start,alpha=0.3,color="tab:green")
				wplot2 = ax.fill_betweenx([ymin,ymax],omi_w_start,omi_w_end,alpha=0.3,color='tab:olive')
				ax.set_title(ptitle,size=20)
	#			ax.set_xticks(years_idx,use_names,size=15)
				ax.set_xlabel('Date',size=18)
				ax.set_ylabel(ylabel,size=18)
				ax.set(ylim=[ymin, ymax])
				ax.set_xlim(dates[0],dates[-1]+120)
				ax.set_yticks(np.array(yval), ylab,size=12)
				t=ax.text(dates[10], yval[-3] ,f"{xs[frame]}", size=25, va="center", ha="left",)
				
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

				return (lplot1,lplot2,t)
				
			ani = animation.FuncAnimation(fig=fig, func=update, frames=len(dates), interval=100,init_func=init)
			plt.show()
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
			writergif = animation.PillowWriter(fps=13)
			ani.save(args[0], writer=writergif)
		else:
	#		fig.write_html(f'{args[1]}', auto_open=True)
			fig.show()	



if __name__ == "__main__":
	main()
