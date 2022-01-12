#---------------------------------- IMPORT OF PACKAGES ----------------------------------
import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt
import webbrowser
#from pprint import pprint
from PIL import Image
import piexif
import glob
from GPSPhoto import gpsphoto
import streamlit as st
import plotly.express as px
from dateutil.relativedelta import relativedelta # to add days or years
import math
#import streamlit.components.v1 as components

#---------------------------------- SETTINGS ----------------------------------

st.set_page_config(page_title='My Travel Retrospective',
	page_icon='🌎', layout="wide")

header = st.container()
dataset = st.container()
features = st.container()
modelTraining = st.container()


pages = {
  "main": "View the travel Retrospective Dashboard",
  "page2": "Create my own dashboard",
}
  
selected_page = st.radio("Select page", pages.values())

#---------------------------------- PAGE 1 -----------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------

if selected_page == pages["main"]:

    #---------------------------------- SIDEBAR ----------------------------------

    st.sidebar.title("Welcome to my app")
    st.sidebar.markdown(" 👩🏻 Claire Mazzucato, Data Management Student")


    url = 'https://www.linkedin.com/in/claire-mazzucato-1a081a117/'

    if st.sidebar.button('Find me on Linkedin'):
        webbrowser.open_new_tab(url)

    url2 = 'https://github.com/clairemazzucato'

    if st.sidebar.button('Follow me on Github'):
        webbrowser.open_new_tab(url2)


    st.sidebar.subheader("Filters")
    #Add a filter on dates 
    ## Range selector
    cols1,_ = st.columns((1,2)) # To make it narrower
    format = 'YYYY-MM-DD'  # format output
    start_date = dt.datetime.now().date()-relativedelta(years=3)  #  I need some range in the past
    end_date = dt.datetime.now().date()-relativedelta(years=2)
    max_days = end_date-start_date
            
    add_slider = st.sidebar.slider('Select date', min_value=start_date, value=end_date ,max_value=end_date, format=format)

    #selectbox = st.sidebar.selectbox(
    #    "Filter by country",
    #    ["Australia", "France", "Italy", "Philippines", "Indonesia"]
    #)
    #st.sidebar.write(f"You selected {selectbox}")


    st.sidebar.header('Used datasets')
    st.sidebar.text('- Iphone Health App')
    st.sidebar.text('- Healthmate App')
    st.sidebar.text('- Iphone Photos dataset')

    #---------------------------------- INTRODUCTION TO APP ----------------------------------

    with header:
        st.title("Let's Take a Travel Retrospective!")
        st.label="Average Sleep"

        st.markdown('Two years ago, I spent 6 months in Melbourne in Australia as an exchange student and travelled in South East Asia. I would like to share with you some of my travels through this app.')


    #---------------------------------- MAP OF VISITED PLACES ----------------------------------
    # MAP OF VISITED PLACES
    st.subheader('🗺️ Visited places')
    newdf = pd.read_csv ('/Users/clairemazzucato/2019photos.csv')
    newdf['Date'] = pd.to_datetime(newdf['Date'])
    newdf['Date'] = newdf['Date'].dt.tz_localize(None)
    newdf = newdf.loc[newdf['Date'].dt.date < add_slider]
    st.map(newdf)
    #st.dataframe(newdf)

    #---------------------------------- DATAFRAMES PHOTOS ----------------------------------
    st.subheader('🏆 Most popular places')
    col1, col2= st.columns(2)

    newdf_sum = newdf.groupby(['City']).sum()
    newdf_sort = newdf_sum.sort_values('filename', ascending=False).head(10)
    newdf_sort = newdf_sort.iloc[1: , :]
    #newdf_sort = newdf_sort.loc[newdf_sort['Date'].dt.date < add_slider]
    with col1: 
        st.text('Most instagrammable places')
        st.dataframe(newdf_sort.index)

    #---------------------------------- COUNTRIES COUNT  ----------------------------------

    List_countries = newdf.groupby(['Country']).count()
    List_countries1 = List_countries[['City']]
    with col2:
        st.text('Visited countries & cities')
        st.dataframe(List_countries1)


    GPSdf2 = pd.read_csv ('/Users/clairemazzucato/2019photos-bis.csv')
    GPSdf2['Date'] = pd.to_datetime(GPSdf2['Date'])
    GPSdf_month = GPSdf2.set_index('Date')
    GPSdf2_month = GPSdf_month.groupby(pd.Grouper(freq="M")).count().reset_index()
    start_date = dt.datetime.now().date()-relativedelta(years=3)#  I need some range in the past
    end_date = dt.datetime.now().date()-relativedelta(years=2)
    GPSdf2_month = GPSdf2_month.loc[GPSdf2_month['Date'].dt.date > start_date]
    GPSdf2_month = GPSdf2_month.loc[GPSdf2_month['Date'].dt.date < end_date]


    #---------------------------------- BAR CHART PHOTOS ----------------------------------

    st.subheader('📅 Photos taken during year')
    fig = px.bar(GPSdf2_month, x='Date', y='filename')
    st.plotly_chart(fig, use_container_width=True)


    def adding_dt_info(df):
        df['Year'] = df['Date'].dt.year
        df['Month'] = df['Date'].dt.month
        df['day'] = df['Date'].dt.day
        df['Hour'] = df['Date'].dt.hour
        df['Weekday'] = df['Date'].dt.strftime("%A")
        df['nb_week'] = df['Date'].dt.isocalendar().week
        return df

    #---------------------------------- HEATMAP PHOTOS ----------------------------------

    st.subheader('When was most photos taken?')
    GPSdf2['Date'] = pd.to_datetime(GPSdf2['Date'])
    GPSdf2 = adding_dt_info(GPSdf2)
    GPSdf_month = GPSdf2.set_index('Date')
    GPSdf2_month = GPSdf_month.groupby(pd.Grouper(freq="W")).count().reset_index()
    start_date = dt.datetime.now().date()-relativedelta(years=3)#  I need some range in the past
    end_date = dt.datetime.now().date()-relativedelta(years=2)
    GPSdf2_month = GPSdf2_month.loc[GPSdf2_month['Date'].dt.date > start_date]
    GPSdf2_month = GPSdf2_month.loc[GPSdf2_month['Date'].dt.date < end_date]
    fig = px.density_heatmap(GPSdf2, x="Month", y="Weekday")
    st.plotly_chart(fig, use_container_width=True)


    #---------------------------------- PHOTOS KPIS ----------------------------------
    mlt = 1.5
    st.subheader("📈 Key metrics about my photo productivity")
    col1, col2, col3 = st.columns(3)

    with col1:
        #st.subheader("📷 Photos taken")
        Totalphotos = str(GPSdf2['filename'].count())
        st.metric("Total photos", Totalphotos, delta_color="inverse")


    with col2:
        #st.subheader(" ")
        Averagephotos = str(GPSdf2['filename'].count() // 12)
        st.metric("Average photos per month", Averagephotos, delta_color="inverse")

    with col3:
        #st.subheader(" ")
        Averagephotosday = str(GPSdf2['filename'].count() // 365)
        st.metric("Average photos per day", Averagephotosday, delta_color="inverse")

    #---------------------------------- HEALTH DATA IMPORT  ----------------------------------
    health_data = pd.read_csv ('/Users/clairemazzucato/health_data.csv')
    sleep_data = pd.read_csv ('/Users/clairemazzucato/sleep_data.csv')

    #---------------------------------- HEALTH KPIS -------------------------------------------
    st.subheader("💪🏻 And what about my health during trips?")
    col1, col2, col3 = st.columns(3)


    health_data_steps = health_data.loc[health_data['type'] == 'StepCount']
    health_data_distance = health_data.loc[health_data['type'] == 'DistanceWalkingRunning']

    #health_data_distance = health_data_distance[(health_data_distance['CreationDatebis'] > start_date) & (health_data_distance['CreationDatebis'] < end_date)]

    health_data_distance_grouped = health_data_distance.groupby(['CreationDatebis']).sum()
    health_data_steps_grouped = health_data_steps.groupby(['CreationDatebis']).sum()

    meandistance = str(math.ceil(health_data_distance_grouped['value'].mean())*mlt)
    meansteps = str(math.ceil(health_data_steps_grouped['value'].mean())*mlt)


    for col in ['creationDate', 'startDate', 'endDate']:
            sleep_data[col] = pd.to_datetime(sleep_data[col])
    sleep_data['startDate'] = sleep_data['startDate'].dt.tz_localize(None)
    sleep_data['endDate'] = sleep_data['endDate'].dt.tz_localize(None)
    sleep_data['creationDate'] = sleep_data['creationDate'].dt.tz_localize(None)

    sleep_data['duration'] = round((sleep_data['endDate']- sleep_data['startDate']).dt.floor('s') / np.timedelta64(1, 's') / 3600.,2)
    averagesleep = math.ceil(sleep_data['duration'].mean())



    with col1:
        st.metric("Daily average distance in KM", meandistance, delta_color="inverse")
    with col2:
        st.metric("Daily average steps", meansteps, delta_color="inverse")
    with col3:
        st.metric("Average night's sleep in HR", averagesleep, delta_color="inverse")

    #---------------------------------- HEALTH CHART ----------------------------------------

    #st.subheader("Walking Activity")
    #fig = px.bar(health_data_distance, x='CreationDatebis', y='value')
    #st.plotly_chart(fig, use_container_width=True)


    text = '''

    ---

    '''
    st.markdown(text)

#---------------------------------- PAGE 2 -----------------------------------
#-----------------------------------------------------------------------------
elif selected_page == pages["page2"]:

#---------------------------------- SIDEBAR ----------------------------------

    st.sidebar.title("Welcome to my app")
    st.sidebar.markdown(" 👩🏻 Claire Mazzucato, Data Management Student")


    url = 'https://www.linkedin.com/in/claire-mazzucato-1a081a117/'

    if st.sidebar.button('Find me on Linkedin'):
        webbrowser.open_new_tab(url)

    url2 = 'https://github.com/clairemazzucato'

    if st.sidebar.button('Follow me on Github'):
        webbrowser.open_new_tab(url2)



    st.header("ℹ️ How to create your own travel retrospective:")
    st.subheader("Export data")
    st.markdown("- First, export your health data from your Apple Health App, the file should be named 'export.xml'")
    st.markdown("- Secondly, export your raw photos in a folder named 'test'. For Mac users, watch this tutorial:")
    
    url3 = 'https://www.fireebok.com/resource/how-to-extract-all-photo-metadata-tags-from-photos-on-mac.html'
    if st.button('Export XMP photos'):
        webbrowser.open_new_tab(url3)

    st.subheader("Import data")   
    st.text("Import your Apple health data")
    uploaded_files = st.file_uploader("Choose your export.xml file", accept_multiple_files=True)
    for uploaded_file in uploaded_files:
        bytes_data = uploaded_file.read()
        st.write("filename:", uploaded_file.name)
        st.write(bytes_data)     

    st.text("Import your folder containing photos")
    uploaded_files = st.file_uploader("Choose your photo folder", accept_multiple_files=True)
    for uploaded_file in uploaded_files:
        bytes_data = uploaded_file.read()
        st.write("filename:", uploaded_file.name)
        st.write(bytes_data)   

    st.subheader("Create your own map")

    #path = '/Users/clairemazzucato/Desktop/test'

    #all_files = glob.glob(path + "/*.JPG") + glob.glob(path + "/*.jpg")
    #list_gps = []

    #@st.cache
    #def main():
    #    n = 0
    #    for filename in all_files: 
    #        im = Image.open(filename)
    #        # Get the data from image file and return a dictionary
    #        data = gpsphoto.getGPSData(filename)
    #        if data.get('Latitude') is not None and data.get('Longitude'):
    #        #if data['Latitude'] != '' and data['Longitude'] != '':
    #            #print(filename, data['Date'], data['Latitude'], data['Longitude'])
    #            data['filename'] = filename
    #            list_gps.append(data)
    #        n = n + 1
    #if __name__ == '__main__':
    #    main()

    #GPSdf = pd.DataFrame(list_gps)
    #GEOdf = GPSdf.rename(columns={'Latitude': 'lat', 'Longitude': 'lon'})
    #GEOdf['Date'] = pd.to_datetime(GEOdf['Date'])
    #GEOdf = GEOdf.loc[GEOdf['Date'].dt.date < add_slider]

    st.markdown("⚠️ This functionality is under construction, the Map Generator will be back soon ! ")




