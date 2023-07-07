# Nama  : Yudha Saputra
# Email : yyudhasaputra@gmail.com

# Memasukan seluruh library yang dibutuhkan
import pandas as pd
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt
 
 # Mendefinisikan fungsi-fungsi yang dibutuhkan
def create_working_df(df):
    df = df.drop('timestamp', axis=1)
    working_day_ride = df.groupby(by=['workingday','user_type']).mean()
    working_day_ride = working_day_ride.reset_index()
    working_day_ride = working_day_ride.drop('holiday', axis = 1)
    working_day_ride['workingday'] = working_day_ride['workingday'].replace({0:'Not Working',1:'Working'})
    return working_day_ride

def create_holiday_df(df):
    df = df.drop('timestamp', axis=1)
    holiday_day_ride = df[df['workingday'] == 0].groupby(by=['holiday','user_type']).mean()
    holiday_day_ride = holiday_day_ride.reset_index()
    holiday_day_ride['holiday'] = holiday_day_ride['holiday'].replace({0:'Non-Holiday',1:'Holiday'})
    return holiday_day_ride
 
def create_timestamp_df(df):
    df['hr'] = df['hr'].astype(str)
    df['timestamp'] = pd.to_datetime(df['dteday'] + ' ' + df['hr'].str.zfill(2), format='%Y-%m-%d %H')
    df = df.sort_values('timestamp')
    return df
    
def create_weather_df(df):
    weather_labels = {1: 'Clear', 2: 'Cloudy', 3: 'Rainy', 4: 'Stormy'}
    zipped_data = list(zip(df['weathersit'],df['casual'],df['registered'],df['cnt']))
    ride_hr_df = pd.DataFrame(zipped_data, columns=['weather','casual','registered','total'])
    ride_hr_df['weather'] = ride_hr_df['weather'].replace(weather_labels)
    return ride_hr_df

def create_season_df(df):
    season_labels = ['Spring','Summer','Fall','Winter']
    zipped_data = list(zip(df['season'],df['casual'],df['registered'],df['cnt']))
    ride_hr_df = pd.DataFrame(zipped_data, columns=['season','casual','registered','total'])
    ride_hr_df['season'] = ride_hr_df['season'].replace(season_labels)
    return ride_hr_df

def create_season_weather_df(df):
    season_labels = {1:'Spring',2:'Summer',3:'Fall',4:'Winter'}
    weather_labels = {1: 'Clear', 2: 'Cloudy', 3: 'Rainy', 4: 'Stormy'}
    zipped_data = list(zip(df['season'],df['weathersit'],df['casual'],df['registered'],df['cnt']))
    ride_hr_df = pd.DataFrame(zipped_data, columns=['season','weather','casual','registered','total'])
    ride_hr_df['season'] = ride_hr_df['season'].replace(season_labels)
    ride_hr_df['weather'] = ride_hr_df['weather'].replace(weather_labels)
    return ride_hr_df

def find_max_value(df,types):
    max_total = df[types].max()
    max_row = df[df[types] == max_total]
    max_season = max_row["season"].iloc[0]
    max_weather = max_row["weather"].iloc[0]
    return max_season,max_weather,max_total

def create_list_with_index(n, specified_index):
    my_list = []
    for i in range(n):
        if i == specified_index:
            my_list.append(0.1)
        else:
            my_list.append(0)
    return my_list

# Memasukan dataset yang sudah diolah pada notebook
hour_df = pd.read_csv("dashboard/hour_data.csv")
day_df = pd.read_csv("dashboard/day_data.csv")
hour_df = create_timestamp_df(hour_df)
hour_df.sort_values(by="timestamp", inplace=True)
hour_df.reset_index(inplace=True)

min_date = hour_df['timestamp'].min()
max_date = hour_df['timestamp'].max()

# Membuat menu filter rentang waktu
with st.sidebar:
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Memfilter dataset sesuai rentang waktu yang dipilih
main_hour_df = hour_df[(hour_df["timestamp"] >= str(start_date)) & 
                (hour_df["timestamp"] <= str(end_date))]
main_day_df = day_df[(day_df["timestamp"] >= str(start_date)) & 
                (day_df["timestamp"] <= str(end_date))]
# Membuat seluruh dataset yang ada helper functionnya
working_df = create_working_df(main_day_df)
holiday_df = create_holiday_df(main_day_df)
weather_df = create_weather_df(main_hour_df)
season_df = create_season_df(main_hour_df)
season_weather_df = create_season_weather_df(main_hour_df)

st.header(':bike: Bicycle Ride Dashboard :bike:')

# Membuat bagian Hourly Ride, menunjukan Ride secara time series
st.subheader('Hourly Ride')

col1, col2, col3 = st.columns(3)
 
with col1:
    total_average = main_hour_df.cnt.mean()
    total_average_str = format(total_average,'.2f')
    st.metric("Total Average Ride", value=total_average_str + " Rides")
 
with col2:
    casual_average = main_hour_df.casual.mean()
    casual_average_str = format(casual_average,'.2f')
    st.metric("Average Casual Rider", value=casual_average_str + " Rides")
 
with col3:
    register_average = main_hour_df.registered.mean()
    registered_average_str = format(register_average,'.2f')
    st.metric("Average Registered Rider", value=registered_average_str + " Rides")
 
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

# Mendefinisikan batas musim
season_boundaries = hour_df['season'].unique().tolist()
season_boundaries.sort()

# Mendefinisikan pewarnaan dan label dari tiap musim
season_colors = ['springgreen', 'gold', 'indianred', 'skyblue']
season_labels =['Spring','Summer','Fall','Winter']

for i, season in enumerate(season_boundaries):
    season_data = main_hour_df[main_hour_df['season'] == season]
    ax1.plot(season_data['timestamp'], season_data['casual'], label=season_labels[i], color=season_colors[i])
    ax2.plot(season_data['timestamp'], season_data['registered'], label=season_labels[i], color=season_colors[i])

ax1.set_ylabel('Casual Count')
ax2.set_ylabel('Registered Count')
ax2.set_xlabel('Timestamp')
ax1.set_title('Timestamp vs Casual Count (By Hour)')
ax2.set_title('Timestamp vs Registered Count (By Hour)')
ax1.legend()
ax2.legend()
 
st.pyplot(fig)

# Membuat bagian Season and Weather Rides, menunjukan rata-rata tertinggi dari tiap jenis rider
st.subheader("Season and Weather Rides")
# Melakukan groupby untuk mencari nilai rata-ratanya
grouped_weather_season = season_weather_df.groupby(by=['season','weather']).mean()
check_group = grouped_weather_season.reset_index()

# Mencari nilai tertinggi untuk total, casual, dan registered
tot_season,tot_weather,tot_value = find_max_value(check_group, "total")
cas_season,cas_weather,cas_value = find_max_value(check_group, "casual")
reg_season,reg_weather,reg_value = find_max_value(check_group, "registered")
col1,col2,col3 = st.columns(3)
with col1:
    # Menunjukan nilai average total ride terbanyak
    value_str = format(tot_value,'.2f')
    st.metric(("Highest Total Average Ride"), value=value_str + " Rides")
with col2:
    # Menunjukan nilai average casual ride terbanyak
    value_str = format(cas_value,'.2f')
    st.metric(("Highest Casual Average Ride"), value=value_str + " Rides")
with col3:
    # Menunjukan nilai average registered ride terbanyak
    value_str = format(reg_value,'.2f')
    st.metric(("Highest Registered Average Ride"), value=value_str + " Rides")
    
col1,col2,col3 = st.columns(3)
with col1:
    # Menunjukan musim dengan Total Ride terbanyak
    st.metric(("Season"), value=tot_season)
with col2:
    # Menunjukan musim dengan Casual Ride terbanyak
    st.metric(("Season"), value=cas_season)
with col3:
    # Menunjukan musim dengan Registered Ride terbanyak
    st.metric(("Season"), value=reg_season)
    
col1,col2,col3 = st.columns(3)
with col1:
    # Menunjukan cuaca dengan Total Ride terbanyak
    st.metric(("Weather"), value=tot_weather)
with col2:
    # Menunjukan cuaca dengan Casual Ride terbanyak
    st.metric(("Weather"), value=cas_weather)
with col3:
    # Menunjukan cuaca dengan Registered Ride terbanyak
    st.metric(("Weather"), value=reg_weather)

# create a list of colors for the bar chart
colors = ['lightblue', 'orange', 'green']

# Membuat 4 subplots untuk menunjukan rata-rata tiap musim
col1,col2 = st.columns(2)
with col1:
    fig, ax = plt.subplots(figsize=(10,10))
    sub_df = grouped_weather_season.loc["Spring"]
    if sub_df.empty:
        st.text("No data found!")
    sub_df.plot.bar(ax=ax, color=colors, rot=90)
    ax.set_title("Spring")
    ax.legend(loc='upper right')
    st.pyplot(fig)
with col2:
    fig, ax = plt.subplots(figsize=(10,10))
    sub_df = grouped_weather_season.loc["Summer"]
    sub_df.plot.bar(ax=ax, color=colors, rot=90)
    ax.set_title("Summer")
    ax.legend(loc='upper right')
    st.pyplot(fig)
col1,col2 = st.columns(2)
with col1:
    fig, ax = plt.subplots(figsize=(10,10))
    sub_df = grouped_weather_season.loc["Fall"]
    sub_df.plot.bar(ax=ax, color=colors, rot=90)
    ax.set_title("Fall")
    ax.legend(loc='upper right')
    st.pyplot(fig)
with col2:
    fig, ax = plt.subplots(figsize=(10,10))
    sub_df = grouped_weather_season.loc["Winter"]
    sub_df.plot.bar(ax=ax, color=colors, rot=90)
    ax.set_title("Winter")
    ax.legend(loc='upper right')
    st.pyplot(fig)
    
# Membuat plot Clear dan Cloudy, menunjukan rata-rata total ride
st.subheader("Clear and Cloudy Total Ride")
col1, col2 = st.columns(2)

clear_weather = check_group[check_group['weather'] == 'Clear']['total']
cloudy_weather = check_group[check_group['weather'] == 'Cloudy']['total']
print(clear_weather)
print(cloudy_weather)

# Mengambil nilai tertinggi dan membuat list 'explode'nya
max_index_clear = cloudy_weather.idxmax()
max_index_cloud = clear_weather.idxmax()
explode = create_list_with_index(4,max_index_cloud)

with col1:
    fig, ax = plt.subplots(figsize=(25, 10))
    ax.pie(x=clear_weather, labels=season_labels,
            autopct='%1.1f%%',
            colors=season_colors,
            explode=explode)
    ax.set_title('Clear Weather Total Ride per Season')
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(25, 10))
    ax.pie(x=cloudy_weather, labels=season_labels,
            autopct='%1.1f%%',
            colors=season_colors,
            explode=explode)
    ax.set_title('Cloudy Weather Total Ride per Season')
    st.pyplot(fig)

# Membuat bagian Holiday vs Non-Holiday, untuk membandingkan rata-rata ride kedua jenis hari
st.subheader("Holiday vs Non-Holiday")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
ax1.set_ylim(0, 5000)
ax2.set_ylim(0, 5000)
sns.barplot(data=working_df, x="workingday", y="value", hue="user_type", errorbar=None, ax=ax2)
sns.barplot(data=holiday_df, x="holiday", y="value", hue="user_type", errorbar=None, ax=ax1)
ax1.legend(loc='upper left')
ax2.legend(loc='upper left')
st.pyplot(fig)