# Bicycle Ride Dashboard
This dashboard is an interactive dashboard that tells about Bike Ride average in various condition, taken from January 2011 to January 2012. The dashboard provides time filter to filter out specific time range into the data and the insights.
## Streamlit Link
https://yudhasaputra-data-analytics-project-bikesharingdataset.streamlit.app/
## File Contents
```
├───dashboard
| ├───day_data.csv
| ├───hour_data.csv
| └───streamlit.py
├───data
| ├───day.csv
| └───hour.csv
├───notebook.ipynb
├───README.md
└───requirements.txt
```
## Setup environment
```
conda create --name main-ds python=3.8
conda activate main-ds
pip install numpy pandas scipy matplotlib seaborn jupyter streamlit babel
```
## Run steamlit app
```
streamlit run dashboard/streamlit.py
```
## Streamlit Dashboard Screenshot

<img width="1280" alt="dash1" src="https://github.com/yudhasaputra/Data-Analytics-Project-BikeSharingDataset/assets/34949406/aa57d6f5-c34d-470a-b0b5-9998d208def6">
<img width="1280" alt="dash2" src="https://github.com/yudhasaputra/Data-Analytics-Project-BikeSharingDataset/assets/34949406/fc409102-704f-4dbe-9604-92f98483897b">
<img width="1280" alt="dash3" src="https://github.com/yudhasaputra/Data-Analytics-Project-BikeSharingDataset/assets/34949406/7eb98f0e-0a62-4143-a185-7bae653a5e57">
<img width="1280" alt="dash4" src="https://github.com/yudhasaputra/Data-Analytics-Project-BikeSharingDataset/assets/34949406/20c22f4d-fc7b-4db0-b8f5-ff60f2f2fb15">
