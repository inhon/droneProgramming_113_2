from dronekit import connect, VehicleMode, LocationGlobalRelative
from RepeatTimer import RepeatTimer
from datetime import datetime
from Formation import formation
from geopy.point import Point
import math
import setting


class Protocol():
    '''
    0   latitude(:011.8f), 
        longitude(:012.8f),
        altitude(:06.2f), 
        time(minute+second, 4 chars)  34 chars (including "0" in the beginning)
    1   "TAKEOFF"                     1 char (only "1")
    2   "TOOKOFF"                     1 char (only "2")
    3   "LAND"                        1 char (only "3")
    4   "LANDED"                      1 char (only "4")
    '''
    def __init__(self) :
        self.formation=formation()
    
    
    def sendMsg(self, client, msgName, vehicle=None): 
        if msgName == "COORDINATES":
            lat, lon = self.formation.getRoverPosition_0(vehicle) #取得rover的目標位置
            alt=setting.ROVER_HEIGHT
            if lat is not None:  #base是靜止，則lat 和 lon 傳送 (None, None)
                current_time = datetime.now().strftime("%M%S")     # This will turn the time into minute and second format, something like 0835 (08:35)
                TCP_msg = "0"+ str("{:011.8f}".format(lat)) + str("{:012.8f}".format(lon)) + str("{:06.2f}".format(alt)) + str(current_time)
            else:
                current_time = datetime.now().strftime("%M%S") 
                lat=0.0  #base是靜止，則lat 和 lon 傳送 (0, 0)
                lon=0.0
                TCP_msg = "0"+ str("{:011.8f}".format(lat)) + str("{:012.8f}".format(lon)) + str("{:06.2f}".format(alt)) + str(current_time)
            
        elif msgName == "TAKEOFF":
            TCP_msg = "1"
        elif msgName == "TOOKOFF":
            TCP_msg = "2"
        elif msgName == "LAND":
            TCP_msg = "3"
        elif msgName == "LANDED":
            TCP_msg = "4"
        else:
            print("ERROR: Wrong Message Name:", msgName)
            return
        
        client.send(TCP_msg.encode())
        #print("Sent",msgName)

    def recvMsg(self, client):
        msgName = client.recv(1).decode()
        # print("Received Msg Name", msgName)
        if(msgName == "0"):
            msg = client.recv(33).decode()
            # print("Received:",msg)
            lat = float(msg[0:11])
            lon = float(msg[11:23])
            alt = float(msg[23:29])
            recvTime = int(msg[31:33])
            # assert(lat <= 90 and lat >= -90)               
            # assert(lon <= 180 and lon >= -180)             
            # assert(alt < 100)                  

            return lat, lon, alt, recvTime
        elif(msgName == "1"):
            return ("TAKEOFF",)
        elif(msgName == "2"):
            return ("TOOKOFF",)
        elif(msgName == "3"):
            return ("LAND",)
        elif(msgName == "4"):
            return ("LANDED",)