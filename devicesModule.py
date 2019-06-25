import sqlite3

conn = sqlite3.connect('database')
c = conn.cursor()

def addDevice(ip,deviceName,deviceType,parent):
    return True

def deleteDevice(ip):
    return True

def addDeviceType(deviceType):
    conn = sqlite3.connect('database')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO deviceType(deviceTypeName) VALUES(?)",[deviceType])
        conn.commit()
        return True
    except:
        return False

def fetchDeviceTypeList():
    conn = sqlite3.connect('database')
    c = conn.cursor()
    output = c.execute("SELECT * FROM deviceType")
    res = []
    for i in output:
        res.append({
            'id' : i[0],
            'deviceTypeName' : i[1]
        })
    return res


def deleteDeviceType(id):
    conn = sqlite3.connect('database')
    c = conn.cursor()
    try:
        c.execute("DELETE FROM deviceType WHERE ID=(?)",[id])
        conn.commit()
        return True
    except:
        return False

def findDevice(filter):
    return True