# IS 452 Final Project
# A Flight Information Board for Travelers
# Te Lin, telin2, 4CR




import requests, urllib, json, sys
from urllib.request import urlopen
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QInputDialog, QLineEdit
from PyQt5.QtCore import pyqtSlot


#  retrieveFlightData function sends my authentication info to FlightAware, and return 15 departure flights.
def retrieveFlightData(airportcode):
    username = "ritalin316"
    apiKey = "f1cb7dfee81dbdfeb18a6919dcd369b6a5bfdc40"
    fxmlUrl = "https://flightxml.flightaware.com/json/FlightXML3/"

    # This section is built with references from flightaware website.
    # link: http://flightaware.com/commercial/flightxml/v3/apiref.rvt
    # "airport_code": input - airport ICAO id; output - city, country, direction, etc.
    # "type": decides what information I receive from flightaware.
    # "howMany": (Optional) Number of flights to fetch, per type.
    payload = {'airport_code': airportcode, 'type': 'departures', 'howMany': '15'}

    # "AirportBoards" returns the flights scheduled, departing, enroute, and arriving at a specified airport.
    response = requests.get(fxmlUrl + "AirportBoards", params=payload, auth=(username, apiKey))

    # 200 is a HTTP status code, it means "OK"
    if response.status_code == 200:
        result_data = response.json()
    else:
        print("Error executing request")

    return result_data


#  buildFlightInfo function analyze the information input, and organize it into a long list, consisting of 15 lists.
#  Each list consists of information of a flight for display.
def buildFlightInfo(data):
    rootdata = data['AirportBoardsResult']['departures']['flights']
    flightinfolist = []

    #  from the raw data retrieved from Flight Aware, I cut out everything I need and append to a list
    for i in range(0, 15):
        epoch_scheduled_dept_time = rootdata[i]['filed_departure_time']['epoch']
        scheduled_dept_time = rootdata[i]['filed_departure_time']['time']
        delay = rootdata[i]['estimated_departure_time']['time']
        if delay == scheduled_dept_time:
            delay = ''
        cancelled = rootdata[i]['cancelled']
        flight_number = rootdata[i]['ident']
        aircraft_type = rootdata[i]['aircrafttype']
        dest_airport = rootdata[i]['destination']['airport_name']
        dest_city = rootdata[i]['destination']['city']
        Estimated_arrival_time = rootdata[i]['estimated_arrival_time']['time']
        if cancelled == False:
            cancelled = "Normal"
        else:
            cancelled = "Cancelled"
            Estimated_arrival_time = "TBD"
        flightinfo = [epoch_scheduled_dept_time, scheduled_dept_time, delay, flight_number, aircraft_type, dest_airport,
                      dest_city, cancelled, Estimated_arrival_time]
        flightinfolist.append(flightinfo)

    # sort lists in flightinfolist by the value of the first item in each list (departure epoch time)
    flightinfolist.sort(key=lambda x: x[0])
    return flightinfolist


#  this function retrieves weather information from Yahoo Weather API: https://developer.yahoo.com/weather/
def retrieveWeather(city):
    baseurl = "https://query.yahooapis.com/v1/public/yql?"
    # Yql is Yahoo Query Language, which worked like SQL. It allows me query, filter, and join data from Web services.
    yql_query = 'select item.condition from weather.forecast where woeid in (select woeid from geo.places(1) where text="' + city + '")'
    yql_url = baseurl + urllib.parse.urlencode({'q': yql_query}) + "&format=json"
    result = urlopen(yql_url).read()
    data = json.loads(result)
    weather = str(data['query']['results']['channel']['item']['condition']['temp']) + 'F, ' + str(
        data['query']['results']['channel']['item']['condition']['text'])
    return weather


#  addWeather function add weather retrieved from Yahoo Weather API to the flight data.
def addWeather(flightlist):
    for flightinfo in flightlist:
        acity = flightinfo[6]
        flightinfo.append(retrieveWeather(acity))
    return flightlist


#  build flight information and destination weather according to input parameter airport_code
def dataMain(airport_code):
    flight_data = retrieveFlightData(airport_code)
    list_flight_info = buildFlightInfo(flight_data)
    list_flight_weather = addWeather(list_flight_info)
    return list_flight_weather


#  I created this graphical user interface based on the following tutorials:
#  https://evileg.com/en/post/236/
#  https://pythonspot.com/pyqt5/

class App(QWidget):

    # creates a PyQT5 window, defines title, location, width, height of a window, and calls flightUI
    def __init__(self):
        super().__init__()
        self.title = 'Flight Information Board'
        self.left = 20
        self.top = 30
        self.width = 1200
        self.height = 800
        self.flightUI()


    #  shows a window with defined features
    def flightUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.infoTable()
        # Add box layout, add table to box layout and add box layout to widget
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)
        # Show widget
        self.show()


    #  creates a dialog window, prompt for user input, and pass the input as an argument to dataMain() function.
    def getText(self):
        text, okPressed = QInputDialog.getText(self,
                                               "Airport Code",
                                               "Type an ICAO code (e.g. KORD for O'Hare International Airport"
                                               "Airport, KBOS for Boston Logan International Airport)",
                                               QLineEdit.Normal, "")
        if okPressed and text != '':
            info = dataMain(text)
            return info

    #  creates a table with 15 rows and 9 columns, assigns headers,
    #  and passes value stored in flightinfolist to the table
    def infoTable(self):
        # Create table
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(15)
        self.tableWidget.setColumnCount(9)
        self.tableWidget.setHorizontalHeaderLabels(["Sched. Dept. Time", "Est. Dept. Time",
                                                    "Flight #", "Aircraft Type",
                                                    "Dest. Airport", "Dest. City",
                                                    "Cancellation", "ETA", "Dest. Weather"])
        info = self.getText()
        for i in range(0, 15):
            for j in range(0, 9):
                self.tableWidget.setItem(i, j, QTableWidgetItem(info[i][j + 1]))
        self.tableWidget.move(0, 0)


#   main function: execute the App application,
#   receives events from the window system, dispatches them to the application widgets
#   and exit finally.
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

