from flask import Flask, render_template, url_for, request, redirect
from markupsafe import Markup
import requests
import config
import numpy as np
import pandas as pd
from crop_prediction import RF
from utils.fertilizer import fertilizer_dic
from database import mydb
import serial
import time
import numpy as np
import socket
import threading


app = Flask(__name__)

app.secret_key = "Sanjeev@123"


################################# login ###########################33
@app.route("/")
def login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_data():
    data = request.form
    sql = """ select password from grow_farmer.user where email = %s"""
    value = (data['username'],)
    cursor = mydb.cursor()
    cursor.execute(sql, value)
    passwd = cursor.fetchone()
    if passwd is not None and passwd[0] == data["password"]:
        return redirect('/home')
    else:
        return redirect("/")


@app.route('/home')
def home():
    return render_template("home.html")
################################# sign up ############################
@app.route("/sign-up")
def sign_up():
    return render_template("singup.html")


@app.route("/register",methods=["POST"])
def register():
    data = request.form
    sql = " insert into grow_farmer.user (name,email,password,mobile,city,state) values (%s, %s, %s, %s, %s, %s)"
    value = (data['name'], data['email'], data['password'], data['phone'], data['city'], data['state'])
    cursor = mydb.cursor()
    cursor.execute(sql, value)
    cursor.close()
    mydb.commit()
    return redirect("/")


################################ crop recommendation ##########################3
def weather_fetch(city_name):
    """
    Fetch and returns the temperature and humidity of a city
    :params: city_name
    :return: temperature, humidity
    """
    api_key = '0f922ae1ca8f2aa5427a261af80f0937'
    base_url = "https://api.openweathermap.org/data/2.5/weather?"

    complete_url = base_url + "q=" + city_name + "&appid=" + api_key
    response = requests.get(complete_url)
    x = response.json()
    if x["cod"] != "404":
        y = x['main']

        temperature = round((y["temp"] - 273.15), 2)
        humidity = y["humidity"]

        return temperature, humidity
    else:
        return None


@app.route("/crop-recommend")
def crop_recommendation():
    return render_template("crop_recommendation.html")


@app.route("/crop-predict", methods=['POST'])
def crop_predict():
    input_arr=[]
    n = int(request.form['nitrogen'])
    p = int(request.form['phosphorous'])
    k = int(request.form['pottasium'])
    ph = int(request.form['ph'])
    rainfall = int(request.form['rainfall'])
    city = request.form.get('city')
    if weather_fetch(city) is not None:
        temperature, humidity = weather_fetch(city)
        arr = np.array([[n, p, k, temperature, humidity, ph, rainfall]])
        res = RF.predict(arr)
        return render_template("crop_result.html", prediction=res[0])
    else:
        return render_template("try_again.html")


############################### fertilizer recommendation #######################
@app.route("/fert-recommend")
def fert_recommend():
    return render_template("fertilizer_pred.html")


@ app.route('/fertilizer-predict', methods=['POST'])
def fert_predict():

    crop_name = str(request.form['cropname'])
    N = int(request.form['nitrogen'])
    P = int(request.form['phosphorous'])
    K = int(request.form['pottasium'])
    # ph = float(request.form['ph'])

    df = pd.read_csv(r'dataset/fertilizer.csv')

    nr = df[df['Crop'] == crop_name]['N'].iloc[0]
    pr = df[df['Crop'] == crop_name]['P'].iloc[0]
    kr = df[df['Crop'] == crop_name]['K'].iloc[0]

    n = nr - N
    p = pr - P
    k = kr - K
    temp = {abs(n): "N", abs(p): "P", abs(k): "K"}
    max_value = temp[max(temp.keys())]
    if max_value == "N":
        if n < 0:
            key = 'NHigh'
        else:
            key = "Nlow"
    elif max_value == "P":
        if p < 0:
            key = 'PHigh'
        else:
            key = "Plow"
    else:
        if k < 0:
            key = 'KHigh'
        else:
            key = "Klow"

    response = Markup(str(fertilizer_dic[key]))

    return render_template('fertilizer_res.html', recommendation=response)


############################# disease prediction ############################
@app.route("/disease-pred")
def disease_prediction():
    return render_template("disease_pred.html")


############################## sensor data ##################################
def read_data_from_arduino(port, baudrate):
    ser = serial.Serial(port, baudrate, timeout=1)
    time.sleep(1)
    return ser


def get_data():
    port = 'COM5'  # Adjust the port as necessary
    baudrate = 9600

    ser = read_data_from_arduino(port, baudrate)

    try:
        arr = []
        i = 0
        while i < 30:
            if ser.in_waiting > 0:
                # Read a line of data from the serial port
                line = ser.readline().decode('utf-8').strip()
                i += 1
                # Ensure the data line is not empty
                if not line:
                    continue
                res = line.split(',')

                # Check if the data has at least 4 elements (N, P, K, and moisture)
                if len(res) < 4:
                    continue
                else:
                    try:
                        temp = list(map(float, line.split(',')))
                        arr.append(temp)
                    except ValueError as e:
                        print(f"Error converting data to float: {e}")

                # Short delay between readings
                time.sleep(0.01)

        # Convert the list to a NumPy array
        nparr = np.array(arr)
        # Calculate the mean along the columns
        col_means = np.mean(nparr, axis=0)
        nparr_rounded = np.round(col_means, decimals=2)
        nparr_rounded[3] = (nparr_rounded[3] / 1023) * 100
        return nparr_rounded

    except KeyboardInterrupt:
        print("Stopping the program.")
    finally:
        ser.close()


@app.route("/sensor-data")
def sensor_data():
    res = get_data()
    return render_template("sensor.html", data=res)



################################################## community #####################################
@app.route("/community")
def farmer_community():
    return render_template("chat_comm.html")

############################ about us #######################################
@app.route("/about")
def about_us():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
