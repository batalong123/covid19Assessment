import pandas as pd 
import numpy as np 
import streamlit as st
from module.utilities import rename_country, detection_variant_mutation, plot_barh, map_plotting, plotting, plot_setting, mapping
from module.clean_prepare import load_variant
import geopandas as gpd
import matplotlib.pyplot as plt  

text1 = """
This section is subdivided like follows:
- Identify variants and mutation by using Nextstrain nomenclature.
- Represent predominant variant and mutation sequence in the map.
- What is a lifetime estimation of predominant variant and mutation in each country?
"""

read2 = """
**Sequence** is to identify the order in which a set of genes or part of molecules are arranged.

We call **lifetime estimation** the duration between the first sequence date and the last sequence date that the viruses
 was detected.
"""

@st.cache(allow_output_mutation=True)
def geodata_variant(data):
	world_path_file = gpd.datasets.get_path('naturalearth_lowres') # upload natural data map
	world = gpd.read_file(world_path_file)
	geodata = world.merge(rename_country(data), left_on='name', right_on='Country')
	geodata['lifetime'] = geodata['last_seq'] - geodata['first_seq']
	geodata['lifetime'] = geodata['lifetime'].apply(lambda x: abs(x.days))
	return geodata

def plot_bar(data, name):


	fig, ax = plt.subplots(figsize=(10, 5))
	data.plot(ax=ax, edgecolor='black', color='red', linewidth=1.5, kind='bar')
	for i, u in enumerate(data.values):
	    ax.annotate(str(u[0]), xy=(i-0.5, u), xytext=(i-0.25, 1), bbox = dict(boxstyle="round", fc="0.8",
	                                                               color='black'))
	ax.set_title(f'{name}: variant and mutation lifetime (in days).')
	ax.set_xlabel('predominanr variant and mutation')
	ax.set_ylabel('lifetime (in days)')
	ax.legend(frameon=True, shadow=True, fancybox=True, loc='best');
	st.pyplot(fig)









def covid19_variant(): 

	plot_setting()
	st.title('Variants and Mutation')
	st.markdown(text1)

	data_variant = load_variant()
	data_variant['first_seq'] = pd.to_datetime(data_variant['first_seq'])
	data_variant['last_seq'] = pd.to_datetime(data_variant['last_seq'])

	list_variant, list_mutation = detection_variant_mutation(data=data_variant.variant.unique().tolist())

	variant_dataframe  = data_variant[data_variant.variant.isin(list_variant)]
	mutation_dataframe = data_variant[data_variant.variant.isin(list_mutation)]

	serie_variant  = variant_dataframe.variant.value_counts()
	serie_mutation = mutation_dataframe.variant.value_counts()

	
	st.header('Variant and mutation nomenclature')
	st.markdown("""The name of variant and mutation 
		that we use here come from [Nextstrain nomenclature](covariant.org).""")

	if st.checkbox('Variant and mutation identification'):
		read1 = f"""
		Covid-19 (SARS-Cov II) has produced **{len(list_variant)} variants** and 
		**{len(list_mutation)} mutations**. 

		> **Variant list**: {list_variant} 

		> **Mutation list**: {list_mutation}
		"""
		st.markdown(read1)

	st.header('Predominant variant and mutation')
	st.markdown("""
		We call **predominant variant and mutation** the variant and mutation that it spreads out
		 in several countries (greater than 100) in the world.""")

	if st.checkbox('Predominant variant'):
		plot_barh(data=serie_variant, name='variant')
		st.markdown("""
			*The predominant variant in this chart are those who its number of country is greater than 100.*
			""")

	if st.checkbox('Predominant mutation'):
		plot_barh(data=serie_mutation, name='mutation')
		st.markdown("""
			*We consider predominant mutation in this chart those who its number of country is greater than or equal to 150.*
			""")

	st.header('Predominant variant and mutation sequence and lifetime estimation')
	st.markdown(read2)
	geodata = geodata_variant(data_variant)

	st.subheader('Predominant variant and mutation sequence')

	
	if st.checkbox('Variant sequence map'):
		name = st.selectbox('Choose variant:', serie_variant.index.tolist()[:6], key=0)
		fig = map_plotting(data=geodata, color=['Reds', 'Blues', 'rainbow','Greens', 'hot_r','YlOrBr'],
            figsize=(15, 15), column='num_seqs', cols=name)
		st.pyplot(fig)
		st.markdown("""*This map shows a predominant variant sequence for each country*.""")


	if st.checkbox('Mutation sequence map'):
		name = st.selectbox('Choose mutation:', serie_mutation.index.tolist()[:8], key=1)
		fig = map_plotting(data=geodata, 
             color=['BuGn', 'PiYG', 'PuBu','tab20', 'Spectral', 'autumn'],
            figsize=(15, 20), column='num_seqs', cols=name)
		st.pyplot(fig)
		st.markdown("""*This map shows a predominant mutation sequence for each country*.""")

	st.subheader('Predominant variant and mutation lifetime')

	if st.checkbox('Mutation lifetime map'):
		name = st.selectbox('Choose mutation:', serie_mutation.index.tolist()[:8], key=3)
		fig = mapping(data=geodata, 
         color=['BuGn', 'PiYG', 'PuBu','tab20', 'Spectral', 'autumn'],
        figsize=(15, 20), column='lifetime', cols=name)
		st.pyplot(fig)
		st.markdown("""*This map shows a predominant mutation lifetime in days for each country*.""")

	if st.checkbox('Variant lifetime map'):
		name = st.selectbox('Choose mutation:', serie_variant.index.tolist()[:6], key=4)
		fig = mapping(data=geodata, 
         color=['Reds', 'Blues', 'rainbow','Greens', 'hot_r','YlOrBr'],
        figsize=(15, 20), column='lifetime', cols=name)
		st.pyplot(fig)
		st.markdown("""*This map shows a predominant variant lifetime in days for each country*.""")

	if st.checkbox('By country'):
		country_name = st.selectbox('Choose country', sorted(geodata.Country.unique().tolist()), key=5)
		df = geodata[geodata.Country == country_name][['variant', 'lifetime']].sort_values(by='lifetime', ascending=False)
		cols = serie_variant.index.tolist()[:6]+serie_mutation.index.tolist()[:8]
		df = df[df.variant.isin(cols)]
		df = df.set_index('variant')
		plot_bar(df, country_name)
		


		





