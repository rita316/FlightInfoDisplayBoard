# A Flight Information Board for Travelers
The purpose of this project was to create a flight information board that meant to provide flights and destination weathers for travelers in a particular airport a user requested (and also is my first python project).

#### This project was divided into three parts:
## Part 1: Data Collection
API provided by Flight Aware (https://flightaware.com/commercial/flightxml/)

The "retrieveFlightData" function sends my authentication info to FlightAware, and returns 15 departure flights.

The "retrieveWeather" function retrieves weather information from the Yahoo Weather API: https://developer.yahoo.com/weather/ .

Yql is Yahoo Query Language, which worked like SQL. It allows me query, filter, and join data from Web services.

## Part 2: Data Processing 
The "buildFlightInfo" function analyze the information input, and organize it into a long list, consisting of 15 lists.
Each list consists of information of a flight for display.

From the raw data retrieved from Flight Aware, I cut out everything I need and append to a list.

Then I sort lists in flightinfolist by the value of the first item in each list (departure epoch time).

The "addWeather" function adds weather retrieved from Yahoo Weather API to the flight data.
The "dataMain" function builds flight information and destination weather according to input parameter airport_code.

## Part 3: User Interface
I created this graphical user interface based on the following tutorials:
https://evileg.com/en/post/236/
https://pythonspot.com/pyqt5/

First, it initializes the PyQT5 window, defines title, location, width, height of a window, and calls the "flightUI" function. 

Then the "flightUI" shows a window with defined features. 

Later, the "getText" function creates a dialog window, prompt for user input, and pass the input as an argument to dataMain() function, and the "infoTable" function creates a table with 15 rows and 9 columns, assigns headers, and passes value stored in flightinfolist to the table.

Main function: execute the App application, receives events from the window system, dispatches them to the application widgets
and exit finally.
