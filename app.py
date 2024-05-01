from flask import Flask, send_file, jsonify, render_template_string
import matplotlib.pyplot as plt
import io
import psycopg2
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()  # Load environment variables from the .env file
app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(os.environ['DATABASE_URL'])

def create_temperature_plot():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT period, temperature, scraped_at
        FROM weather_forecasts
        WHERE scraped_at >= current_date - INTERVAL '7 days'
        ORDER BY scraped_at;
    """)
    data = cur.fetchall()
    cur.close()
    conn.close()

    df = pd.DataFrame(data, columns=['period', 'temperature', 'scraped_at'])
    df['temperature'] = df['temperature'].str.extract('(\d+)').astype(int)
    df['scraped_at'] = pd.to_datetime(df['scraped_at']).dt.date

    fig, ax = plt.subplots()
    ax.plot(df['scraped_at'], df['temperature'], marker='o', linestyle='-')
    ax.set(title='Weekly Temperature Trends', xlabel='Date', ylabel='Temperature (°F)')
    ax.grid(True)
    return fig, df

@app.route('/temperature_trends')
def temperature_trends():
    fig, _ = create_temperature_plot()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

@app.route('/temperature_table')
def temperature_table():
    _, df = create_temperature_plot()
    # Render DataFrame as HTML table
    html_table = df.to_html(classes='table table-striped table-hover', index=False)
    return render_template_string("""
        <html>
            <head>
                <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/css/bootstrap.min.css">
                <title>Temperature Data</title>
            </head>
            <body>
                <h1>Temperature Table</h1>
                {{ table|safe }}
            </body>
        </html>
        """, table=html_table)

@app.route('/temperature_chart')
def temperature_chart():
    fig, df = create_temperature_plot()
    # Optionally create another style of chart, here we'll use a bar chart
    fig, ax = plt.subplots()
    ax.bar(df['scraped_at'], df['temperature'], color='blue')
    ax.set(title='Weekly Temperature Bar Chart', xlabel='Date', ylabel='Temperature (°F)')
    ax.grid(True)
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return send_file(buf, mimetype='image/png')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
