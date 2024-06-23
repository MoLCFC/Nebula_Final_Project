import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import pandas as pd
from db import connect_to_db, insert_weather_data, fetch_data
from db import fetch_data_to_dataframe, clean_and_transform, aggregate_data
from matplot import plot_temperature_trends, plot_temperature_comparison, save_plot



def fetch_weather_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch web page. Status code: {response.status_code}")

# Example usage
url = "https://forecast.weather.gov/MapClick.php?lat=37.7772&lon=-122.4168"
page_content = fetch_weather_page(url)

#Parsing the wesbite using beautfiul soup
def parse_weather_data(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    # Modify the selector based on the data you need
    forecast_items = soup.find_all('div', class_='tombstone-container')
    weather_data = []
    for item in forecast_items:
        period = item.find('p', class_='period-name').get_text()
        short_desc = item.find('p', class_='short-desc').get_text()
        temp = item.find('p', class_='temp').get_text()
        weather_data.append({'period': period, 'short_desc': short_desc, 'temp': temp})
    return weather_data

try:
    page_content = fetch_weather_page(url)
    weather_data = parse_weather_data(page_content)
except Exception as e:
    print(f"An error occurred: {e}")

#Used to import functions from db.py file 
db_connection = connect_to_db()
df = fetch_data_to_dataframe(db_connection)
df_cleaned = clean_and_transform(df)
df_aggregated = aggregate_data(df_cleaned)

# To save to CSV
df_aggregated.to_csv('processed_weather_data.csv', index=False)

# To save back to the database (assuming a new table for processed data)
def save_processed_data(connection, dataframe):
    dataframe.to_sql('processed_weather_forecasts', con=connection, if_exists='replace', index=False)
    print("Processed data saved to the database successfully")


# fetching the data and inserting it into the database
fetch_data(db_connection)
insert_weather_data(db_connection,weather_data)


# Example usage with the db_connection from the previous steps
#print(df.head())

# Clean and transform the DataFrame
#print(df_cleaned.head())\

# Aggregate the cleaned data
#print(df_aggregated)

# If reading from a CSV file
df = pd.read_csv('processed_weather_data.csv')

# Or, if loading directly from the database, you can use the previous function to load data to DataFrame


# Call the function with the aggregated DataFrame
plot_temperature_trends(df)
# Call the function with the DataFrame
plot_temperature_comparison(df)

# Call the save function
save_plot(df)


#Flask operations



    