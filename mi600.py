# -*- coding: utf-8 -*-
import requests
from requests.exceptions import Timeout
import os
from paho.mqtt import client as mqtt
import time, json, sys, math, datetime, re
from datetime import datetime
import subprocess
import platform
import configparser
import csv

def connectMQTT(ip, port):
#https://github.com/fr00sch/bosswerk_mi600_solar
#https://pypi.org/project/paho-mqtt/
    client = mqtt.Client()
    client.username_pw_set(mqtt_username, mqtt_password)
    client.on_connect = on_connect
    client.on_message = on_message
#with mqtt.Client(client_id="0", clean_session=True, userdata=None, protocol="MQTTv311", transport="tcp") as client:
    client.connect(ip , port, 60)
    return client

def savedata(d1, d2, d3):
    with open("data.csv",  mode='w') as file:
        file_writer = csv.writer(file, delimiter=',', quotechar='"',quoting=csv.QUOTE_MINIMAL)
        file_writer.writerow([d1,d2,d3])

def readdata():
    with open('data.csv', mode='r') as file:
        csvfile = csv.reader(file, delimiter=',')
        
        for row in csvfile:
            #print(row)
            #print(row[0])
            print(row[0],row[1],row[2],)

        d1 = row[0]
        d2 = row[1]
        d3 = row[2]

    return d1, d2, d3

def sendData(webdata_now_p, webdata_today_e, webdata_total_e):
 startmsg1 = json.dumps({"lastDateUpdate":datetime.today().strftime('%Y-%m-%d %H:%M:%S'), "clientname":'MI600', "status":"Online" }, skipkeys = True, allow_nan = False);
 #print("Message2 if Online", startmsg1) # for testing
 startmsg2 = json.dumps({"Energy": {"lastDateUpdate":datetime.today().strftime('%Y-%m-%d %H:%M:%S'), "power":webdata_now_p, "today":webdata_today_e, "total":webdata_total_e }}, skipkeys = True, allow_nan = False);
 #print("Message1 if Online", startmsg2) # for testing
 savedata(webdata_now_p, webdata_today_e, webdata_total_e)
 pubmsg(startmsg1, startmsg2)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    #https://github.com/fr00sch/bosswerk_mi600_solar
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #https://github.com/fr00sch/bosswerk_mi600_solar
    print(msg.topic+":"+str(msg.payload))  

def ping_ip(current_ip_address):
        #source: https://dmitrygolovach.com/python-ping-ip-address/
        try:
            output = subprocess.check_output("ping -{} 1 {}".format('n' if platform.system().lower(
            ) == "windows" else 'c', current_ip_address ), shell=True, universal_newlines=True)
            if 'unreachable' in output:
                return False
            else:
                return True
        except Exception:
                return False

def find_target_value(target, hp_source):
    find_target = hp_source.find(target)
    #print("target: {}" .format(find_target))
    get_target_back = "-1"
    if find_target > 0:
        find_value_start = hp_source.find("\"", find_target)
        #print("start: {}" .format(find_value_start)) # for testing
        find_value_end = hp_source.find("\"", find_value_start+1)
        #print("end: {}" .format(find_value_end)) # for testing
          
    get_target_back = hp_source[find_value_start+1:find_value_end]
    return(get_target_back)

def get_Solar_values():
    try:
        r = requests.get(webinterface_url, verify=False, auth=(htaccess_user, htaccess_pw), timeout=2)
    except Timeout:
        print('I waited far too long')

    else:
        print('The request got executed')
        if r.status_code == 200:
            hp_source = str(r.text)
            #print(hp_source)
            error = re.search("ERROR:404 Not Found:", hp_source)


            if(hp_source.find('ERROR:404 Not Found') == True):
                print(error)
            else:
                ret0 = find_target_value("var webdata_now_p =", hp_source)
                print(find_target_value("var webdata_now_p =", hp_source))
                if not (re.search('---',ret0) == True):
                    power = ret0
                    #print(ret0)
                ret1 = find_target_value("var webdata_today_e =", hp_source)
                print(find_target_value("var webdata_today_e =", hp_source))
                if not (re.search('---',ret1) == True):
                    today = ret1
                    #print(ret1)
                ret2 = find_target_value("var webdata_total_e =", hp_source)
                print(find_target_value("var webdata_total_e =", hp_source))
                if not (re.search('---',ret2) == True):
                    total = ret2
                    #print(ret2)

                sendData(power, today, total)

        else:
            print(r.status_code)

        #close connection
        r.close()
        print("Connection Closed")

def pubmsg (msg1, msg2):
    client.publish(topic1, msg1, qos=0, retain=mqtt_retain)
    #print("Message1 send to MQTT Brocker", msg1) # for testing
    time.sleep(1) # benötigt weil sonnst die 2te nachrichten nicht abgesetzt wird warum ist noch schleierhaft
    client.publish(topic2, msg2, qos=0, retain=mqtt_retain)
    #print("Message2 send to MQTT Brocker", msg2) # for testing
    client.disconnect()

if __name__=='__main__':

    config = configparser.ConfigParser()
    path = os.path.dirname(os.path.abspath(__file__))
    config.read('/opt/mi600/config.ini')
    htaccess_user = config['BOSSWERK']['user']
    htaccess_pw = config['BOSSWERK']['password']
    bosswerkIP = config['BOSSWERK']['ip']
    ping_try_count = config['BOSSWERK']['ping_time']
    webinterface_url = config['BOSSWERK']['url']

    mqtt_ip = config['MQTT']['mqtt_ip']
    mqtt_port = config['MQTT']['mqtt_port']
    topic = config['MQTT']['topic']
    client_id = config['MQTT']['client_id']
    mqtt_username = config['MQTT']['mqtt_username']
    mqtt_password = config['MQTT']['mqtt_password']
    mqtt_retain = bool(config['MQTT']['mqtt_retain'])

    statetopic = "/STATE"
    sensortopic = "/SENSOR"
    topic1 = topic + statetopic
    topic2 = topic + sensortopic
    #print("Topic1= " + topic1) # for testing
    #print("Topic2= " + topic2) # for testing

    getDataCountPing = 9
    client = connectMQTT(mqtt_ip,int(mqtt_port))
    while getDataCountPing < int(ping_try_count):
        print(getDataCountPing , "/" , ping_try_count )
        if ping_ip(bosswerkIP) == True:
            #power, today, total = readdata()
            get_Solar_values()
            break
        else:
          getDataCountPing = getDataCountPing + 1
          time.sleep(3)
          if getDataCountPing == int(ping_try_count):

            power, today, total = readdata()
            startmsg1 = json.dumps({"lastDateUpdate":datetime.today().strftime('%Y-%m-%d %H:%M:%S'), "clientname":'MI600', "status":"Offline" }, skipkeys = True, allow_nan = False);
            print("Message Topic1 if Offline", startmsg1) # for testing
            startmsg2 = json.dumps({"Energy": {"lastDateUpdate":datetime.today().strftime('%Y-%m-%d %H:%M:%S'), "power":0.0, "today":today, "total":total  }}, skipkeys = True, allow_nan = False);
            print("Message Topic2 if Offline", startmsg2) # for testing
            
            #sendData("Mi600", "123", "4.5", "6789") # for testing

            pubmsg(startmsg1, startmsg2)
