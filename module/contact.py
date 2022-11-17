import streamlit as st

def contact_me():

	doc = """
	Covid-19 data are extracted from Kaggle Data Science Community provided by [Johns Hopkins University](https://www.kaggle.com/datasets/antgoldbloom/covid19-data-from-john-hopkins-university)
	and coVariants data is downloaded from website https://covariants.org/

	If you want to contact me for any suggestions, take this email link: [lumierebatalong@gmail.com](lumierebatalong@gmail.com)

	Thank you for using this application.

	Author: **Massock Batalong M.B.**
	"""

	st.title("# Contact me.")
	st.markdown(doc)
	st.balloons()