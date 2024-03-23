from flask import Flask, render_template, request,redirect,session;
import sqlite3
from bcrypt import gensalt,hashpw,checkpw
import os
from functools import cmp_to_key

app = Flask(__name__)
app.secret_key = os.urandom(24)

def hash_password(password):
    salt = gensalt()
    hashed_password = hashpw(password.encode('utf-8'), salt)
    return hashed_password

def check_password(entered_password, hashed_password):
    return checkpw(entered_password.encode('utf-8'), hashed_password)

def compare_datetime(entry1, entry2):
    if entry1[2] < entry2[2]:
        return -1
    elif entry1[2] > entry2[2]:
        return 1
    else:
        return 0
    
def sort_by_datetime(entries):
    entries.sort(key=cmp_to_key(compare_datetime))
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

@app.route('/getDataForBooking',methods=['POST', 'GET'])
def getForFromCampus():
    if request.method == 'POST':
        to = request.form['station']
        date = request.form['departureDate']
        time = request.form['departureTime']
        direction = request.form['direction']
        print(to,date,time)
        f = '%Y-%m-%d %H:%M:%S'
        date_time = date + ' ' + time + ':00'
        try:
            conn = sqlite3.connect('cabmates.db') 
            cursor = conn.cursor()
            if direction == 'From Campus':
                cursor.execute('''INSERT INTO fromCampus (Email, DateTime, Station) VALUES (?, ?, ?)''', (session['email'], date_time, to))
            else:
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

@app.route('/deleteBooking', methods=['POST', 'GET'])
def delete_booking_route():
    entry_id = request.form['entry_id']
    direction = request.form['direction']
    print(direction, entry_id)
    try:
        conn = sqlite3.connect('cabmates.db') 
        cursor = conn.cursor()
        if direction == 'From Campus':
            cursor.execute('''DELETE FROM fromCampus WHERE BookingID = ?''', (entry_id,))
        else:
            cursor.execute('''DELETE FROM toCampus WHERE BookingID = ?''', (entry_id,))
        conn.commit()
        conn.close()
        print('Data deleted')
    except:
        print('Data not deleted')
    return redirect('/index')  

@app.route('/viewBooking', methods=['POST', 'GET'])
def view_booking():
    entry_id = request.form['entry_id']
    direction = request.form['direction']
    print(direction, entry_id)
    try:
        conn = sqlite3.connect('cabmates.db') 
        cursor = conn.cursor()
        BookingEntries = []
        if direction == 'From Campus':
            cursor.execute('''SELECT * FROM fromCampus WHERE BookingID = ?''', (entry_id,))
            entry = cursor.fetchone()
            cursor.execute('''SELECT * FROM fromCampus WHERE Station = ?''', (entry[3],))
        else:
            cursor.execute('''SELECT * FROM toCampus WHERE BookingID = ?''', (entry_id,))
            entry = cursor.fetchone()
            cursor.execute('''SELECT * FROM toCampus WHERE Station = ?''', (entry[3],))
        entries = cursor.fetchall()
        for item in entries:
            if item[1] == session['email']:
                continue
            date = item[2].split(' ')[0]
            time = item[2].split(' ')[1]
            email = item[1]
            cursor.execute( '''select * from Login where Email = ?''', (item[1],))
            data = cursor.fetchone()
            Fname = data[0]
            Lname = data[1]
            Name = Fname + ' ' + Lname
            Gender = data[4]
            Batch = data[3]
            temp_tuple = (date, time, email, Name, Gender, Batch)
            BookingEntries.append(temp_tuple)
        cursor.execute( '''select fname from Login where Email = ?''', (session['email'],))
        user = cursor.fetchone()
        conn.commit()
        conn.close()
    except:
        print('Data not found')
    return render_template('/viewBooking.html', available_options = BookingEntries, user=user[0] , entry_id=entry_id,  direction=direction)

@app.route('/index')
def index():
    conn = sqlite3.connect('cabmates.db') 
    cursor = conn.cursor()
    if(session):
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
    else:
        return redirect('/')

@app.route('/logout_user', methods=['POST', 'GET'])
def logout_user():
    session.pop('email', None)
    return redirect('/')


@app.route('/viewBookingRedirect', methods=['POST', 'GET'])
def view_booking_redirect():
    conn = sqlite3.connect('cabmates.db') 
    entry_id = request.form['entry_id']
    direction = request.form['direction']
    cursor = conn.cursor()
    cursor.execute( '''select fname from Login where Email = ?''', (session['email'],))
    user = cursor.fetchone()
    return render_template('/viewBooking.html', user=user[0], entry_id=entry_id, direction=direction)

if __name__ == '__main__':
    app.run(debug=True)