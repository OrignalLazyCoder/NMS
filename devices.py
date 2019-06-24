import sqlite3

conn = sqlite3.connect('database')
c = conn.cursor()

def addDevice(ip,deviceName,deviceType,parent):
    return True

def deleteDevice(ip):
    return True

def addDeviceType(deviceType):
    return True

def deleteDeviceType(deviceType):
    return True

def manageDevice(ip):
    return True

def findDevice(filter):
    return True