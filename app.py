from flask import Flask, render_template, request,redirect,session;
import sqlite3
from bcrypt import gensalt,hashpw,checkpw
from cas import CASClient
from urllib.parse import quote_plus
from cryptography.fernet import Fernet
import os
from functools import cmp_to_key

app = Flask(__name__)
app.secret_key = os.urandom(24)

CAS_SERVER_URL="https://login.iiit.ac.in/cas/"
SERVICE_URL="http://localhost:5000/Get_Auth"
REDIRECT_URL="http://localhost:5000/Get_Auth"

cas_client = CASClient(
    version=3,
    service_url=f"{SERVICE_URL}?next={quote_plus(REDIRECT_URL)}",
    server_url=CAS_SERVER_URL,
)

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
        cas_login_url = cas_client.get_login_url()
        return redirect(cas_login_url)
    else:
        ticket = request.args.get('ticket')
        if ticket:
            user, attributes, pgtiou = cas_client.verify_ticket(ticket)
            if user:
                roll = attributes['RollNo']
                email = attributes['E-Mail']
                first_name = attributes['FirstName']
                last_name = attributes['LastName']
                uid = attributes['uid']
                batch = ''
                gender = ''
                conn = sqlite3.connect('cabmates.db') 
                cursor = conn.cursor()
                try:
                    cursor.execute( '''
                                    SELECT * FROM Login WHERE Uid = ?
                                    ''', (uid,))
                    entry=cursor.fetchone()
                    print(entry)
                    conn.commit()
                    conn.close()
                    if entry:
                        print('login sucessfull')
                        with open('key.key', 'rb') as file:
                            key = file.read()
                        fernet = Fernet(key)
                        token = fernet.encrypt(uid.encode())
                        session['token'] = token
                        return redirect('/index')
                    else:
                        message='User not found! Please Sign Up.'
                        return render_template('SignUp.html',roll=roll, email=email, first_name=first_name, last_name=last_name, uid=uid, message=message)
                except:
                    message='Error with database. Please try again'
                    return render_template('LogIn.html', message=message)
            else:
                message='Error with CAS. Please try again'
                return render_template('LogIn.html', message=message)
        else:
            message='Error with CAS. Please try again'
            return render_template('LogIn.html', message=message)
        


@app.route('/Get_userData',methods=['POST', 'GET'])
def Get_userData():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        roll = request.form['roll']
        uid = request.form['uid']
        gender = request.form['gender']
        batch = request.form['batch']
        conn = sqlite3.connect('cabmates.db') 
        cursor = conn.cursor()
        try:
            print(fname)
            print(lname)
            print(email)
            print(roll)
            print(uid)
            print(gender)
            print(batch)
            cursor.execute('''
                        INSERT INTO Login (Fname, Lname, Email, RollNo, Uid, Batch, Gender)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                        ''', (fname, lname, email, roll, uid, batch, gender))
            print('signUp successful')
            conn.commit()
            conn.close()
            with open('key.key', 'rb') as file:
                key = file.read()
            fernet = Fernet(key)
            token = fernet.encrypt(uid.encode())
            session['token'] = token
            return redirect('/index')
        except:
            print('Sign Up Failed')
            message='Sign Up Failed!'
            return render_template('LogIn.html', message=message)

@app.route('/getDataForBooking',methods=['POST', 'GET'])
def getForFromCampus():
    if request.method == 'POST':
        token = session['token']
        with open('key.key', 'rb') as file:
            key = file.read()
        fernet = Fernet(key)
        uid = fernet.decrypt(token).decode()
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
                cursor.execute('''INSERT INTO fromCampus (Uid, DateTime, Station) VALUES (?, ?, ?)''', (uid, date_time, to))
            else:
                cursor.execute('''INSERT INTO toCampus (Uid, DateTime, Station) VALUES (?, ?, ?)''', (uid, date_time, to))
            print('Data inserted')
            conn.commit()
            conn.close()
        except:
            print('Data not inserted')
        return redirect('/index')
    else:
        return redirect('/index')

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
    token = session['token']
    with open('key.key', 'rb') as file:
        key = file.read()
    fernet = Fernet(key)
    uid = fernet.decrypt(token).decode()
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
            if item[1] == uid:
                continue
            date = item[2].split(' ')[0]
            time = item[2].split(' ')[1]
            uid = item[1]
            cursor.execute( '''select * from Login where Uid = ?''', (item[1],))
            data = cursor.fetchone()
            Fname = data[0]
            Lname = data[1]
            Name = Fname + ' ' + Lname
            Gender = data[6]
            Batch = data[5]
            temp_tuple = (date, time, uid, Name, Gender, Batch)
            BookingEntries.append(temp_tuple)
        cursor.execute( '''select fname from Login where Uid = ?''', (uid,))
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
    token = session['token']
    with open('key.key', 'rb') as file:
        key = file.read()
    fernet = Fernet(key)
    uid = fernet.decrypt(token).decode()
    if(session):
        cursor.execute( '''
                        SELECT * FROM fromCampus WHERE Uid = ?
                        ''', (uid,))
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
                        SELECT * FROM toCampus WHERE Uid = ?
                        ''', (uid,))
        
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
        cursor.execute( '''select fname from Login where Uid = ?''', (uid,))
        user = cursor.fetchone()
        return render_template('index.html', fromCampus_entries = fromCampus_entries, toCampus_entries = toCampus_entries, user=user[0])
    else:
        return redirect('/')

@app.route('/logout_user', methods=['POST', 'GET'])
def logout_user():
    session.pop('token', None)
    return redirect('/')


@app.route('/viewBookingRedirect', methods=['POST', 'GET'])
def view_booking_redirect():
    conn = sqlite3.connect('cabmates.db') 
    entry_id = request.form['entry_id']
    direction = request.form['direction']
    token = session['token']
    with open('key.key', 'rb') as file:
        key = file.read()
    fernet = Fernet(key)
    uid = fernet.decrypt(token).decode()
    cursor = conn.cursor()
    cursor.execute( '''select fname from Login where Uid = ?''', (uid,))
    user = cursor.fetchone()
    return render_template('/viewBooking.html', user=user[0], entry_id=entry_id, direction=direction)

if __name__ == '__main__':
    key = Fernet.generate_key()
    with open('key.key', 'wb') as file:
        file.write(key)
    app.run(debug=True)