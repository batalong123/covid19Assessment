from module.utilities import plot_setting
from module.clean_prepare import load_global_data
import geopandas as gpd
import mapclassify as mpc
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st    


@st.cache(allow_output_mutation=True)
def geo_data_transforms():

	data = load_global_data()
	end_date = data.date.unique()[-1] #today
	yesterday = data.date.unique()[-2] #yesterday

	#geospatial
	geoCovid = gpd.GeoDataFrame(data, 
                            geometry=gpd.points_from_xy(data.Long,
                            data.Lat))
	geoCovid.crs = 'epsg:4326'

	world_path_file = gpd.datasets.get_path('naturalearth_lowres') # upload natural data map
	world = gpd.read_file(world_path_file)

	today_data_covid19 = data[data.date == end_date]
	grouped_data_covid19 = today_data_covid19.groupby('country')[['cases', \
	'fatalities']].agg('sum').reset_index()

	geo_merged_covid19 = world.merge(grouped_data_covid19[['country','cases','fatalities']], 
                         left_on='name', right_on='country')
	return geo_merged_covid19, end_date, yesterday


def geospatial_covid19():

	plot_setting()

	geocovid19, today, yesterday = geo_data_transforms()
	continent = geocovid19.groupby(by='continent')[['cases', 'fatalities']].agg('sum')

	st.title('Covid-19 geospatial analysis')
	if st.checkbox('SARS-Cov II world map'):
		if st.checkbox('Covid19 cases map'):
			fig, ax = plt.subplots(figsize=(15,15))
			geocovid19.plot(cmap='viridis', column='cases', 
                        scheme='quantiles',
                        k=5, ax = ax,
                        legend=True, edgecolor='black', linewidth=1.5, 
                       legend_kwds={'loc':'lower left', 'frameon':True, 'shadow':True,
                                    'markerscale':1.5, 'fancybox':True, 'edgecolor':'black', 
                                   'title': 'cases range', 'title_fontsize':16, 'fontsize':14})
			ax.axis('off')
			ax.set_title(f'SARS-Cov 2 cases map for date {today}.',
				fontweight='bold', fontsize=20)
			st.pyplot(fig)
			text = """
			*This is the world map of Covid19 cases and its variants.*
			*From black (less contamination) to yellow (more contamination),*
			*we observe that Western Europe and part of Eastern Europe,*
			*North America, almost all of Oceania are highly contaminated*
			*unlike other continents such as Africa, Asia, South America.*
			"""
			st.markdown(text)

		if st.checkbox('Covid19 fatalities map'):
			fig, ax = plt.subplots(figsize=(15,15))
			geocovid19.plot(cmap='OrRd', 
                        column='fatalities',
                        legend=True,
                        scheme='quantiles', k=5,ax=ax,
                        edgecolor='black', linewidth=1.5, 
                        legend_kwds={'loc':'lower left', 'frameon':True, 'shadow':True,
                                    'markerscale':1.5, 'fancybox':True, 'edgecolor':'black', 
                                    'title': 'fatalities range', 
                                    'title_fontsize':16,
                                     'fontsize':14})
			ax.axis('off')
			ax.set_title(f'SARS-Cov 2 fatalities map for date {today}.',
				fontweight='bold', fontsize=20)
			st.pyplot(fig)
			st.markdown("""*This is the world map of Covid19 deaths and its variants.*
				*Dark red indicates countries with more deaths.*""")

	if st.checkbox('SARS-Cov II contamination by continent'):
		fig, ax = plt.subplots(figsize=(12, 5))
		continent.plot(kind='bar', subplots=True, layout=(1,2), 
               ax=ax, edgecolor='black', linewidth=1.5)
		plt.suptitle(f'SARS-Cov II by continent for date = {today}', fontsize=20, fontweight='bold', y=1.1)
		st.pyplot(fig)

	if st.checkbox('SARS-Cov II contamination by country'):
		if st.checkbox('cases video'):
			video_byte = open('videos/covid19cases.mp4', 'rb').read()
			st.video(video_byte)
			st.markdown("""
				*This is a video showing bar race of Covid19 cases for each country.*""")
		if st.checkbox('fatalities video'):
			video_byte = open('videos/covid19fatalities.mp4', 'rb').read()
			st.video(video_byte)
			st.markdown("""
				*This is a video showing bar race of Covid19 fatalities for each country.*
				""")










