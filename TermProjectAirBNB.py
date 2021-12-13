"""
Name: Jose Ordaz
CS230: Section XXX
Data: Which data set you used
URL: 
Description:
This program ... (a few sentences about your program and the queries and charts)

"""

import streamlit as st
#from streamlit_folium import folium_static
#import folium
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np

def barchart(x,y):
    plt.bar(x, y, color="red")
    plt.ylabel("Price")
    plt.xlabel("Minimum nights")
    plt.title(f"Correlation price and minimum nights")
    plt.bar(x, y, align="center", alpha=0.5)
    plt.show()
    return plt

st.set_page_config(page_title='AirBNB.com',
                   layout="wide",
                   page_icon="https://visualpharm.com/assets/422/Cool-595b40b75ba036ed117d7b9b.svg")

header_container = st.container()
data_container = st.container()
subheader_container = st.container()


with header_container:
    st.image('https://upload.wikimedia.org/wikipedia/commons/6/69/Airbnb_Logo_B%C3%A9lo.svg', width=400)
    st.title('Find a place to stay')
    st.header("📍London")
    st.write("This app is awesome!")
    st.write("")

with data_container:
    st.subheader('Feed me only with the specified .csv file :)')
    uploaded_file = st.file_uploader('Please upload the LondonAirBnBSep2021.csv file', type='csv')

    if uploaded_file:
        st.markdown('---')
        df = pd.read_csv(uploaded_file,
                         usecols=["name",
                                  "host_id",
                                  "host_name",
                                  "neighbourhood",
                                  "latitude",
                                  "longitude",
                                  "room_type",
                                  "price",
                                  "minimum_nights",
                                  "number_of_reviews",
                                  "reviews_per_month",
                                  "availability_365"])


        def sidebar():
            st.sidebar.title('Filters')
            neighbourhood = st.sidebar.selectbox('Neighbourhood',  (df['neighbourhood'].unique()))
            room_type = st.sidebar.selectbox('Room Type', (df['room_type'].unique()))
            price = st.sidebar.slider('Max price', 10, max(df['price']) , step=10)
            show_data = st.sidebar.checkbox("Show Data")
            map = st.sidebar.checkbox("Show Map")
            show_analysis = st.sidebar.checkbox("Show Analysis")
            filt_df = df[(df['neighbourhood'] == neighbourhood) &
                         (df['room_type'] == room_type) &
                         (df["price"].between(0, price))]

            if show_data:
                st.write(filt_df)

            if map:
                st.subheader(f'Showing {room_type.lower()}(s) in {neighbourhood} for less than ${price}')
                world = folium.Map(
                    zoom_start=15,
                    location=[filt_df["latitude"].mean(), filt_df["longitude"].mean()])

                folium.TileLayer('stamentoner').add_to(world)

                # filt_df.apply(lambda column: folium.Marker(location=[column["latitude"],
                # column["longitude"]], icon=folium.Icon(color="red", icon="home", prefix='fa')).add_to(world), axis=1)

                for lat, lon, name, price in zip(filt_df["latitude"].tolist(), filt_df["longitude"].tolist(),
                                                 filt_df["name"].tolist(), filt_df["price"].tolist()):
                    folium.Marker(location=[lat, lon],
                                  popup=folium.Popup(f"""{name} <br> Price per night = ${price}.00 <br.""",
                                  max_width=len(f"name= {name}")*20),
                                  icon=folium.Icon(color="red", icon="home", prefix='fa')).add_to(world)
                folium_static(world)

                # while map:
                #     try:
                #         folium_static(world)
                #         break
                #     except ValueError:g
                #         st.error("Price cannot be 0")

            if show_analysis:
                price = filt_df["price"]
                count = len(price)
                mean = np.mean(price)
                minimum = np.min(price)
                std = np.std(price)
                maximum = np.max(price)

                stats_rows = [
                    ["Count:", f"{count:5.2f}"],
                    ["Mean:", f"${mean:5.2f}"],
                    ["Standard Deviation:", f"${std:5.2f}"],
                    ["Minimum:", f"${minimum:5.2f}"],
                    ["Maximum:", f"${maximum:5.2f}"]]

                col_width = max(len(str(word)) for row in stats_rows for word in row) + 5

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write("")
                    st.write("")
                    st.write("")
                    st.subheader("Statistical analysis")
                    for row in stats_rows:
                        row_words = []
                        for word in row:
                            row_words.append(str(word).ljust(col_width))

                        st.text("".join(row_words))

                with col2:
                    fig = px.scatter(filt_df,
                                     x="number_of_reviews",
                                     y="price",
                                     color='price' ,
                                     title= f"Correlation between price and number of reviews in {neighbourhood}")
                    st.plotly_chart(fig)


                col4, col5, col6 = st.columns(3)

                with col4:
                    y = filt_df["price"].tolist()
                    x = (filt_df["minimum_nights"].tolist())
                    st.set_option('deprecation.showPyplotGlobalUse', False)
                    st.pyplot(barchart(x, y))



        sidebar()

        col7, col8 = st.columns(2)
        with col7:
            user_name = st.text_input("Please write down your name", 'John Doe')
            st.write("Thanks,", user_name, " for using this app!")
        with col8:
            st.write("")
            st.write("")
            if st.button("Assistance"):
                st.write ("If you want to be contacted for assistance with your reservation click here")
                phone = st.text_input("Please write down your phone", '999-999-9999')
                if phone:
                    st.write(f"Thanks, {user_name}! One of our agents will call you soon!")

            else:
                st.write("Click me")

