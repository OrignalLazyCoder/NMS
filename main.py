from flask import Flask, session, redirect, url_for, render_template, request
import os
import sqlite3
import hashlib
import userModule

app = Flask(__name__)
app.secret_key = os.urandom(24)


def checkIfUserExist(uId , uPwdHash):
    conn = sqlite3.connect('database')
    c = conn.cursor()
    result = c.execute("SELECT * FROM users WHERE userId=(?)",[uId])
    for i in result:
        if uPwdHash in i:
            return True , i[3]
    return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashBoard')
def dashBoard():
    if 'userId' not in session:
        return redirect(url_for('index' , isUser = False))
    try:
        if session['userId'] == None:
            return redirect(url_for('index' , isUser = False))
    except:
        return redirect(url_for('index' , isUser = False))

    return render_template('dashboard.html',userName = session['userId'] , userType =  session['uType'])

@app.route('/login' , methods=['POST'])
def login():
    uId = request.form['uId']
    uPwd = request.form['uPwd']
    uPwdHash = hashlib.sha384(uPwd.encode()).hexdigest()
    result,uType = checkIfUserExist(uId,uPwdHash)
    if result:
        session['userId'] = uId
        session['uType'] = uType
        return redirect(url_for('dashBoard'))
    else:
        return redirect(url_for('index' , wrongCredentials = True))

@app.route('/logout')
def logout():
    session.pop('userId' , None)
    session.pop('uType' , None)
    return redirect(url_for('index'))

#Manage Users DashBoard
@app.route('/users')
def users():
    if 'userId' not in session:
        return redirect(url_for('index' , isUser = False))
    try:
        if session['userId'] == None:
            return redirect(url_for('index' , isUser = False))
    except:
        return redirect(url_for('index' , isUser = False))
    if session['uType'] != "admin":
            return redirect(url_for('dashBoard'))
    return render_template('users.html',userName = session['userId'])

#Add new User in database
@app.route('/addNewUser' , methods=['POST'])
def addNewUser():
    if session['uType'] != "admin":
            return redirect(url_for('dashBoard'))
    uId = request.form['uId']
    uPwd = request.form['uPwd']
    uType = request.form['uType']
    status = userModule.addUser(uId,uPwd,uType)
    if status:
        return render_template('users.html', addedNew = True)
    else:
        return render_template('users.html', addedNew = False)
    
#Add new user web interface
@app.route('/addUser')
def addUser():
    if 'userId' not in session:
        return redirect(url_for('index' , isUser = False))
    try:
        if session['userId'] == None:
            return redirect(url_for('index' , isUser = False))
    except:
        return redirect(url_for('index' , isUser = False))
    if session['uType'] != "admin":
            return redirect(url_for('dashBoard'))
    return render_template('addUser.html',userName = session['userId'])

#Delete user Interface
@app.route('/deleteUser')
def deleteUser():
    if 'userId' not in session:
        return redirect(url_for('index' , isUser = False))
    try:
        if session['userId'] == None:
            return redirect(url_for('index' , isUser = False))
    except:
        return redirect(url_for('index' , isUser = False))
    if session['uType'] != "admin":
            return redirect(url_for('dashBoard'))
    allUsers = userModule.fetchUserList()
    return render_template('deleteUser.html',userList = allUsers)

#Delete User Activity
@app.route('/delete/<id>')
def delete(id):
    result = userModule.deleteUser(id)
    if result:
        return render_template('users.html' , isDeleted = result)
    else:
        return render_template('users.html' , isDeleted = False)

#View User interface    
@app.route("/viewUsers")
def viewUsers():
    if 'userId' not in session:
        return redirect(url_for('index' , isUser = False))
    try:
        if session['userId'] == None:
            return redirect(url_for('index' , isUser = False))
    except:
        return redirect(url_for('index' , isUser = False))
    if session['uType'] != "admin":
            return redirect(url_for('dashBoard'))
    allUsers = userModule.fetchUserList()
    return render_template('viewUsers.html',userList = allUsers)

#Change User Interface
@app.route('/changeUser')
def changeUser():
    if 'userId' not in session:
        return redirect(url_for('index' , isUser = False))
    try:
        if session['userId'] == None:
            return redirect(url_for('index' , isUser = False))
    except:
        return redirect(url_for('index' , isUser = False))
    if session['uType'] != "admin":
            return redirect(url_for('dashBoard'))
    allUsers = userModule.fetchUserList()
    return render_template('changeUser.html',userList = allUsers)

@app.route('/updateUser/<id>' , methods =['POST'])
def updateUser(id):
    res = userModule.updateUser(request.form['newType'],id)
    if res:
        return render_template('users.html' , isUpdated = res)
    else:
        return render_template('users.html' , isUpdated = False)


#Create database at __init__
def createDB():
    conn = sqlite3.connect('database')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users(ID INTEGER PRIMARY KEY AUTOINCREMENT , userId TEXT NOT NULL UNIQUE , userPass TEXT NOT NULL , userAuth TEXT NOT NULL)')
    c.execute('CREATE TABLE IF NOT EXISTS devices(ID INTEGER PRIMARY KEY AUTOINCREMENT , deviceIp TEXT NOT NULL UNIQUE , deviceName TEXT NOT NULL , deviceType TEXT NOT NULL)')
    conn.commit()

@app.errorhandler(404)
def page_not_found(e):
    return 'page under Development right now.'

if __name__  == "__main__":
    createDB()
    app.run(debug = True)