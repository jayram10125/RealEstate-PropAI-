import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
from wordcloud import WordCloud 
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Mapping Demo", page_icon="🌍")

st.title("Analytics")

new_df= pd.read_csv("dataset/data_viz1.csv")

feature_text = pickle.load(open("dataset/feature_text.pkl", "rb"))

numeric_columns = ['price', 'price_per_sqft', 'built_up_area', 'latitude', 'longitude']
for col in numeric_columns:
    new_df[col] = pd.to_numeric(new_df[col], errors='coerce')

# Drop rows with NaN values in the numeric columns to ensure clean data for groupby
new_df = new_df.dropna(subset=numeric_columns)

# Make sure the sector column doesn't have NaN values before groupby
new_df = new_df.dropna(subset=['sector'])

# Now perform the groupby operation with explicit aggregation functions
group_df = new_df.groupby('sector').agg({col: 'mean' for col in numeric_columns})

st.header('Sector Price per Sqft Geomap')




fig = px.scatter_mapbox(group_df, lat="latitude", lon="longitude", color="price_per_sqft", size='built_up_area',
                  color_continuous_scale=px.colors.cyclical.IceFire, zoom=10,
                  mapbox_style="open-street-map",width=1200,height=700,hover_name=group_df.index)

st.plotly_chart(fig,use_container_width=True)


##word cloude
st.header('Features Wordcloud')

wordcloud = WordCloud(
    width=800,
    height=800,
    background_color='black',
    stopwords=set(['s']),
    min_font_size=10
).generate(feature_text)

# ✅ Create figure explicitly
fig, ax = plt.subplots(figsize=(8, 8))
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis("off")

# ✅ Pass figure to Streamlit
st.pyplot(fig)



st.header('Area Vs Price')

property_type = st.selectbox('Select Property Type', ['flat','house'])

if property_type == 'house':
    fig1 = px.scatter(new_df[new_df['property_type'] == 'house'], x="built_up_area", y="price", color="bedRoom", title="Area Vs Price")

    st.plotly_chart(fig1, use_container_width=True)
else:
    fig1 = px.scatter(new_df[new_df['property_type'] == 'flat'], x="built_up_area", y="price", color="bedRoom",
                      title="Area Vs Price")

    st.plotly_chart(fig1, use_container_width=True)

st.header('BHK Pie Chart')

sector_options = new_df['sector'].unique().tolist()
sector_options.insert(0,'overall')

selected_sector = st.selectbox('Select Sector', sector_options)

if selected_sector == 'overall':

    fig2 = px.pie(new_df, names='bedRoom')

    st.plotly_chart(fig2, use_container_width=True)
else:

    fig2 = px.pie(new_df[new_df['sector'] == selected_sector], names='bedRoom')

    st.plotly_chart(fig2, use_container_width=True)

st.header('Side by Side BHK price comparison')

fig3 = px.box(new_df[new_df['bedRoom'] <= 4], x='bedRoom', y='price', title='BHK Price Range')

st.plotly_chart(fig3, use_container_width=True)


st.header('Side by Side Distplot for property type')

fig3 = plt.figure(figsize=(10, 4))
sns.distplot(new_df[new_df['property_type'] == 'house']['price'],label='house')
sns.distplot(new_df[new_df['property_type'] == 'flat']['price'], label='flat')
plt.legend()
st.pyplot(fig3)
