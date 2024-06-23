import psycopg2
from psycopg2.extras import RealDictCursor
import pandas as pd

def connect_to_db():
    try:
        # Replace 'dbname', 'user', 'password', and 'host' with your database details 
        connection = psycopg2.connect(
            dbname="Weather_SQL",
            user="Weather_SQL_owner",
            password="M0oVjdTu9gOa",
            host="ep-icy-forest-a5xy6v9q.us-east-2.aws.neon.tech"
        )
        connection.autocommit = True
        print("Connected to the database successfully")
        return connection
    except Exception as e:
        print(f"Error connecting to database: {e}")



def insert_weather_data(db_connection, weather_data):
    cursor = db_connection.cursor()
    query = """
    INSERT INTO weather_forecasts (period, short_desc, temperature)
    VALUES (%s, %s, %s);
    """
    for data in weather_data:
        cursor.execute(query, (data['period'], data['short_desc'], data['temp']))
    print("Data inserted successfully")

def fetch_data(db_connection):
    cursor = db_connection.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM weather_forecasts;")
    records = cursor.fetchall()
    for record in records:
        print(record)


def fetch_data_to_dataframe(connection):
    query = "SELECT * FROM weather_forecasts;"
    dataframe = pd.read_sql_query(query, connection)
    return dataframe

# Example usage with the db_connection from the previous steps

def clean_and_transform(dataframe):
    # Convert temperature to a numerical value
    dataframe['temperature'] = dataframe['temperature'].str.extract('(\d+)').astype(int)

    # Rename columns for clarity
    dataframe.rename(columns={'period': 'forecast_period', 'short_desc': 'description'}, inplace=True)

    # Fill any missing values, if necessary
    dataframe.fillna(method='ffill', inplace=True)

    return dataframe

def aggregate_data(dataframe):
    # Aggregate data by period, finding the average temperature
    aggregated_df = dataframe.groupby('forecast_period').agg({'temperature': 'mean'}).reset_index()
    aggregated_df['temperature'] = aggregated_df['temperature'].round(1)  # round the average temperature to one decimal
    return aggregated_df


