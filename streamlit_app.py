import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk


st.title("Recogidas de Uber en NYC")
st.markdown(
    """
    Una aplicación que muestra las recogidas de Uber en Nueva York distribuidas geográficamente.
    Datos recogidos durante el mes de septiembre de 2014.
    """
)

# LOADING DATA
DATE_TIME = "date/time"
DATA_URL = "http://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz"


@st.cache_data(persist=True)
def load_data(number_rows):
    df = pd.read_csv(DATA_URL, nrows=number_rows)
    df.rename(str.lower, axis="columns", inplace=True)
    df[DATE_TIME] = pd.to_datetime(df[DATE_TIME])
    return df


data = load_data(100000)
midpoint = (np.average(data["lat"]), np.average(data["lon"]))

hora = st.sidebar.number_input('Hora:', 0, 23, 6)
data = data[data[DATE_TIME].dt.hour == hora]

st.write('## Datos geoespaciales a las %sh' % hora)

st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=pdk.ViewState(
        latitude=midpoint[0],
        longitude=midpoint[1],
        zoom=11,
        pitch=50
    ),
    layers=[
        pdk.Layer(
           'HexagonLayer',
           data=data,
           get_position='[lon, lat]',
           radius=100,
           elevation_scale=4,
           elevation_range=[0, 1000],
           pickable=True,
           extruded=True
        )
    ]
))

show_data = st.sidebar.checkbox('Mostrar tabla de datos')

if show_data:
    st.write(data)
