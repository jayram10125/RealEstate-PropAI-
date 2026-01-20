import streamlit as st
import pickle
import pandas as pd
st.set_page_config(page_title="Recommend Appartments", page_icon="🏢")
st.title("Select Location and Radius")

## hum user se 'landmark(location ) lenge and disteance lenge as input and the 
# uss distance ke andar me se  sare  appartment dikhayenge[called location based filtering] and then user #kisi ek appartment ko select karega
# uske basis pe 5 similar appartment dikhayenge'

location_df = pickle.load(open("dataset/location_distance.pkl", "rb"))

cosine_sim1 = pickle.load(open("dataset/cosine_sim1.pkl", "rb"))
cosine_sim2 = pickle.load(open("dataset/cosine_sim2.pkl", "rb"))
cosine_sim3 = pickle.load(open("dataset/cosine_sim3.pkl", "rb"))

def recommend_properties_with_scores(property_name, top_n=5):
    cosine_sim_matrix = 0.5 * cosine_sim1 + 0.8 * cosine_sim2 + 1 * cosine_sim3
    # cosine_sim_matrix = cosine_sim3

    # Get the similarity scores for the property using its name as the index
    sim_scores = list(enumerate(cosine_sim_matrix[location_df.index.get_loc(property_name)]))

    # Sort properties based on the similarity scores
    sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the indices and scores of the top_n most similar properties
    top_indices = [i[0] for i in sorted_scores[1:top_n + 1]]
    top_scores = [i[1] for i in sorted_scores[1:top_n + 1]]

    # Retrieve the names of the top properties using the indices
    top_properties = location_df.index[top_indices].tolist()

    # Create a dataframe with the results
    recommendations_df = pd.DataFrame({
        'PropertyName': top_properties,
        'SimilarityScore': top_scores
    })

    return recommendations_df

selected_location=st.selectbox('Location', sorted(location_df.columns.tolist()))

radius=st.number_input('Radius (in km)')

if st.button('Search'):
    result_ser=location_df[location_df[selected_location] < radius*1000][selected_location].sort_values().to_dict()

    appartment=[]
    distance=[]
    for key,value in result_ser.items():
        st.text(str(key)+" "+str(round(value/1000))+" kms")


st.title("Recommend Appartment")
selected_appartment=st.selectbox('Select Appartment to get Similar Listings',sorted(location_df.index.tolist()))
if st.button('Recommend'):
    recommendation_df = recommend_properties_with_scores(selected_appartment)

    st.dataframe(recommendation_df)