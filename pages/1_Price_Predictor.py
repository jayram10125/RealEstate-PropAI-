import streamlit as st
import pickle
import numpy as np
import pandas as pd

st.set_page_config(page_title="Plotting Demo", page_icon="📈")
st.title("Price Predictor")
#property_type	sector	bedRoom	bathroom	balcony	agePossession	
# built_up_area	servant room	store room	furnishing_type	luxury_category	
# floor_category

with open("df.pkl", "rb") as file:
    df = pickle.load(file)

with open("pipeline.pkl", "rb") as file:
    pipeline = pickle.load(file)


st.header('Enter your inputs to predict the price')
# property_type

property_type = st.selectbox('Property Type', ['flat','house'])

# Sector
sector = st.selectbox('Sector', sorted(df['sector'].unique().tolist()))

# bedRoom
bedRoom = float(st.selectbox('Number of Bedrooms', sorted(df['bedRoom'].unique().tolist())))
# bathroom
bathroom = float(st.selectbox('Number of Bathrooms', sorted(df['bathroom'].unique().tolist())))

#balcony
balcony = st.selectbox('Number of Balconies', sorted(df['balcony'].unique().tolist()))
#agePossession
property_age = st.selectbox('Age of property', sorted(df['agePossession'].unique().tolist()))
# built_up_area
built_up_area = float(st.number_input('Built-up Area (in sqft)'))
# servant room
servant_room = st.selectbox('Servant Rooms', ('Yes','No'))
if servant_room == 'Yes':
    servant_room = 1.0
else:
    servant_room = 0.0

# store room
store_room = st.selectbox('Store Rooms', ('Yes','No'))
if store_room == 'Yes': 
    store_room = 1.0
else:
    store_room = 0.0

# furnishing_type
furnishing_type = st.selectbox('Furnishing Type', sorted(df['furnishing_type'].unique().tolist()))
# luxury_category
luxury_category = st.selectbox('Luxury Category', sorted(df['luxury_category'].unique().tolist()))
#floor_category
floor_category = st.selectbox('floor Category', sorted(df['floor_category'].unique().tolist()))

if st.button('Predict Price'):
    # form a data frame
    data = [[property_type,sector,bedRoom,bathroom,balcony,property_age,built_up_area,servant_room,
             store_room,furnishing_type,luxury_category,floor_category]]
    columns = ['property_type', 'sector', 'bedRoom', 'bathroom', 'balcony',
       'agePossession', 'built_up_area', 'servant room', 'store room',
       'furnishing_type', 'luxury_category', 'floor_category']

    one_df = pd.DataFrame(data, columns=columns)

    #st.dataframe(one_df)
    #predict

    base_price=np.expm1(pipeline.predict(one_df))[0]
    low=base_price-0.25
    high=base_price+0.25

    # display

    st.text(f"The predicted price is between {low:.2f} Cr to {high:.2f} Cr")