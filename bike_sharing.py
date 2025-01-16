# Import Libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='darkgrid')

# Load dataset
data = pd.read_csv("clean_df.csv")
data['dteday'] = pd.to_datetime(data['dteday'])

# Sidebar
st.sidebar.image('bike_sh.jpg')
st.sidebar.header('Bike Sharing')
start_date, end_date = st.sidebar.date_input(
    "Rentang Waktu",
    [data['dteday'].min(), data['dteday'].max()],
    min_value=data['dteday'].min(),
    max_value=data['dteday'].max()
)

# Filter data
filtered_data = data[(data['dteday'] >= pd.to_datetime(start_date)) & (data['dteday'] <= pd.to_datetime(end_date))]

#Total Penyewa
total_rentals = filtered_data['cnt'].sum()
st.header('Bike Sharing Dashboard')
st.metric("Total Penyewa Sepeda", total_rentals)

# Sewa Harian
st.subheader("Sewa Harian")
daily_data = filtered_data.groupby('dteday')['cnt'].sum()
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(daily_data.index, daily_data.values, color='#90CAF9')
ax.set_xlabel("Tanggal")
ax.set_ylabel("Jumlah Penyewa Sepeda")
ax.set_title("Jumlah Penyewa Harian")
st.pyplot(fig)

#
st.subheader("Analisi Sewa Berdasarkan Bulan dan Tahun")
# Membuat dua kolom
col1, col2 = st.columns(2)
# Kolom pertama: bulan
with col1:
    st.write("**Total Sewa Berdasarkan Bulan (2011 & 2012)**")
    month_data = filtered_data.groupby("month")['cnt'].sum().reset_index()

    # Mengubah angka bulan menjadi nama bulan
    month_names = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'Mei', 6: 'Jun',
                   7: 'Jul', 8: 'Agu', 9: 'Sep', 10: 'Okt', 11: 'Nov', 12: 'Des'}
    month_data['month'] = month_data['month'].replace(month_names)

    fig1, ax1 = plt.subplots(figsize=(6, 4))
    sns.barplot(x='month', y='cnt', data=month_data, color='#90CAF9', ax=ax1)
    ax1.set_title("Jumlah Penyewa Sepeda Berdasarkan Bulan (2011 & 2012)", fontsize=14)
    ax1.set_xlabel("Bulan", fontsize=10)
    ax1.set_ylabel("Jumlah Penyewa", fontsize=10)
    st.pyplot(fig1)

# Kolom kedua: perbandingan (2011 vs 2012)
with col2:
    st.write("**Perbandingan Total Sewa Per Bulan (2011 vs 2012)**")
    month_data = filtered_data.groupby(['year', 'month'])['cnt'].sum().reset_index()
    month_data['month'] = month_data['month'].replace(month_names)

    # Pisahkan data berdasarkan tahun
    data_2011 = month_data[month_data['year'] == 0]
    data_2012 = month_data[month_data['year'] == 1]

    fig2, ax2 = plt.subplots(figsize=(6, 4))
    sns.lineplot(x='month', y='cnt', data=data_2011, marker='o', label='2011', color='#90CAF9', ax=ax2)
    sns.lineplot(x='month', y='cnt', data=data_2012, marker='o', label='2012', color='#B9D8F3', ax=ax2)
    ax2.set_title("Perbandingan Jumlah Penyewa Sepeda Setiap Bulan (2011 vs 2012)", fontsize=14)
    ax2.set_xlabel("Bulan", fontsize=10)
    ax2.set_ylabel("Jumlah Penyewa", fontsize=10)
    ax2.legend(title='Tahun')
    st.pyplot(fig2)

# Season
st.subheader("Distribusi Penyewaan Berdasarkan Musim")
season_mapping = {1: 'Musim Semi', 2: 'Musim Panas', 3: 'Musim Gugur', 4: 'Musim Dingin'}
filtered_data['season_name'] = filtered_data['season'].map(season_mapping)
data_season = filtered_data.groupby('season_name')['cnt'].sum().reset_index()
# Membuat plot
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='season_name', y='cnt', data=data_season, palette=["#B9D8F3", "#90CAF9", "#B9D8F3", "#B9D8F3"])
ax.set_title("Jumlah Penyewa Berdasarkan Musim")
ax.set_xlabel("Musim")
ax.set_ylabel("Jumlah Penyewa")
st.pyplot(fig)


st.subheader("Distribusi Penyewaan Berdasarkan Waktu dalam Sehari")
#Kategori waktu
def kategori_waktu(hour):
    if 5 <= hour < 11:
        return 'Pagi'
    elif 11 <= hour < 15:
        return 'Siang'
    elif 15 <= hour < 18:
        return 'Sore'
    else:
        return 'Malam'

#menerapkan kategori waktu
filtered_data['waktu'] = filtered_data['hour'].apply(kategori_waktu)
waktu_sewa = filtered_data.groupby('waktu')['cnt'].sum().reset_index()

fig3, ax3 = plt.subplots(figsize=(8, 6))
colors = ["#90CAF9", "#B9D8F3","#B9D8F3","#B9D8F3"]
ax3.pie(waktu_sewa['cnt'], labels=waktu_sewa['waktu'], autopct='%1.1f%%', startangle=90, colors=colors)
ax3.set_title("Jumlah Penyewa Sepeda Berdasarkan Waktu (Pagi, Siang, Sore, Malam)", fontsize=16)
ax3.axis('equal')
st.pyplot(fig3)

st.caption('Copyright (c) Elisa_ 2024')
