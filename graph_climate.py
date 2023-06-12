import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import mysql.connector
import datetime as t
from PIL import Image
import os
matplotlib.use('Agg')


def create_graphs(dates="today", rooms="All"):
    plt.ioff()
    if rooms == "All":
        rooms = ["Master Bedroom", "Second Bedroom", "Living Room"]
    location = [i for i in rooms]
    print(location)

    if dates == "today":
        today = t.datetime.now().strftime('%Y-%m-%d')
    else:
        today = t.datetime.now().strftime('%Y-%m-%d')

    for room in location:
        print(room.replace(" ", "_"))
        # Establish a connection to the database
        conn = mysql.connector.connect(
            host="192.168.1.4",
            user="Dr.Tautology",
            password="SmidgeCat12516!",
            database="home_thermostat"
        )
        cursor = conn.cursor()
        query = f"SELECT date, time, temperature, humidity FROM home_thermostat.house_climate_data WHERE location ='{room}' and date='{today}'"
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

        plt.figure(figsize=(figure_width / dpi, figure_height / dpi), dpi=dpi)

        plt.subplots_adjust(bottom=0.2)

        # Plot the temperature and humidity
        plt.plot(df.index, df["temperature"], label="Temperature")
        plt.plot(df.index, df["humidity"], label="Humidity")

        # Set the x-axis label
        plt.xlabel("Date and Time")

        # Set the y-axis label
        plt.ylabel("TempF/Humidity%")

        # Set the title
        plt.title(f"Temperature and Humidity in {room}")

        # Rotate x-axis labels for better visibility
        plt.xticks(rotation=45, fontsize=6)

        # Show the legend
        plt.legend()
        datetime = t.datetime.now().strftime('%d%m%y%H%M%S')

        # Save the figure as an image instead of displaying it on screen
        plt.savefig(f'/home/Dr.Tautology/ClimateDataPlotting/ClimateDataPlotting/images/{room.replace(" ", "_")}_{datetime}.png', dpi=dpi)
        plt.close('all')
        # Close the cursor and the connection
        cursor.close()
        conn.close()

        # Open the saved image using PIL
        with Image.open(f'/home/Dr.Tautology/ClimateDataPlotting/ClimateDataPlotting/images/{room.replace(" ", "_")}_{datetime}.png', 'r') as image:
            # Resize the image
            # width x height
            resized_image = image.resize((320, 240), Image.ANTIALIAS)
            resized_image.save(f'/home/Dr.Tautology/ClimateDataPlotting/ClimateDataPlotting/images/{room.replace(" ","_")}_{datetime}_240x320.png')
            os.remove(f'/home/Dr.Tautology/ClimateDataPlotting/ClimateDataPlotting/images/{room.replace(" ","_")}_{datetime}.png')


if __name__ == "__main__":
    create_graphs()
