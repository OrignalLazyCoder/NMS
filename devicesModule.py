import sqlite3
import subprocess


conn = sqlite3.connect('database')
c = conn.cursor()

def addDevice(ip,deviceName,deviceType,parent):
    conn = sqlite3.connect('database')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO deviceList(deviceIp,deviceName,deviceType,parent) VALUES(?,?,?,?)",(ip,deviceName,deviceType,parent))
        conn.commit()
        return True
    except:
        return False

def deleteDevice(id):
    conn = sqlite3.connect('database')
    c = conn.cursor()

    try:
        c.execute("DELETE FROM deviceList WHERE ID=(?)",[id])
        conn.commit()
        return True
    except:
        return False

def fetchDeviceList():
    conn = sqlite3.connect('database')
    c = conn.cursor()
    data = c.execute('SELECT * FROM deviceList')
    res = []
    for i in data:
        res.append({
            'id' : i[0],
            'ip' : i[1],
            'name' : i[2],
            'type' : i[3],
            'parent' : i[4]
        })
    return res

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

def getStatus(all_hosts):
    status = []
    color = []
    info = subprocess.STARTUPINFO()
    info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    info.wShowWindow = subprocess.SW_HIDE
    for i in range(len(all_hosts)):
        output = subprocess.Popen(['ping', '-n', '1', '-w', '500', str(all_hosts[i])], stdout=subprocess.PIPE, startupinfo=info).communicate()[0]
        if "Destination host unreachable" in output.decode('utf-8'):
            status.append("offline")
            color.append('#f00')
        elif "Request timed out" in output.decode('utf-8'):
            status.append("offline")
            color.append('#f00')
        else:
            status.append("online")
            color.append('#0f0')
    return status , color

def checkOnline():
    conn = sqlite3.connect('database')
    c = conn.cursor()
    output = c.execute("SELECT * FROM deviceList")
    Id = []
    ip = []
    name = []
    Type = []
    parent = []
    for i in output:
        Id.append(i[0])
        ip.append(i[1])
        name.append(i[2])
        Type.append(i[3])
        parent.append(i[4])
    deviceStatus , color = getStatus(ip)
    liveStatus = []
    for i in range(len(ip)):
        liveStatus.append({
                'id' : Id[i],
                'ip' : ip[i],
                'name' : name[i],
                'type' : Type[i],
                'parent' : parent[i],
                'status' : deviceStatus[i],
                'color' : color[i]

            })
    return liveStatus