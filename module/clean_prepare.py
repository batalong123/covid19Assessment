import pandas as pd 
import numpy as np 
import streamlit as st
import time
from module.utilities import global_data, rename

file1 = 'data/RAW_global_deaths.csv'
file2 = 'data/RAW_global_confirmed_cases.csv'
file3 = 'data/RAW_us_confirmed_cases.csv'
file4 = 'data/RAW_us_deaths.csv'
file5 = 'data/variants.csv'
file6 = 'data/CONVENIENT_global_metadata.csv'

@st.cache(allow_output_mutation=True)
def load_global_data():
    raw_conf = pd.read_csv(file2)
    raw_death = pd.read_csv(file1)
    data_covid19 = global_data(raw_conf, raw_death)
    data_covid19 = rename(data_covid19)    
    return data_covid19

@st.cache(allow_output_mutation=True)
def load_variant():
    return pd.read_csv(file5)

