import matplotlib.pyplot as plt


def plot_temperature_trends(dataframe):
    plt.figure(figsize=(10, 5))  # Set the figure size
    plt.plot(dataframe['forecast_period'], dataframe['temperature'], marker='o')  # Plot a line chart
    plt.title('Temperature Trends Over Time')  # Add a title
    plt.xlabel('Forecast Period')  # Add an x-label
    plt.ylabel('Average Temperature (°F)')  # Add a y-label
    plt.grid(True)  # Add a grid
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    plt.tight_layout()  # Automatically adjust subplot parameters to give specified padding
    plt.show()

def plot_temperature_comparison(dataframe):
    plt.figure(figsize=(10, 5))
    plt.bar(dataframe['forecast_period'], dataframe['temperature'], color='blue')
    plt.title('Comparison of Average Temperatures')
    plt.xlabel('Forecast Period')
    plt.ylabel('Average Temperature (°F)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def save_plot(dataframe):
    plt.figure()
    plt.plot(dataframe['forecast_period'], dataframe['temperature'], marker='o')
    plt.title('Temperature Trends Over Time')
    plt.xlabel('Forecast Period')
    plt.ylabel('Average Temperature (°F)')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    # Save the figure
    plt.savefig('temperature_trends.png')  # You can specify different formats like PDF, SVG, etc.

