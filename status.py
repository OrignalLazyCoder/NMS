import sqlite3

conn = sqlite3.connect('database')
c = conn.cursor()

def checkStatus():
    return True

def checkOneStatus(ip):
    return True