import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
st.set_page_config(page_title="Spotify 2024 Global Streaming Data", layout="wide", initial_sidebar_state="auto")
st.sidebar.header('Фильтры для визуализации датасета')

st.markdown("<h1 style='text-align: center;'>Spotify 2024 Global Streaming Data", unsafe_allow_html=True)
st.divider()

dataframe = pd.read_csv('Spotify_2024_Global_Streaming_Data.csv')
rows_counts = st.sidebar.slider(label="Выберите сколько строк отобразить", min_value=10, max_value=len(dataframe))
release_year = st.sidebar.select_slider(label="Выберите треки какого года отобразить", options=sorted(dataframe['Release Year'].unique()), value=(dataframe['Release Year'].min(), dataframe['Release Year'].max()))
country = st.sidebar.multiselect(label="Выберите какие страны отобразить", options=sorted(dataframe['Country'].unique()), default=sorted(dataframe['Country'].unique()))
genre = st.sidebar.multiselect(label="Выберите какой жанр музыки отобразить", options=sorted(dataframe['Genre'].unique()), default=sorted(dataframe['Genre'].unique()))
platform_type = st.sidebar.multiselect(label="Выберите какой тип платформы отобразить", options=sorted(dataframe['Platform Type'].unique()), default=sorted(dataframe['Platform Type'].unique()))
columns_order = [
    'Country',
    'Artist',
    'Album',
    'Genre',
    'Release Year',
    'Monthly Listeners (Millions)',
    'Total Streams (Millions)',
    'Total Hours Streamed (Millions)',
    'Avg Stream Duration (Min)',
    'Platform Type',
    'Streams Last 30 Days (Millions)',
    'Skip Rate (%)'
]
edit_dataframe = (dataframe[
    (dataframe['Country'].isin(country)) &
    (dataframe['Genre'].isin(genre)) &
    (dataframe['Release Year'].between(release_year[0], release_year[1])) &
    (dataframe['Platform Type'].isin(platform_type))
].loc[:, columns_order]).copy()
st.dataframe(edit_dataframe.head(rows_counts))

st.divider()
title_map = {
    ('Country', 'Monthly Listeners (Millions)'): 'Распределение кол-ва ежемесячных слушателей по странам',
    ('Genre', 'Monthly Listeners (Millions)'): 'Распределение кол-ва ежемесячных слушателей по жанрам',
    ('Platform Type', 'Monthly Listeners (Millions)'): 'Распределение кол-ва ежемесячных слушателей по платформам',

    ('Country', 'Total Streams (Millions)'): 'Распределение кол-ва прослушиваний по странам',
    ('Genre', 'Total Streams (Millions)'): 'Распределение кол-ва прослушиваний по жанрам',
    ('Platform Type', 'Total Streams (Millions)'): 'Распределение кол-ва прослушиваний по платформам',

    ('Country', 'Total Hours Streamed (Millions)'): 'Распределение часов прослушиваний по странам',
    ('Genre', 'Total Hours Streamed (Millions)'): 'Распределение часов прослушиваний по жанрам',
    ('Platform Type', 'Total Hours Streamed (Millions)'): 'Распределение часов прослушиваний по платформам',
}
x_label_map = {
    'Country': 'Страна',
    'Genre': 'Жанр',
    'Platform Type': 'Платформа'
}
y_label_map = {
    'Monthly Listeners (Millions)': 'Кол-во ежемесячных слушателей',
    'Total Streams (Millions)': 'Общее кол-во прослушиваний',
    'Total Hours Streamed (Millions)': 'Общие часы прослушиваний'
}
x_option = st.selectbox(label="Выберите ось X", options=['Country', 'Genre', 'Platform Type'], index=2)
y_option = st.selectbox(label="Выберите ось Y", options=['Monthly Listeners (Millions)', 'Total Streams (Millions)', 'Total Hours Streamed (Millions)'], index=2)
hours_by_platform = edit_dataframe.groupby(x_option)[y_option].sum()
fig, ax = plt.subplots(figsize=(5, 3))
hours_by_platform.plot(kind='bar', ax=ax)
ax.set_title(title_map[x_option, y_option])
ax.set_xlabel(x_label_map[x_option])
ax.set_ylabel(y_label_map[y_option])
ax.grid(axis="y")
st.pyplot(fig)
