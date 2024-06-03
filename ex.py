import requests
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
    print(x)

    if x["cod"] != "404":
        y = x['main']

        temperature = round((y["temp"] - 273.15), 2)
        humidity = y["humidity"]

        print(temperature, humidity)
        return temperature, humidity
    else:
        return None


print(weather_fetch('Bareja'))
