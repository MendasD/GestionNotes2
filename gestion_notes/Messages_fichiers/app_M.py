
import numpy as np
import pandas as pd
import plotly as py
import streamlit as st 
import query
import altair as alt
from streamlit_option_menu import option_menu 
from numerize.numerize import numerize 
import plotly.graph_objs as go
import plotly.figure_factory as ff
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as plt
import warnings
warnings.filterwarnings('ignore')


#Streamlit Configuration 

#######################
# Page configuration
st.set_page_config(
    page_title="Mental Health Disorders Trends",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

#######################
# CSS styling


st.markdown("""
<style>
    [data-testid=stSidebar] {
        background-color: #1b2631;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
    .stForm {
        background-color: #1b2631;
    }
    </style>
""", unsafe_allow_html=True)

#########################################
#DATA EXPLORER
#########################################
#import streamlit as st
import pandas as pd
import requests
import io

# URL du fichier CSV
file_url = 'https://drive.google.com/uc?export=download&id=1amQ77JbBVBliMY4tffkSm9jkVZ0-uv5l'

# Télécharger le fichier
response = requests.get(file_url)
dataset = io.StringIO(response.text)

# Lire le CSV dans un DataFrame
data = pd.read_csv(dataset, on_bad_lines='warn')

# Utiliser le DataFrame dans ton application Streamlit
#st.write(df)
#Load our Dataset
#data = pd.read_csv('Mental health Depression disorder Data 3.csv')

#Informations of our dataset
data.info()

#Check the number of missing values
data.isnull().sum()


#Handling Columns

#Splitting final tables and naming the headers based on columns

# First Part
data_1 = data.iloc[:6468]

# Second Part
data_2 = data.iloc[6469:54276]
data_2.columns = data.iloc[6468]
data_2 = data_2.iloc[:,:7].drop(columns = 6468)

# Third Part
data_3 = data.iloc[54277:102084]
data_3.columns = data.iloc[54276]
data_3 = data_3.iloc[:,:7].drop(columns = 54276)

#Fourth Part
data_4 = data.iloc[102085:]
data_4.columns = data.iloc[102084]
data_4 = data_4.iloc[:,:5].drop(columns = 102084)

#Joining tables based on entity, code and year for a deeper analysis

Table_1 = pd.merge(data_1, data_2, how='left', on=['Entity', 'Code', 'Year'])
Table_2 = pd.merge(Table_1, data_3, how='left', on=['Entity', 'Code', 'Year'])
_data = pd.merge(Table_2, data_4, how='left', on=['Entity', 'Code', 'Year'])
_data.head()

# OUR DATASET

data = _data
data.head()


#########################################
#HANDLE CATEGORICAL VARIABLES 
#########################################

#Convert columns to FLOAT

for column in data.columns:
  try:
    data[column] = data[column].astype(float)
  except Exception as e:
    print('Error', column, e)


#########################################
#HANDLE MISSING VALUES 
#########################################

# Check Missing Values
print('Missing Values:')
missing = data.isnull().sum()
#missing

# Delete 'Population_y' and 'Code'columns
data = data.drop('Population_y', axis=1)
data = data.drop('Code', axis=1)

#Convert Year column to INT 
data['Year'] = data['Year'].astype(int)

# Use interpolate to handle missing values for Population column
data['Population_x'] = data['Population_x'].interpolate(method='linear')

##########################
#TITLE
##########################
st.markdown("# Mental Health Disorders Analysis")


#########################################
#SIDEBAR
#########################################

#Sidebar 
st.sidebar.image('Main_App/im.jpg', caption='Mental Health Disorders Trends') #ADD IMAGE OR LOGO TO SIDEBAR 

# Switchers
all_years = ["All"] + list(data['Year'].unique())
year = st.sidebar.multiselect(
    "Select Year",
    options=all_years,
    default=all_years
)

all_entities = ["All"] + list(data['Entity'].unique())
entity = st.sidebar.multiselect(
    "Select Entity",
    options=all_entities,
    default=all_entities
)

# Apply filters
if "All" in year:
    filtered_year = data
else:
    filtered_year = data[data['Year'].isin(year)]

if "All" in entity:
    filtered_data = filtered_year
else:
    filtered_data = filtered_year[filtered_year['Entity'].isin(entity)]


#########################################
#HANDLE COLUMNS DISPLAYING 
#########################################

def selection():
   with st.expander("Show Variables"):
      show_variables = st.multiselect('Filter: ', filtered_data.columns, default=[])
      st.write(filtered_data[show_variables])
    
   #Analysis
   total_anxiety_disorders = filtered_data['Anxiety disorders (%)'].mean()   
   total_suicide_rate = filtered_data['Suicide rate (deaths per 100,000 individuals)'].mean()
   total_depression_number = filtered_data['Prevalence - Depressive disorders - Sex: Both - Age: All Ages (Number) (people suffering from depression)'].sum()
   section_1, section_2, section_3 = st.columns(3, gap='large')

   with section_1:
        st.info('Anxiety')
        st.metric(label='Anxiety_Disorders', value=f'{total_anxiety_disorders:,.0f}')

   with section_2:
        st.info('Suicide (100,000)')
        st.metric(label='Total Suicide Rate', value=f'{total_suicide_rate:,.0f}')

   with section_3:
        st.info('Depression (Number)')
        st.metric(label='Depression Disorder (Number)', value=f'{total_depression_number:,.0f}')

selection()


#Create new datafram that group value by yearly
mean_by_year_df = data.groupby('Year')[['Schizophrenia (%)', 'Bipolar disorder (%)',
       'Eating disorders (%)', 'Anxiety disorders (%)', 'Drug use disorders (%)',
       'Depression (%)', 'Alcohol use disorders (%)']].mean().reset_index()
#mean_by_year_df


################################
#VISUALIZATIONS 
################################ 

def graph():
    st.markdown('#### Mental Health Disorders over Years')
    fig = go.Figure()
    # Add line 
    for column in mean_by_year_df.columns[1:]:
       fig.add_trace(go.Scatter(
            x=mean_by_year_df['Year'],
            y=mean_by_year_df[column],
            mode='lines+markers',
            name=column
        ))
    # Updating Layout 
    fig.update_layout(
    #title='Mental Health Through Years',
    xaxis_title='Years',
    yaxis_title='Disorders Rates',
    legend_title='Mental Health Disorders',
    xaxis=dict(tickmode='linear', tickvals=mean_by_year_df['Year'].tolist()),
    xaxis_tickangle=-90,
    template='plotly_white'
)
    st.plotly_chart(fig)

graph()

#####################

# Choose Year
years = sorted(data['Year'].unique())
selected_year = st.sidebar.selectbox('Year', years)

# Mental Disorders List
disorders = [
        'Schizophrenia (%)', 
        'Bipolar disorder (%)', 
        'Eating disorders (%)', 
        'Anxiety disorders (%)', 
        'Drug use disorders (%)', 
        'Depression (%)', 
        'Alcohol use disorders (%)'
    ]
selected_disorder = st.sidebar.selectbox('Mental Disorder', disorders)
# Choose color
color_themes = [
        'Viridis', 'Cividis', 'Plasma', 'Inferno', 'Magma',
        'Blues', 'Greens', 'Reds', 'Oranges', 'Purples',
        'Rainbow', 'Jet', 'Picnic', 'Portland', 'Jet'
    ]
    # Choose Theme
selected_color_theme = st.sidebar.selectbox('Choose Theme', color_themes)

def make_choropleth(data, year, mental_health_disorder, input_color_theme):
    st.markdown('#### Mental Health Disorders Rates in Countries')
    # Filter Year
    df_year = data[(data['Year'] == year) & (data['Entity'].notnull())]

    # Choropleth Map
    choropleth = px.choropleth(
        df_year,
        locations='Entity',  #Columns names
        color=mental_health_disorder,  # Disorders columns
        locationmode="country names",
        color_continuous_scale=input_color_theme,
        range_color=(0, df_year[mental_health_disorder].max()),
        labels={mental_health_disorder: mental_health_disorder},
        scope="world"
    )
    
    # Undate layout
    choropleth.update_layout(
        #title='Mental Health Disorders Rates in Countries',
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=0, r=0, t=0, b=0),
        height=450,  
        )
    

    
    st.plotly_chart(choropleth, use_container_width=True)

make_choropleth(data, selected_year, selected_disorder, selected_color_theme)


def make_bar_1(data):
    st.markdown('#### Mental Health Disorders in selected Entities')
    #Load Second Dataset
    dataset = pd.read_csv('Main_App/continents2.csv')
    #Keep necessary columns only and rename
    continent = dataset[['region', 'sub-region', 'name']]
    continent = dataset.rename(columns = {'name': 'Entity'})
    #continent_df.head()

    #Join our datasets 
    #Left join to source_df
    merge_df = data.merge(continent[['Entity', 'region']], how='left', on ='Entity')
    data = merge_df
    
# Créer le graphique en barres avec Plotly
    fig_1 = px.bar(filtered_data,
             x='Entity',
             y=selected_disorder,
             color=selected_disorder,
             color_continuous_scale=selected_color_theme,
             #title='Mental Health Disorders in Regions?',
             labels={'value': 'Disorder Rate', 'region': 'Region'},
             text=selected_disorder)
    
    fig_1.update_layout(height=500, width=1600)

    st.plotly_chart(fig_1)

make_bar_1(data)

def make_bar_2(data):
    st.markdown('#### Mental Health Disorders in Regions')
    #Load Second Dataset
    dataset = pd.read_csv('Main_App/continents2.csv')
    #Keep necessary columns only and rename
    continent = dataset[['region', 'sub-region', 'name']]
    continent = dataset.rename(columns = {'name': 'Entity'})
    #continent_df.head()

    #Join our datasets 
    #Left join to source_df
    merge_df = data.merge(continent[['Entity', 'region']], how='left', on ='Entity')
    data = merge_df
    
# Créer le graphique en barres avec Plotly
    fig_2 = px.bar(data,
             x='region',
             y=selected_disorder,
             color=selected_disorder,
             color_continuous_scale=selected_color_theme,
             #title='Mental Health Disorders in Selected Entities',
             labels={'value': 'Disorder Rate', 'region': 'Region'},
             text=selected_disorder)
    
    fig_2.update_layout(height=500, width=1600)       
    st.plotly_chart(fig_2)
    
make_bar_2(data)
# Columns Configuration
#def main():
    
    # Créer les colonnes pour organiser les graphiques
    #col1, col2 = st.columns(2, gap='medium')
    
    #with col1:
       #make_bar_1(data)

    #with col2:
       #make_bar_2(data)    
#if __name__ == "__main__":
    #main()

    
def suicide(data):
    fig = px.scatter(filtered_data, x="Depression (%)", y="Suicide rate (deaths per 100,000 individuals)",
	         size="Population_x", color="Entity",
                 hover_name="Entity", log_x=True, size_max=60, animation_frame= 'Year')


    
    st.plotly_chart(fig, use_container_width=True)

suicide(data)


def gender(data):
    # Préparer les données pour le graphique Sunburst
    long_data = data.melt(id_vars=['Year', 'Entity'], value_vars=['Prevalence in females (%)', 'Prevalence in males (%)'], 
                        var_name='Gender', value_name='Prevalence')

    # Ajouter une colonne de niveau hiérarchique
    long_data['Level'] = long_data['Year'].astype(str) + ' > ' + long_data['Gender']

    # Création du graphique Sunburst
    fig = px.sunburst(
        long_data,
        path=['Year', 'Gender', 'Entity'],
        values='Prevalence',
        title='Depression Prevalence by Gender in Different Years and Entities'
    )

    
    st.plotly_chart(fig, use_container_width=True)

gender(data)

    #selected_year,selected_disorder,selected_color_theme

    #.query("year==2007")

    

#make_bar(data)


    #col1, col2 = st.columns(2, gap='small')
    
    #with col1:
       #make_choropleth(data, selected_year, selected_disorder, selected_color_theme)

    
    

#########################################
#HANDLE COLUMNS DISPLAYING 
#########################################

