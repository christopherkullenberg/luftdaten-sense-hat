#!/usr/bin/python
from sense_hat import SenseHat
from time import sleep
import requests

sense = SenseHat()
sense.set_rotation(180)

r = [255, 0, 0]
o = [255, 127, 0]
y = [255, 255, 0]
g = [0, 255, 0]
b = [0, 0, 255]
i = [75, 0, 130]
v = [159, 0, 255]
e = [0, 0, 0]

def getdata(sensorid):
    PM10 = {}
    PM2 = {}
    Time = ""
    data = requests.get('http://api.luftdaten.info/v1/sensor/' + str(sensorid)
                        + '/')
    jsonobject = data.json()
    for j in jsonobject:
        Time = j['timestamp']
        PM10[j['sensordatavalues'][0]['value_type']] = j['sensordatavalues'][0]['value']
        PM2[j['sensordatavalues'][1]['value_type']] = j['sensordatavalues'][1]['value']
    return(Time, PM10, PM2)


def cleardisplay():
    print("Clearing display...")
    sense.clear()


def scrolldisplay(sensorid):
    currentdata = getdata(sensorid)
    print("current data: " + str(currentdata))
    Time = currentdata[0]
    PM10 = float(currentdata[1]['P1'])
    PM2 = float(currentdata[2]['P2'])

    if PM10 > 49:
        pm10colour = r
    elif PM10 > 24:
        pm10colour = y
    else:
        pm10colour = g
    print("PM10 " + str(PM10))
    sense.show_message("PM10 " + str(PM10), text_colour=pm10colour)

    if PM2 > 24:
        pm2colour = r
    elif PM2 > 10:
        pm2colour = y
    else:
        pm2colour = g
    print("PM2.5 " + str(PM2))
    sense.show_message("PM2.5 " + str(PM2), text_colour=pm2colour)

    temp = sense.get_temperature()
    print("Temp: " + str(temp))
    if temp > 30:
        tempcolour = r
    elif temp > 24:
        tempcolour = y
    else:
        tempcolour = b
    # sense.show_message("Temp: %s C" % round(temp, 2), text_colour=tempcolour)

    humidity = sense.get_humidity()
    print("Luftfuktighetet:" + str(humidity))
    # sense.show_message("Luftfukt: %s %%rH" % round(humidity, 2), text_colour=v)

    sense.show_message(Time[10:], text_colour=g)
    sense.show_message(" Luftdata.se", text_colour=g)

def startup(sensorid):
    sense.show_message("Booting...", scroll_speed=0.03, text_colour=r)
    #test for internet connection
    if len(getdata(sensorid)) == 3:
        sense.show_message("OK", scroll_speed=0.03, text_colour=g)
        sense.show_message("Press joystick to get data.....", scroll_speed=0.03, text_colour=b)
    else:
        sense.show_message("Network Error", scroll_speed=0.03, text_colour=r)

def run(sensorid):
    print("Waiting for joystick input...")
    event = sense.stick.wait_for_event()
    print("The joystick was {} {}".format(event.action, event.direction))
    sleep(0.1)
    event = sense.stick.wait_for_event(emptybuffer=True)
    print("The joystick was {} {}".format(event.action, event.direction))
    cleardisplay()
    scrolldisplay(sensorid)
