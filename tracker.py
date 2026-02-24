import streamlit as st
import pandas as pd
import pydeck as pdk

st.set_page_config(layout="wide")

if "locations" not in st.session_state:
    st.session_state.locations = []

st.title("🗺 Live Family Tracker")

col1, col2 = st.columns(2)

with col1:
    name = st.text_input("Enter Name")
    latitude = st.number_input("Latitude", value=17.385044)
    longitude = st.number_input("Longitude", value=78.486671)

    if st.button("Share Location"):
        st.session_state.locations.append({
            "name": name,
            "latitude": latitude,
            "longitude": longitude
        })
        st.success("Location Added")

with col2:
    if st.session_state.locations:
        df = pd.DataFrame(st.session_state.locations)
        st.dataframe(df)

if st.session_state.locations:

    df = pd.DataFrame(st.session_state.locations)

    center_lat = df["latitude"].mean()
    center_lon = df["longitude"].mean()

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position=["longitude", "latitude"],
        get_fill_color=[0, 200, 255, 200],
        get_radius=400,
        pickable=True,
    )

    view_state = pdk.ViewState(
        latitude=center_lat,
        longitude=center_lon,
        zoom=14,
    )

    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"text": "{name}"}
    )

    st.pydeck_chart(deck)