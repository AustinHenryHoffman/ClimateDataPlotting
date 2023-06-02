import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector
from datetime import timedelta

# Establish a connection to the database
conn = mysql.connector.connect(
    host="192.168.1.4",
    user="Dr.Tautology",
    password="SmidgeCat12516!",
    database="home_thermostat"
)

# Create a cursor object
cursor = conn.cursor()

# Execute the select query
query = "SELECT date, time, temperature, humidity FROM house_climate_data WHERE location = 'Master Bedroom'"
cursor.execute(query)

# Fetch the data
data = cursor.fetchall()

# Create a DataFrame
df = pd.DataFrame(data, columns=["date", "time", "temperature", "humidity"])

# Convert 'date' column to datetime format
df['date'] = pd.to_datetime(df['date'])

# Convert 'time' column to timedelta format
df['time'] = pd.to_timedelta(df['time'])

# Combine date and time columns into a single datetime column
df['datetime'] = df['date'] + df['time']

# Set the datetime column as the index
df = df.set_index("datetime")

# Set the figure size and adjust the margins
plt.figure(figsize=(10, 6))
plt.subplots_adjust(bottom=0.15)

# Plot the temperature and humidity
plt.plot(df.index, df["temperature"], label="Temperature")
plt.plot(df.index, df["humidity"], label="Humidity")

# Set the x-axis label
plt.xlabel("Date and Time")

# Set the y-axis label
plt.ylabel("TempF/Humidity%")

# Set the title
plt.title("Temperature and Humidity in Master Bedroom")

# Rotate x-axis labels for better visibility
plt.xticks(rotation=45, fontsize=6)

# Show the legend
plt.legend()

# Save the figure as an image instead of displaying it on screen
plt.savefig('./MasterBedroomGraph.png')

# Display the graph
plt.show()

# Close the cursor and the connection
cursor.close()
conn.close()