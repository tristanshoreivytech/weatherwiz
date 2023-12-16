import tkinter as tk
from tkinter import messagebox
from tkinter import *

#Required for alt text
from tktooltip import ToolTip
import tkinter.ttk as ttk

#Requires internet access to retrieve weather data
import requests
import json

#Required for PNG, JPEG display capabilities
from PIL import ImageTk, Image

#Important for API access
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

#Defines City weather object
class City:

    def __init__(self, name, weather):
        self.name = name
        self.weather = weather

    #Return float value of current temperature in Celsius
    def getTemp(self):
        return (self.weather["main"]["temp"]-273.15)

    #Return name of city
    def getName(self):
        return self.name

    #Return longitude and latitude of city
    def getCoords(self):
        return (self.weather["coord"])

    #Return integer value of current humidity percentage
    def getHumidity(self):
        return self.weather["main"]["humidity"]

    #Return string single-word description of weather (e.g., "Clouds", "Rain", etc.)
    def getWeather(self):
        return self.weather["weather"][0]["main"]

    def getIcon(self):
        return (self.weather["weather"][0]["icon"])+".png"

#Retrieves weather data via internet and OpenWeatherAPI (Console Version for debugging)
def fetch_weather(city):
    #Retrieve current weather data
    weather_report = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid=3b14c6f7fc323360a6e3c3934f43d46b',headers=headers).text
    #Put weather data into Python dictionary format
    weather = json.loads(weather_report)
    #Checks if City exists
    if (weather["cod"] == "404"):
        print("City does not exist, Please try again.")
    else:
        #Generate city object which can return values for different weather components
        myCity = City(city, weather)
        #print example weather components of city object
        print("{:.1f}".format(weather["main"]["temp"]-273.15) + " degrees Celsius")
        print(myCity.getName())
        print(myCity.getTemp())
        print(myCity.getHumidity())
        print(myCity.getCoords())
        print("The current weather is", myCity.getWeather())

#Retrieves weather data via internet and OpenWeatherAPI
def display_weather(city):
    #Retrieve current weather data
    weather_report = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid=3b14c6f7fc323360a6e3c3934f43d46b',headers=headers).text
    #Put weather data into Python dictionary format
    weather = json.loads(weather_report)
    #Checks if City exists
    if (weather["cod"] == "404"):
        result_label.config(text="Unable to retrieve temperature data (Invalid City).")
    else:
        #Generate city object which can return values for different weather components
        myCity = City(city, weather)
        #Displays appropriate picture depending on weather description
        imgname = myCity.getIcon()
        global imgname2
        imgname2 = ImageTk.PhotoImage(Image.open(imgname))
        label2.config(image = imgname2, bg="light blue")
        label2.photo_ref = imgname2
        #Display Alt Text for image
        ToolTip(label2, msg=myCity.getWeather())
        #Display Text Results of City Weather
        result_label.config(font=("Courier", 10))
        result_label.config(text=f"City: {myCity.getName()}\n"
                                  f"Temperature: "+"{:.1f}".format(myCity.getTemp())+"°C\n"
                                  f"Description: {myCity.getWeather()}\n"
                                  f"Humidity: {myCity.getHumidity()}%\n"
                                  f"Coordinates: {myCity.getCoords()}")

#Performs action when weather button clicked
def get_weather_button_clicked():
    city = city_entry.get()
    #checks to make sure something is entered
    if (city != ""):
        #Creates new window for results of city query
        global results
        results = Toplevel(root, bg="light blue")
        results.title("City Weather")
        results.geometry("400x400")
        #Creates section for text results
        global result_label
        result_label = tk.Label(results, text="")
        #Creates section for image
        global frame2
        frame2 = Frame(results, width=600, height=400)
        frame2.pack()
        frame2.place(anchor='center', relx=0.5, rely=0.5)
        global img2
        #Shows error image by default if invalid city, overridden if valid
        img2 = ImageTk.PhotoImage(Image.open("error.png"))
        global label2
        label2 = Label(frame2, image = img2)
        label2.pack()
        result_label.grid(row=2, column=0, columnspan=2, pady=10)
        #Adds button to return to main WeatherWiz window
        get_exit2_button = tk.Button(results, text="Back to Main Menu", command=results.destroy)
        get_exit2_button.grid(row=8, column=0, columnspan=2, pady=10)
        display_weather(city)

#city=input("Enter the Name of Any City >>  ")
#fetch_weather(city)

# GUI setup
root = tk.Tk()
root.title("WeatherWiz")
frame = Frame(root, width=600, height=400)
frame.pack()
frame.place(anchor='center', relx=0.5, rely=0.5)
img = ImageTk.PhotoImage(Image.open("heaven.jpg"))
label = Label(frame, image = img)
label.pack()
root.geometry("600x600")
#Display Alt Text for image
ToolTip(label, msg="Background Image")

# Widgets
city_label = tk.Label(root, text="Enter City:")
city_entry = tk.Entry(root)
get_weather_button = tk.Button(root, text="Get Weather", command=get_weather_button_clicked)
get_exit_button = tk.Button(root, text="Exit", command=root.destroy)
#result_label = tk.Label(results, text="")

# Layout
city_label.grid(row=0, column=0, padx=10, pady=10)
city_entry.grid(row=0, column=1, padx=10, pady=10)
get_weather_button.grid(row=1, column=0, columnspan=2, pady=10)
get_exit_button.grid(row=2, column=0, columnspan=2, pady=10)
#result_label.grid(row=2, column=0, columnspan=2, pady=10)

# Run the GUI
root.mainloop()
