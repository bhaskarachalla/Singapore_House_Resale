import streamlit as st
from streamlit_option_menu import option_menu
import json
import requests
import pandas as pd
from geopy.distance import geodesic
import statistics
import numpy as np
import pickle

# -------------------------Reading the data on Lat and Long of all the MRT Stations in Singapore------------------------
data1 = pd.read_csv('combined.csv')
data = pd.read_csv('mrt.csv')
#data = pd.read_csv('C:/Users/Srinivasa Rao/OneDrive/Documents/GUVI_Projects/Singapore_House_Resale/mrt.csv')
mrt_location = pd.DataFrame(data)

data1 = pd.read_csv('combined.csv')
#data1 = pd.read_csv('C:/Users/Srinivasa Rao/OneDrive/Documents/GUVI_Projects/Singapore_House_Resale/combined.csv')
drop_box = pd.DataFrame(data1)

# -------------------------------This is the configuration page for our Streamlit Application---------------------------
st.set_page_config(
    page_title="Singapore Resale Flat Prices Prediction",
    page_icon="house",
    layout="wide"
)

#---------------------------------------------------This is the sidebar navigation--------------------------------------
with st.sidebar:
    selected = option_menu("Main Menu", ["About Project", "Predictions"],
                           icons=["house", "gear"],
                           styles={"nav-link": {"font": "sans serif", "font-size": "20px", "text-align": "centre"},
                                   "nav-link-selected": {"font": "sans serif", "background-color": "#0072b1"},
                                   "icon": {"font-size": "20px"}
                                   }
                           )

# -----------------------------------------------About Project Section--------------------------------------------------
if selected == "About Project":
    st.markdown("# :blue[Singapore Resale Flat Prices Prediction]")
    st.markdown('<div style="height: 50px;"></div>', unsafe_allow_html=True)
    st.markdown("### :blue[Technologies :] Python, Pandas, Numpy, Scikit-Learn, Streamlit, Python scripting, "
                "Machine Learning, Data Preprocessing, Visualization, EDA, Model Building, Data Wrangling, "
                "Model Deployment")
    st.markdown("### :blue[Overview :] This project aims to construct a machine learning model and implement "
                "it as a user-friendly online application in order to provide accurate predictions about the "
                "resale values of apartments in Singapore. This prediction model will be based on past transactions "
                "involving resale flats, and its goal is to aid both future buyers and sellers in evaluating the "
                "worth of a flat after it has been previously resold. Resale prices are influenced by a wide variety "
                "of criteria, including location, the kind of apartment, the total square footage, and the length "
                "of the lease. The provision of customers with an expected resale price based on these criteria is "
                "one of the ways in which a predictive model may assist in the overcoming of these obstacles.")
    st.markdown("### :blue[Domain :] Real Estate")

# ------------------------------------------------Predictions Section---------------------------------------------------
if selected == "Predictions":
    st.markdown("# :blue[Predicting Results based on Trained Models]")
    st.markdown("### :orange[Predicting Resale Price (Regression Task) (Accuracy: 84%)]")

    with st.form("form1"):
        # -----New Data inputs from the user for predicting the resale price-----
        street_name = st.selectbox('Select the street',drop_box['street_name'].unique())
        block = st.selectbox("Select block",drop_box['blk_no'].unique())
        floor_area_sqm = st.selectbox('Floor Area (Per Square Meter)', drop_box['floor_area_sqm'].unique())
        lease_commence_date = st.selectbox('Lease Commence Date',drop_box['lease_commence_date'].unique())
        storey_range = st.selectbox("Storey Range (Format: 'Value1' TO 'Value2')",drop_box['storey_range'].unique())

        # -----Submit Button for PREDICT RESALE PRICE-----
        submit_button = st.form_submit_button(label="PREDICT RESALE PRICE")

    if submit_button:
        try:
            with open(r"model.pkl", 'rb') as file:
                loaded_model = pickle.load(file)
            with open(r'scaler.pkl', 'rb') as f:
                scaler_loaded = pickle.load(f)

            # -----Calculating lease_remain_years using lease_commence_date-----
            lease_remain_years = 99 - (2024 - lease_commence_date)

            # -----Calculating median of storey_range to make our calculations quite comfortable-----
            split_list = storey_range.split(' TO ')
            float_list = [float(i) for i in split_list]
            storey_median = statistics.median(float_list)

            # -----Getting the address by joining the block number and the street name-----
            address = block + " " + street_name
            query_address = address
            query_string = f'https://photon.komoot.io/api/?q={query_address}'
            resp = requests.get(query_string)

            # -----Using OpenMap API getting the latitude and longitude location of that address-----
            origin = []
            data_geo_location = json.loads(resp.content)
            if len(data_geo_location['features']) != 0:
                latitude = data_geo_location['features'][0]['geometry']['coordinates'][1]
                longitude = data_geo_location['features'][0]['geometry']['coordinates'][0]
                origin.append((latitude, longitude))

                # -----Appending the Latitudes and Longitudes of the MRT Stations-----
                # Latitudes and Longitudes are been appended in the form of a tuple to that list
                mrt_lat = mrt_location['latitude']
                mrt_long = mrt_location['longitude']
                list_of_mrt_coordinates = []
                for lat, long in zip(mrt_lat, mrt_long):
                    list_of_mrt_coordinates.append((lat, long))

                # -----Getting distance to nearest MRT Stations (Mass Rapid Transit System)-----
                list_of_dist_mrt = []
                for destination in range(len(list_of_mrt_coordinates)):
                    list_of_dist_mrt.append(geodesic(origin[0], list_of_mrt_coordinates[destination]).meters)
                min_dist_mrt = min(list_of_dist_mrt)

                # -----Getting distance from CBD (Central Business District)-----
                cbd_dist = geodesic(origin[0], (1.2830, 103.8513)).meters  # CBD coordinates

                # -----Sending the user-entered values for prediction to our model-----
                new_sample = np.array(
                    [[cbd_dist, min_dist_mrt, np.log(floor_area_sqm), lease_remain_years, np.log(storey_median)]])
                new_sample_scaled = scaler_loaded.transform(new_sample)
                new_pred = loaded_model.predict(new_sample_scaled)[0]
                st.write('## :green[Predicted resale price:] ', np.exp(new_pred))
            else:
                st.write("Could not find the geographical coordinates for the given address.")

        except Exception as e:
            st.write("An error occurred:", e)
            st.write("Enter the above values to get the predicted resale price of the flat")

