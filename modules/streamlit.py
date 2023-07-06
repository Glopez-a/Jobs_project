import streamlit as st
import pandas as pd
from modules import scrapping as scrp


def streamlit():
    st.title('Companies information!')
    df = pd.read_csv("./data/companies_info.csv", index_col=None)
    st.dataframe(df[['Name','size','revenue','founded','Overall','Culture','Diversidad','Conciliacion','Managers','Sueldos','Oportunidades','Recomendar a un amigo','CEO puntuación','Imagen de empresa','industry']], use_container_width=True)
    if st.button("CLICK AQUÍ PARA ACTUALIZAR LA INFORMACIÓN! :sunglasses:"):
        scrp.search_info(8000)