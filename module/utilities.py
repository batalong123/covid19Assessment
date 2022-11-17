import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st 
import random

def plot_setting():
	# Set Matplotlib defaults
	plt.style.use("seaborn-whitegrid")
	plt.rc("figure", autolayout=True, figsize=(11, 4))
	plt.rc(
	    "axes",
	    labelweight="bold",
	    labelsize="large",
	    titleweight="bold",
	    titlesize=16,
	    titlepad=10)
	plt.rc(
	    "font",
	    family = 'DejaVu Sans',
	    weight = 'bold')

	plot_params = dict(
	    color="0.75",
	    style=".-",
	    markeredgecolor="0.25",
	    markerfacecolor="0.25",)

@st.cache(allow_output_mutation=True)
def global_data(raw_conf, raw_deaths):
    """
        Put all together raw_conf and raw_death in the same dataframe global_covid19.
    """
    region = []
    cases = []
    time = []
    latitude = []
    longitude = []
    fat = []
    for u in list(raw_conf.columns)[4:]:
        time.append([u for i in range(raw_conf.shape[0])])
        region.append(list(raw_conf['Country/Region']))
        cases.append(list(raw_conf[u]))

        latitude.append(list(raw_conf.Lat))
        longitude.append(list(raw_conf.Long))
        fat.append(list(raw_deaths[u]))
        
    global_covid19 = pd.DataFrame()
    global_covid19['date'] = np.concatenate(time)
    global_covid19['country'] = np.concatenate(region)
    global_covid19['Lat'] = np.concatenate(latitude)
    global_covid19['Long'] = np.concatenate(longitude)
    global_covid19['cases'] = np.concatenate(cases)
    global_covid19['fatalities'] = np.concatenate(fat)
    return global_covid19

@st.cache(allow_output_mutation=True)
def rename(data):
    
    replace = ['Dem. Rep. Congo',  'Congo','Central African Rep.',
          'Eq. Guinea','eSwatini','Bosnia and Herz.', 'S. Sudan', 'Dominican Rep.', 
          'United States of America', 'South Korea', "Côte d'Ivoire"]

    name = ['Congo (Kinshasa)',  'Congo (Brazzaville)', 
        'Central African Republic', 'Equatorial Guinea', 'Eswatini', 
            'Bosnia and Herzegovina', 'South Sudan',
       'Dominica','US', 'Korea, South',"Cote d'Ivoire"]
    data = data.replace(to_replace=name, value=replace)
    return data

@st.cache(allow_output_mutation=True)
def detection_variant_mutation(data=None):
    """ 
        This function detecte variant and mutation 
        data: list variant and mutation
        
        return list variant and list mutation
    """
    isvariant = []
    ismutation = []
    for u in data:
        
        words = u.split('.')
        l1 = words[0]
        l2 = words[-1]
        cond1 = ('S' in words or l1=='S' or l2[0]=='S')
        cond2 = (l2[-1].isdigit() or l2[-1] =='-')
        cond3 = (l2[-2].isdigit())
        
        if  cond1 and cond2  and cond3 :
            ismutation.append(u)
        else:
            isvariant.append(u)
            
    return isvariant, ismutation

def plot_barh(data=None, name=None):
    """ 
        This function plot horizontal bar
    """
    fig, ax = plt.subplots(figsize=(10, 10))
    data.plot(ax=ax, edgecolor='black', color='red', linewidth=1.5, kind='barh')
    for i, u in enumerate(data):
        ax.annotate(str(u), xy=(u, i), xytext=(1, i), bbox = dict(boxstyle="round", fc="0.8",
                                                                   color='black'))
    ax.set_title(f'{name} ranking.')
    ax.set_xlabel('number of country')
    ax.set_ylabel(f'{name}')
    ax.legend(frameon=True, shadow=True, fancybox=True, loc='best');
    st.pyplot(fig)

@st.cache(allow_output_mutation=True)
def rename_country(data):
    """ 
        This function rename country
    """
    
    replace = ['Czech Republic', 'Republic of the Congo','USA','Eswatini','Central African Republic',
          'South Sudan', 'Equatorial Guinea', 'Democratic Republic of the Congo', 'Bosnia and Herzegovina',
          'Dominican Republic','Dominica']
    values= ['Czechia', 'Congo', 'United States of America', 'eSwatini', 'Central African Rep.',
         'S. Sudan', 'Eq. Guinea', 'Dem. Rep. Congo', 'Bosnia and Herz.', 'Dominican Rep.','Dominican Rep.']
    
    data = data.replace(to_replace=replace, value=values)
    data['first_seq'] = pd.to_datetime(data['first_seq'])
    data['last_seq']  = pd.to_datetime(data['last_seq'])
    return data

@st.cache(allow_output_mutation=True)
def map_plotting(data: pd.DataFrame, color:list, figsize:(int,int),
                 column:str, cols:list):
    """
        This function plot on map each predominant variant or mutation
        
        data: pandas dataframe
        color: color list
        name: title
        figsize: size of figure
        layout: layout
        column: the column that we plot
    """

    fig, ax = plt.subplots(figsize=figsize)
    cd = data[data.variant == cols]
    cd.plot(cmap=random.choice(color), 
                    column=column,
                    legend=True,
                    ax=ax,
                    scheme='quantiles', k=5,
                    edgecolor='black', linewidth=1.5, 
                    legend_kwds={'loc':'lower left', 'frameon':True, 'shadow':True,
                                'markerscale':1, 'fancybox':True, 'edgecolor':'black',  
                                'title_fontsize':12,
                                 'fontsize':12})
    ax.axis('off')
    ax.set_title(f'{cols} sequence map', fontsize=20, fontweight='bold');
    return fig

def mapping(data: pd.DataFrame, color:list, figsize:(int,int),
                 column:str, cols:list):
    """
        This function plot on map each predominant variant or mutation
        
        data: pandas dataframe
        color: color list
        name: title
        figsize: size of figure
        layout: layout
        column: the column that we plot
    """

    fig, ax = plt.subplots(figsize=figsize)
    cd = data[data.variant == cols]
    cd.plot(cmap=random.choice(color), 
                    column=column,
                    legend=True,
                    ax=ax,
                    scheme='quantiles', k=5,
                    edgecolor='black', linewidth=1.5, 
                    legend_kwds={'loc':'lower left', 'frameon':True, 'shadow':True,
                                'markerscale':1, 'fancybox':True, 'edgecolor':'black',  
                                'title_fontsize':12,
                                 'fontsize':12})
    ax.axis('off')
    ax.set_title(f'{cols} lifetime (in days) map', fontsize=20, fontweight='bold');
    return fig



def plotting(data: pd.DataFrame, name:str, figsize:(int, int), layout:(int, int), dpi:int, cols:list):
    """
        This function plot on map each predominant variant or mutation
        
        data: pandas dataframe
        name: title
        figsize: size of figure
        layout: layout
        cols: list
    """

    fig = plt.figure(figsize=figsize, dpi=dpi)
    fig.subplots_adjust(wspace=0.2, hspace=0.2)
    
    for i, u in enumerate(cols):
        ax = fig.add_subplot(layout[0], layout[1], i+1)
        cd = data[data.variant == u]
        
        cd['lifetime'].plot.box(ax=ax)
        ax.set_title(u)
        ax.set_ylabel('days')
    plt.suptitle(f'Predominant {name} lifetime', fontsize=20, fontweight='bold', y=1.1);


