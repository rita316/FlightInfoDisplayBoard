# A Flight Information Board for Travelers
The purpose of this project was to create a flight information board that meant to provide flights and destination weathers for travelers in a particular airport a user requested (and also is my first python project).

#### This project was divided into three parts:
## Part 1: Data Collection
API provided by Flight Aware (https://flightaware.com/commercial/flightxml/)
retrieveFlightData function sends my authentication info to FlightAware, and return 15 departure flights.
this function retrieves weather information from Yahoo Weather API: https://developer.yahoo.com/weather/
Yql is Yahoo Query Language, which worked like SQL. It allows me query, filter, and join data from Web services.

## Part 2: Data Processing 
buildFlightInfo function analyze the information input, and organize it into a long list, consisting of 15 lists.
Each list consists of information of a flight for display.
from the raw data retrieved from Flight Aware, I cut out everything I need and append to a list
sort lists in flightinfolist by the value of the first item in each list (departure epoch time)
The addWeather function add weather retrieved from Yahoo Weather API to the flight data.
build flight information and destination weather according to input parameter airport_code

## Part 3: User Interface
I created this graphical user interface based on the following tutorials:
https://evileg.com/en/post/236/
https://pythonspot.com/pyqt5/
creates a PyQT5 window, defines title, location, width, height of a window, and calls flightUI
shows a window with defined features
creates a dialog window, prompt for user input, and pass the input as an argument to dataMain() function.
creates a table with 15 rows and 9 columns, assigns headers,
and passes value stored in flightinfolist to the table
main function: execute the App application,
receives events from the window system, dispatches them to the application widgets
and exit finally.
