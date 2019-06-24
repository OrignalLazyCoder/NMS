import sqlite3
import hashlib

def addUser(uId,uPwd,uType):
    conn = sqlite3.connect('database')
    c = conn.cursor()
    uPwd = hashlib.sha384(uPwd.encode()).hexdigest()
    try:
        c.execute("INSERT INTO users(userId,userPass,userAuth) VALUES(?,?,?)",(uId , uPwd , uType))
        conn.commit()
        return True
    except:
        return False

def updateUser(userType,uId):
    conn = sqlite3.connect('database')
    c = conn.cursor()
    try:
        c.execute("UPDATE users SET userAuth = (?) WHERE ID=(?)",(userType , uId))
        conn.commit()
        return True
    except:
        return False

def deleteUser(uId):
    conn = sqlite3.connect('database')
    c = conn.cursor()
    try:
        c.execute("DELETE FROM users WHERE ID=(?)",[uId])
        conn.commit()
        return True
    except:
        return False

def fetchUserList():
    conn = sqlite3.connect('database')
    c = conn.cursor()
    res = c.execute("SELECT ID,userId,userAuth FROM users")
    allUsers = []
    for i in res:
        allUsers.append({
            'uId' : i[0],
            'uName' : i[1],
            'uType' : i[2]
        })
    return allUsers