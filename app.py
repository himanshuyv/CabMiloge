from flask import Flask, render_template, request,redirect,session;
import sqlite3
from bcrypt import gensalt,hashpw,checkpw
import os
import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)

def hash_password(password):
    salt = gensalt()
    hashed_password = hashpw(password.encode('utf-8'), salt)
    return hashed_password

def check_password(entered_password, hashed_password):
    return checkpw(entered_password.encode('utf-8'), hashed_password)

def sort_by_datetime(entries):
    for i in range(len(entries)):
        for j in range(len(entries)):
            if entries[i][2] < entries[j][2]:
                temp = entries[i]
                entries[i] = entries[j]
                entries[j] = temp
    return entries


@app.route('/')
def LogIn():
    return render_template('LogIn.html')


@app.route('/Get_Auth', methods=['POST', 'GET'])
def Get_Auth():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        print(email)
        print(password)
        conn = sqlite3.connect('cabmates.db') 
        cursor = conn.cursor()
        try:
            cursor.execute( '''
                            SELECT * FROM Login WHERE Email = ?
                            ''', (email,))
            entry=cursor.fetchone()
            conn.commit()
            conn.close()
            if check_password(password, entry[5]) :
                print('login sucessfull')
                session['email'] = email
                return redirect('/index')
            else :
                message='wrong password!'
                return render_template('LogIn.html',message=message)
        except:
            print('login failed')
            message='Email not found!'
            return render_template('LogIn.html',message=message)
    else:
        return render_template('LogIn.html')
        


@app.route('/Get_userData',methods=['POST', 'GET'])
def Get_userData():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        Password = request.form['password']
        gender = request.form['gender']
        batch = request.form['batch']
    
        hashpw = hash_password(Password)

        conn = sqlite3.connect('cabmates.db') 
        cursor = conn.cursor()
        try:
            cursor.execute('''
                        INSERT INTO Login (Fname, Lname, Email, Batch, Gender, Password)
                        VALUES (?, ?, ?, ?, ?, ?)
                        ''', (fname, lname, email, batch, gender, hashpw))
            print('signUp successful')
            conn.commit()
            conn.close()
            return render_template('LogIn.html')
        except:
            print('login failed')
            message='Email Already in Use!'
            return render_template('SignUp.html',message=message)
    else:
        render_template('SignUp.html')

@app.route('/getForFromCampus',methods=['POST', 'GET'])
def getForFromCampus():
    if request.method == 'POST':
        to = request.form['station']
        date = request.form['departureDate']
        time = request.form['departureTime']
        print(to,date,time)
        f = '%Y-%m-%d %H:%M:%S'
        date_time = date + ' ' + time + ':00'
        try:
            conn = sqlite3.connect('cabmates.db') 
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO fromCampus (Email, DateTime, Station) VALUES (?, ?, ?)''', (session['email'], date_time, to))
            print('Data inserted')
            conn.commit()
            conn.close()
        except:
            print('Data not inserted')
        return redirect('/index')
    else:
        return redirect('/index')
    
@app.route('/getForToCampus',methods=['POST', 'GET'])
def getForToCampus():
    if request.method == 'POST':
        to = request.form['station']
        date = request.form['departureDate']
        time = request.form['departureTime']
        print(to,date,time)
        f = '%Y-%m-%d %H:%M:%S'
        date_time = date + ' ' + time + ':00'
        try:
            conn = sqlite3.connect('cabmates.db') 
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO toCampus (Email, DateTime, Station) VALUES (?, ?, ?)''', (session['email'], date_time, to))
            print('Data inserted')
            conn.commit()
            conn.close()
        except:
            print('Data not inserted')
        return redirect('/index')
    else:
        return redirect('/index')

@app.route('/SignUp',methods=['POST', 'GET'])
def SignUp():
    return render_template('SignUp.html')

@app.route('/deleteBookingFromCampus', methods=['POST', 'GET'])
def delete_booking_route():
    entry_id = request.form['entry_id']
    print(entry_id)
    try:
        conn = sqlite3.connect('cabmates.db') 
        cursor = conn.cursor()
        cursor.execute('''DELETE FROM fromCampus WHERE BookingID = ?''', (entry_id,))
        conn.commit()
        conn.close()
        print('Data deleted')
    except:
        print('Data not deleted')
    return redirect('/index')

@app.route('/deleteBookingToCampus', methods=['POST', 'GET'])
def delete_booking_route_to():
    entry_id = request.form['entry_id']
    print(entry_id)
    try:
        conn = sqlite3.connect('cabmates.db') 
        cursor = conn.cursor()
        cursor.execute('''DELETE FROM toCampus WHERE BookingID = ?''', (entry_id,))
        conn.commit()
        conn.close()
        print('Data deleted')
    except:
        print('Data not deleted')
    return redirect('/index')   


@app.route('/index')
def index():
    conn = sqlite3.connect('cabmates.db') 
    cursor = conn.cursor()

    cursor.execute( '''
                    SELECT * FROM fromCampus WHERE Email = ?
                    ''', (session['email'],))
    entries = cursor.fetchall()
    sort_by_datetime(entries)
    fromCampus_entries = []
    for item in entries:
        date = item[2].split(' ')[0]
        time = item[2].split(' ')[1]
        station = item[3]
        entry_id = item[0]
        temp_tuple = (date,time,station,entry_id)
        fromCampus_entries.append(temp_tuple)
    cursor.execute( '''
                    SELECT * FROM toCampus WHERE Email = ?
                    ''', (session['email'],))
    
    entries = cursor.fetchall()
    sort_by_datetime(entries)
    toCampus_entries = []
    for item in entries:
        date = item[2].split(' ')[0]
        time = item[2].split(' ')[1]
        station = item[3]
        entry_id = item[0]
        temp_tuple = (date,time,station,entry_id)
        toCampus_entries.append(temp_tuple)
    cursor.execute( '''select fname from Login where Email = ?''', (session['email'],))
    user = cursor.fetchone()
    return render_template('index.html', fromCampus_entries = fromCampus_entries, toCampus_entries = toCampus_entries, user=user[0])

if __name__ == '__main__':
    app.run(debug=True)