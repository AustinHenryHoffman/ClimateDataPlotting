# Using flask to make an api
# import necessary libraries and functions
from flask import Flask, jsonify, request, send_from_directory
import datetime as dt
import mysql.connector
import subprocess
import os
# creating a Flask app
app = Flask(__name__)
connection = mysql.connector.connect(host='192.168.1.4', user='Dr.Tautology', password='SmidgeCat12516!', database='home_thermostat')


@app.route('/datetime', methods=['GET'])
def home():
    if(request.method == 'GET'):

        date = dt.datetime.now().strftime('%Y-%m-%d')
        time = dt.datetime.now().strftime('%H:%M:%S')
        return jsonify({'date': date, 'time': time})


@app.route('/climate', methods=['POST'])
def handle_request():
    data = request.get_json()
    connection = mysql.connector.connect(host='192.168.1.4', user='Dr.Tautology', password='SmidgeCat12516!', database='home_thermostat')
    insert_query = "INSERT INTO house_climate_data(date, time, temperature,humidity,location) VALUES (%s, %s, %s, %s, %s)"
    values = (data['date'], data['time'], data['temperature'], data['humidity'], data['location'])
    cursor = connection.cursor()
    cursor.execute(insert_query, values)
    connection.commit()
    cursor.close()
    connection.close()
    return 'Success'


@app.route('/masterbedroom')
def send_image():
    # Replace './images' with the actual directory path where your images are located
    images_dir = '/home/Dr.Tautology/ClimateDataPlotting/ClimateDataPlotting/images/'
    subprocess.run(['python', '/home/Dr.Tautology/ClimateDataPlotting/ClimateDataPlotting/graph_climate.py'])
    # Get the list of files in the directory
    image_files = os.listdir(images_dir)
    # Filter the files to only include those starting with "Master_Bedroom"
    filtered_files = [filename for filename in image_files if filename.startswith("Master_Bedroom")]
    # Sort the filtered files based on modification time (newest first)
    sorted_files = sorted(filtered_files, key=lambda x: os.path.getmtime(os.path.join(images_dir, x)), reverse=True)

    # Check if any matching files were found
    if sorted_files:
        # Get the newest file
        newest_file = sorted_files[0]
        # Construct the full path to the image file
        image_path = os.path.join(images_dir, newest_file)
        # Send the file
        return send_from_directory(images_dir, newest_file, as_attachment=True)
    else:
        return "No matching image file found."


@app.route('/livingroom')
def send_image():
    # Replace './images' with the actual directory path where your images are located
    images_dir = '/home/Dr.Tautology/ClimateDataPlotting/ClimateDataPlotting/images/'
    subprocess.run(['python', '/home/Dr.Tautology/ClimateDataPlotting/ClimateDataPlotting/graph_climate.py'])
    # Get the list of files in the directory
    image_files = os.listdir(images_dir)
    # Filter the files to only include those starting with "Master_Bedroom"
    filtered_files = [filename for filename in image_files if filename.startswith("Living_Room")]
    # Sort the filtered files based on modification time (newest first)
    sorted_files = sorted(filtered_files, key=lambda x: os.path.getmtime(os.path.join(images_dir, x)), reverse=True)

    # Check if any matching files were found
    if sorted_files:
        # Get the newest file
        newest_file = sorted_files[0]
        # Construct the full path to the image file
        image_path = os.path.join(images_dir, newest_file)
        # Send the file
        return send_from_directory(images_dir, newest_file, as_attachment=True)
    else:
        return "No matching image file found."


@app.route('/secondbedroom')
def send_image():
    # Replace './images' with the actual directory path where your images are located
    images_dir = '/home/Dr.Tautology/ClimateDataPlotting/ClimateDataPlotting/images/'
    subprocess.run(['python', '/home/Dr.Tautology/ClimateDataPlotting/ClimateDataPlotting/graph_climate.py'])
    # Get the list of files in the directory
    image_files = os.listdir(images_dir)
    # Filter the files to only include those starting with "Master_Bedroom"
    filtered_files = [filename for filename in image_files if filename.startswith("Second_Bedroom")]
    # Sort the filtered files based on modification time (newest first)
    sorted_files = sorted(filtered_files, key=lambda x: os.path.getmtime(os.path.join(images_dir, x)), reverse=True)

    # Check if any matching files were found
    if sorted_files:
        # Get the newest file
        newest_file = sorted_files[0]
        # Construct the full path to the image file
        image_path = os.path.join(images_dir, newest_file)
        # Send the file
        return send_from_directory(images_dir, newest_file, as_attachment=True)
    else:
        return "No matching image file found."


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000, debug=True)
