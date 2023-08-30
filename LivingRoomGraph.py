import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector
from datetime import timedelta
import datetime as t
from PIL import Image
import json
from pathlib import Path

# Establish a connection to the database
with open("./etc/config.json", "r") as file:
    config_data = json.load(file)
db_info = config_data["db"]
conn = mysql.connector.connect(
    host=db_info["host"],
    user=db_info["user"],
    password=db_info["password"],
    database=db_info["database"]
)

# Create a cursor object
cursor = conn.cursor()
today=t.datetime.now().strftime('%Y-%m-%d')
query = f"SELECT date, time, temperature, humidity FROM house_climate_data WHERE location = 'Living Room' and date='{today}'"
# Execute the select query
#query = "SELECT date, time, temperature, humidity FROM house_climate_data WHERE location = 'Living Room'"
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


# Set the figure size to match the screen resolution
figure_width = 320  # Width of the screen in pixels
figure_height = 240  # Height of the screen in pixels
dpi = 80  # Dots per inch (adjust this value as needed)

#plt.figure(figsize=(figure_width / dpi, figure_height / dpi), dpi=dpi)

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
plt.title("Temperature and Humidity in Living Room")

# Rotate x-axis labels for better visibility
plt.xticks(rotation=45, fontsize=6)

# Show the legend
plt.legend()
datetime = t.datetime.now().strftime('d%m%y%H%M%S')

# Save the figure as an image instead of displaying it on screen
plt.savefig(f'./images/LivingRoom_{datetime}.png',dpi=dpi)

# Display the graph
# plt.show()

# Close the cursor and the connection
cursor.close()
conn.close()
# Open the saved image using PIL

image = Image.open(f'./images/LivingRoom_{datetime}.png')

# Resize the image to 128x128
resized_image = image.resize((128, 128))
resized_image.save(f'./images/LivingRoom_{datetime}_128x128.png')


# Convert the resized image to raw format
#raw_data = resized_image.tobytes()

# Save the raw data to a file
# draw_file_path = f'./LivingRoom_{datetime}_128x128.raw'
# with open(raw_file_path, 'wb') as file:
    # file.write(raw_data)

