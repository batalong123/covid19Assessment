
import streamlit as st
import pandas as pd
import numpy as np
from module.clean_prepare import load_global_data



def welcome():

	#title
	st.title("Covid-19 pandemic: Assessment")

	#description
	text = """   
	On December 31, 2019 China precisely province of Wuhan recorded its cases
	and victims of SARS-Cov II. Other cases of Covid-19 were observed in the rest
	of the world, notably Lombardy region (Italy).

	On March 11, 2020 the World Health Organization (WHO) declared Covid-19 a
	global health crisis (Covid-19 pandemic). While the world was experiencing the
	SARS-Cov II virus, some countries detected between September and November 2020
	their first variants, namely UK (the B.1.1.7 variant), South Africa (the B. 1.351),
	US(the CAL.20C variant, Delta), etc...


	This is how 2021 became a year of “festival of SARS-Cov II variant and
	mutation” which generated several waves.

	Despite the appearance of vaccines, resistances of certain variants was
	observed. Until today, SARS-Cov II and its variants continue their journey.
	"""

	st.markdown(text, unsafe_allow_html=False)

	#load data
	covid19 = load_global_data()



	if st.checkbox('See/Hide data'):
	    st.dataframe(covid19.iloc[:, :6])

	text = """
	The data is downloaded from Johns Hopkins University.
	"""

	with st.expander("Read more."):
		st.markdown(text, unsafe_allow_html=False)
##*******************************************************************************************              




        



