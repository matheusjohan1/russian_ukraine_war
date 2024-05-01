import pandas as pd
from PIL import Image
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import streamlit as st
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster

st.set_page_config(layout = 'wide')

pd.options.display.float_format = '{:.2f}'.format

refugees_by_country = pd.read_csv('datasets/ukrainian_refugees_by_country.csv')

refugees_by_country.rename(columns={
     'Country':'country',
     'Number of Refugees (January 15, 2024)': 'refugees'}, inplace=True)

refugees = refugees_by_country[['country', 'refugees']].copy()

coords = pd.read_csv('datasets/world_country_and_usa_states_latitude_and_longitude_values.csv')
coords = coords.dropna(subset=['latitude', 'longitude'])
coords_ = coords[['latitude', 'longitude', 'country']].copy()

refugees = pd.merge(refugees, coords_, on='country', how='left')

military = pd.read_csv('datasets/military_spending.csv')
military = military.rename(columns={"RUSSIA'S MILITARY SPENDING\nper year ($USD bn)":'Russia', "UKRAINE'S MILITARY SPENDING\r\nper year ($USD bn)":'Ukraine'})
military['Year'] = military['Year'].astype(str)

nm1 = military[['Year', "RUSSIA'S % of GDP"]]
nm1 = nm1.rename(columns={"RUSSIA'S % of GDP":'% GDP'})
nm1['country'] = 'Rússia'

nm2 = military[['Year', "UKRAINE'S % of GDP"]]
nm2 = nm2.rename(columns={"UKRAINE'S % of GDP":'% GDP'})
nm2['country'] = 'Ucrânia'

military2 = pd.concat([nm1, nm2])
military2 = military2.replace({'% GDP': r'%'}, {'% GDP': ''}, regex=True)
military2['% GDP'] = military2['% GDP'].astype(float)

financial_aid = pd.read_csv('datasets/financial_aid.csv')
a = financial_aid[:4]
b = pd.DataFrame(financial_aid[4:].sum()).T
b.at[0, 'Country'] = 'Outros'
financial_aid_1 = pd.concat([a,b])
financial_aid_1 = financial_aid_1.reset_index(drop=True)
financial_aid_1 = financial_aid_1.replace({'Country': r'United States'}, {'Country': 'Estados Unidos'}, regex=True)
financial_aid_1 = financial_aid_1.replace({'Country': r'Germany'}, {'Country': 'Alemanha'}, regex=True)
financial_aid_1 = financial_aid_1.replace({'Country': r'United Kingdom'}, {'Country': 'Reino Unido'}, regex=True)
financial_aid_1 = financial_aid_1.replace({'Country': r'Denmark'}, {'Country': 'Dinamarca'}, regex=True)
financial_aid_1['% of total'] = financial_aid_1['% of total'].astype(float)
financial_aid_1['% of total'] = financial_aid_1['% of total'].round()

russian_control = pd.read_csv('datasets/russian_control.csv')
russian_control['country'] = 'Ukraine'
russian_control = russian_control.replace({'% Ukraine occupied by Russia': r'%'}, {'% Ukraine occupied by Russia': ''}, regex=True)
russian_control['% Ukraine occupied by Russia'] = russian_control['% Ukraine occupied by Russia'].astype(float)

deaths = pd.read_csv('datasets/estimated_deaths.csv')

uk_civilians = pd.read_csv('datasets/uk_civilian.csv')

political_countries_url = (
    "http://geojson.xyz/naturalearth-3.3.0/ne_50m_admin_0_countries.geojson")

pic = 'img/anzhela-bets-6HBpGLk4DgI-unsplash.jpg'

c01, c02, c03 = st.columns((1,1,1))
with c01:
    st.title('798 dias')

c1, c2 = st.columns((1,1))

with c1:
      # adding image
      image = Image.open(pic)
      new_pic = image.resize((800,800))
      st.image(new_pic)

with c2:
      # adding texts
      c2.header('Em 22 de Fevereiro de 2022, a Rússia invadiu a Ucrânia…')
      c2.markdown('    ')
      c2.markdown('    ')
      c2.markdown('    ')
      c2.markdown('    ')
      c2.markdown('    ')
      c2.markdown('    ')
      c2.markdown('    ')
      c2.markdown('    ')
      c2.markdown('    ')
      c2.markdown('    ')
      c2.markdown('    ')      
      c2.markdown('    ')
      c2.markdown('    ')
      c2.markdown('    ')
      c2.markdown('    ')
      c2.markdown('    ')
      c2.markdown('    ')
      c2.markdown('    ')
      c2.markdown('    ')
      c2.markdown('    ')
      c2.markdown('    ')
      c2.markdown('    ')
      c2.markdown('    ')
      c2.markdown('    ')
      c2.markdown('    ')
      c2.markdown('    ')
      c2.markdown('    ')
      c2.markdown('    ')
      c2.subheader("Até o dia 30 de Abril de 2024, já se passaram 798 dias que se deu início a guerra e o terror para milhões de pessoas.                   ")
      c2.markdown('*Prédio destruído na cidade de Chernihiv, Ucrânia* [Foto: Anzhela Bets](https://unsplash.com/pt-br/fotografias/um-grande-edificio-que-foi-demolido-6HBpGLk4DgI)')



st.markdown('## As estimativas de gastos militares são de, aproximadamente,') 
st.markdown('# :orange[US$ 600 bi].')

st.text('Enquanto, normalmente, os países reservam até 2% do PIB para gastos militares, ambos os países aumentaram o quanto destinaram do PIB e a Ucrânia ultrapassou a')
st.text('marca dos 20%, tanto em 2022 (início da guerra), quanto em 2024. Vale ressaltar que, além dos valores que estão representados no gráfico, a Ucrânia recebeu')
st.text('cerca de US$ 179 bi em recursos militares, totalizando, então, os US$ 600 bi.')

c3, c4 = st.columns((2,1))

with c3:
    #set seaborn style
    sns.set_theme(style = 'dark', rc={'axes.facecolor':'#0E1117', 'figure.facecolor':'#0E1117', 'xtick.color':'white', 'ytick.color':'white'})
    sns.despine()

    # setting figure size
    fig = plt.figure(figsize=(12,6))

    #define colors to use in chart
    color_map = ['darkseagreen', 'lightslategrey']
        
    #create area chart
    plt.stackplot(military['Year'], military["Russia"], military["Ukraine"],
                                    labels=['Rússia', 'Ucrânia'],
                                    colors=color_map)


    #add legend
    legend = plt.legend(loc='upper left', labelcolor='white')

    #add graph title, axis labels and remove borders
    plt.title('Gastos Militares US$ bi', color='white', fontweight='bold')
    plt.xlabel('Ano', color='white', fontweight='bold')
    plt.ylabel('US$ Bilhões', color='white', fontweight='bold')
    sns.despine(left=True)

    #display area chart
    st.pyplot(fig)

with c4:
     #set seaborn style
     sns.set_theme(style = 'dark', rc={'axes.facecolor':'#0E1117', 'figure.facecolor':'#0E1117', 'xtick.color':'white', 'ytick.color':'white'})

     #setting figure size
     fig, ax = plt.subplots(figsize=(8, 8.8))

     #define colors to use in chart
     color_map = {'Rússia':'darkseagreen', 'Ucrânia':'lightslategrey'}
        
     #create area chart
     ax = sns.barplot(x='% GDP', y='Year', hue='country', data=military2, orient='h', palette=color_map)

     # add values
     for container in ax.containers:
         ax.bar_label(container, color='w', padding=5)
        
     #add legend
     legend = plt.legend(loc='upper right', labelcolor='white')

     #add graph title, axis labels and remove borders
     plt.title('% PIB', color='white', fontsize=14, fontweight='bold')
     plt.xlabel('% PIB', color='white', fontweight='bold')
     plt.ylabel('Ano', color='white', fontweight='bold')
     sns.despine(left=True)

     #display area chart
     st.pyplot(fig, use_container_width=True)

st.markdown('## De onde vem os US$ 179 bi destinados a Ucrânia? ') 

c5, c6 = st.columns((2,1))

with c5:
     x = financial_aid_1['Country']
     y = financial_aid_1['% of total']
     text = financial_aid_1['% of total']

     #create area chart
     fig = go.Figure(go.Waterfall(
         x=x,
         y=y,
         text=text, increasing = {"marker":{"color":"#778899"}},
         textposition = "outside"

     ))
     
     # update layout
     fig.update_layout(plot_bgcolor='#0E1117', paper_bgcolor='#0E1117', font=dict(color='#FFFFFF'), yaxis=dict(
        title_text="% Ajuda Militar"))
     fig.update_xaxes(showgrid=False)
     fig.update_yaxes(showgrid=False)

     st.plotly_chart(fig, use_container_width=True)

with c6:
     # adding texts
     st.markdown('    ')      
     st.markdown('    ')
     st.markdown('- A Alemanha foi o segundo país que mais financiou militarmente a Ucrânia e é quem mais importa Gás Natural da Rússia. Dos **239** bilhões de metros cúbicos exportados pela Rússia, cerca de **56.3** bilhões vão para a Alemanha;')
     st.markdown('- Os Estados Unidos foi o país que mais enviou recursos com fins militares a Ucrânia com, aproximadamente, **103 bi de dólares**. Desses, **61 bi de dólares** foram repassados após Janeiro de 2024;')
     st.markdown('- Os Estados Unidos é o principal produtor de Gás Natural no mundo. No entanto, a Rússia é o país que mais exporta Gás Natural.')

c7, c8 = st.columns((1,2))

with c7:
     # adding texts
     st.header('Ocupação do território ucraniano')

     st.markdown('Logo após a invasão russa em Fevereiro de 2024, a Ucrânia teve o pico da invasão. Com isso, grande parte da população precisou sair do próprio país para evitar os confrontos da guerra. Até Janeiro de 2024, aproximadamente, **5 milhões** de ucranianos se refugiaram em outros países.')
     st.markdown('    ')
     st.markdown('    ')

     # setting figure size
     fig = plt.figure(figsize=(6,4))

     # determining colors used
     color_map = ['lightsteelblue', 'lightslategrey', 'darkseagreen']

     # creating area chart
     ax = sns.barplot(data=russian_control, x='month_year', y='% Ukraine occupied by Russia', palette=color_map)

     # adding values
     for container in ax.containers:
          ax.bar_label(container, color='w', padding=5)

     # updating layout and removing borders
     plt.xlabel('Mês-ano', color='white', fontweight='bold')
     plt.ylabel('% Ocupação Russa', color='white', fontweight='bold')

     sns.despine(left=True)

     st.pyplot(fig)

with c8:
    st.subheader('Para onde vão os refugiados ucranianos?')
    # creating map
    m = folium.Map(location=[53.0000, 9.0000], zoom_start=3)

    # adding layer
    folium.Choropleth(
        geo_data=political_countries_url,
        data=refugees,
        columns=['country', 'refugees'],
        key_on='feature.properties.name',
        fill_color='YlOrRd', 
        fill_opacity=0.7, 
        line_opacity=0.2,
        nan_fill_color="white",
        legend_name='Refugiados da Ucrânia'
    ).add_to(m)

    # adding markers
    marker_cluster = MarkerCluster().add_to(m)

    for name, row in refugees.iterrows():
            folium.Marker( [row['latitude'], row['longitude']],
                        popup='País: {0} Número de Refugiados: {1}'.format( row['country'],
                                                                        row['refugees'])).add_to(marker_cluster)

    folium_static(m, width=950, height=500)

c9, c10, c11 = st.columns((1,1,1))

with c9:
     st.subheader('Soldados mortos')
     st.markdown('Até o momento, cerca de 135 mil pessoas perderam suas vidas no campo de batalha.')
     
     # setting figure size
     fig = plt.figure(figsize=(6,4))

     # setting colors
     color_map = {'Rússia':'darkseagreen', 'Ucrânia':'lightslategrey'}

     # creating chart area
     ax = sns.barplot(data=deaths.loc[deaths['type'] == 'military'], x='country', y='killed', palette=color_map)
     
     # adding values
     for container in ax.containers:
         ax.bar_label(container, color='w', padding=5)

     # updating layout and remove borders
     plt.xlabel('Número de Mortos', color='white', fontweight='bold')
     plt.ylabel('País', color='white', fontweight='bold')
     sns.despine(left=True)

     st.pyplot(fig)

with c10:
     st.subheader('Soldados feridos')
     st.markdown('Além dos 135 mil mortos, quase 300 mil soldados foram feridos.')
     
     # setting figure size
     fig = plt.figure(figsize=(6,5))

     # setting colors
     color_map = {'Rússia':'darkseagreen', 'Ucrânia':'lightslategrey'}

     # creating area chart
     ax = sns.barplot(data=deaths.loc[deaths['type'] == 'military'], x='wounded', y='country', palette=color_map)

     # adding values
     for container in ax.containers:
         ax.bar_label(container, color='w', padding=5)

     # updating layout and removing borders
     plt.xlabel('Número de Feridos', color='white', fontweight='bold')
     plt.ylabel('País', color='white', fontweight='bold')
     sns.despine(left=True)

     st.pyplot(fig)

with c11:
     st.subheader('Civis ucranianos')
     st.markdown('E a guerra não atinge apenas os militares, mas também os civis que não conseguiram fugir ou não tiveram nem tempo.')
     
     # setting figure size
     fig = plt.figure(figsize=(6,4))

     # setting colors
     color_map = {'Mortos':'tomato', 'Feridos':'lightcoral'}

     # creating area chart
     ax = sns.barplot(data=uk_civilians, x='type', y='count', palette=color_map)
     
     # adding values
     for container in ax.containers:
         ax.bar_label(container, color='w', padding=5)

     # updating layout and removing borders
     plt.xlabel('Contagem', color='white', fontweight='bold')
     plt.ylabel('Morto ou Ferido', color='white', fontweight='bold')
     sns.despine(left=True)
     
     st.pyplot(fig)

st.header('Mais quantos dias e vidas serão necessários para encerrar a guerra?')