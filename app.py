from flask import Flask, render_template, request,redirect,session,jsonify,flash,url_for;
import sqlite3
from bcrypt import gensalt,hashpw,checkpw
from cas import CASClient
from urllib.parse import quote_plus
from cryptography.fernet import Fernet
import os
from functools import cmp_to_key
import smtplib
from email.message import EmailMessage
import datetime


SECRET_KEY = os.getenv('SECRET_KEY',os.urandom(24))
CAS_SERVER_URL = os.getenv('CAS_SERVER_URL', 'https://login.iiit.ac.in/cas/')
SERVICE_URL = os.getenv('SERVICE_URL', 'http://localhost:5000/Get_Auth')
REDIRECT_URL = os.getenv('REDIRECT_URL', 'http://localhost:5000/Get_Auth')



app = Flask(__name__)
app.secret_key = SECRET_KEY

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
            # cursor.execute('''SELECT * FROM fromCampus''')
            entry = cursor.fetchone()
            cursor.execute('''SELECT * FROM fromCampus WHERE Station = ?''', (entry[3],))
            # cursor.execute('''SELECT * FROM fromCampus ''')
            
        else:
            cursor.execute('''SELECT * FROM toCampus WHERE BookingID = ?''', (entry_id,))
            # cursor.execute('''SELECT * FROM toCampus''')
            entry = cursor.fetchone()
            cursor.execute('''SELECT * FROM toCampus WHERE Station = ?''', (entry[3],))
            # cursor.execute('''SELECT * FROM toCampus''')
            
        entries = cursor.fetchall()
        
        
        
        print(entries)
        
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
        cursor.execute('SELECT * FROM Login WHERE Uid = ?', (uid,))
        user = cursor.fetchone()
        conn.commit()
        conn.close()
    except:
        print('Data not found')
    return render_template('/bookingspage.html', available_options = BookingEntries, fname=user[0], lname=user[2] , entry_id=entry_id,  direction=direction)

@app.route('/upcomingTravels')
def upcomingTravels():
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
        cursor.execute( '''select * from Login where Uid = ?''', (uid,))

        user = cursor.fetchone()
        
        print('uid:',uid)
        print('user:',user)
        
        return render_template('upcomingtravels.html', fromCampus_entries = fromCampus_entries, toCampus_entries = toCampus_entries, fname=user[0],lname=user[1])
    else:
        return redirect('/')
    
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
        cursor.execute( '''select * from Login where Uid = ?''', (uid,))
        user = cursor.fetchone()
        print('uid:',uid)
        print('user:',user)
        return render_template('index.html', fname=user[0],lname=user[1])
    else:
        return redirect('/')


@app.route('/logout_user', methods=['POST', 'GET'])
def logout_user():
    session.pop('token', None)
    return redirect('/')


@app.route('/viewBookingRedirect', methods=['POST', 'GET'])
def view_booking_redirect():
    # entry_id = request.form['entry_id']
    # direction = request.form['direction']
    token = session['token']
    with open('key.key', 'rb') as file:
        key = file.read()
    fernet = Fernet(key)
    uid = fernet.decrypt(token).decode()

    # print(direction, entry_id)
        
    try:
        conn = sqlite3.connect('cabmates.db') 
        cursor = conn.cursor()
        BookingEntries = []
        # if direction == 'From Campus':
        # cursor.execute('''SELECT * FROM fromCampus WHERE BookingID = ?''', (entry_id,))
        # # cursor.execute('''SELECT * FROM fromCampus''')
        # entry = cursor.fetchone()
        cursor.execute('''select * from Login where Uid = ?''', (uid,))
        user_data=cursor.fetchall()
        
        
        cursor.execute('''SELECT * FROM fromCampus''')
        entries1 = cursor.fetchall()
        
        # print("\n\nentries:\n",entries1)
        # print("\n\n")
        
        for item in entries1:
            if item[1] == uid:
                continue
            date = item[2].split(' ')[0]
            time = item[2].split(' ')[1]
            uid = item[1]
            cursor.execute( '''select * from Login where Uid = ?''', (item[1],))
            data = cursor.fetchone()
            # print("\n\n data:\n",data)
            # print("\n\n")
            Fname = data[0]
            Lname = data[1]
            Name = Fname + ' ' + Lname
            email_id=data[2]
            Gender = data[6]
            Batch = data[5]
            station= item[3]
            from_location="IIIT Campus"
            temp_tuple = (date, time, uid, Name, Gender, Batch, station, from_location, email_id, user_data[0][3]) #user_data[2] is user emailid
            # print("\nhello\n")
            BookingEntries.append(temp_tuple)
        
        # /print("hello")
        
        cursor.execute('''SELECT * FROM toCampus''')
        entries1 = cursor.fetchall()
        # print(entries1)
        for item in entries1:
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
            email_id=data[2]
            station= "IIIT Campus"
            from_location=item[3]
            temp_tuple = (date, time, uid, Name, Gender, Batch,station,from_location, email_id, user_data[0][3])
            BookingEntries.append(temp_tuple)
        
        # print(BookingEntries)
        cursor.execute('SELECT * FROM Login WHERE Uid = ?', (uid,))
        user = cursor.fetchone()
        # print("\n\nuser:", user)
        conn.commit()
        conn.close()
    except Exception as e:
        print('An error occurred:', e)
        
    return render_template('/bookingspage.html', available_options = BookingEntries, fname=user[0], lname=user[1] )




def isTimeinRange(entry, BookingEntries, rev_requested_time):
    
    for time in rev_requested_time:
        time = int(time)
        
        if time== 23:
            time_p = time
            time1 = time_p + ":00:00"
            time_first = datetime.datetime.strptime(time1, "%H:%M:%S")
            # time_second = datetime.datetime.strptime(time2, "%H:%M:%S")
            entry_time = datetime.datetime.strptime(entry[1], "%H:%M:%S")
            
            if datetime.time(23, 0, 0) == time_first:
                if entry_time >= time_first:
                    BookingEntries.append(entry[1])
        else:
            
            time_p = time
            time_s = time + 1
            if time < 10:
                time_p = "0" + str(time_p)
                time_s = "0" + str(time_s)
            else:
                time_p = str(time_p)
                time_s = str(time_s)
            print("hey1")
            time1 = time_p + ":00:00"
            time2 = time_s + ":00:00"
            time_first = datetime.datetime.strptime(time1, "%H:%M:%S")
            time_second = datetime.datetime.strptime(time2, "%H:%M:%S")
            entry_time = datetime.datetime.strptime(entry[1], "%H:%M:%S")
            
            if datetime.time(23, 0, 0) == time_first:
                if entry_time >= time_first:
                    BookingEntries.append(entry)
            elif entry_time >=time_first and entry_time < time_second:
                print(entry_time)
                print(time_first)
                print(time_second)
                BookingEntries.append(entry)
                break


@app.route('/apply_filters', methods=['POST'])
def apply_filters():
    token = session['token']
    with open('key.key', 'rb') as file:
        key = file.read()
    fernet = Fernet(key)
    uid = fernet.decrypt(token).decode()

    try:       
        conn = sqlite3.connect('cabmates.db')
        cursor = conn.cursor()
        filters = request.json
        
        cursor.execute('''select * from Login where Uid = ?''', (uid,))
        user_data=cursor.fetchall()
  
        AllEntries = []
        BookingEntries = []
        
        # print(filters)
        
                
        requested_batch= filters.get('selectedBatch').split(",")
        requested_time= filters.get('selectedTime').split(",")
        requested_desti= filters.get('selectedDestination').split(",")
        requested_start= filters.get('selectedStart').split(",")
        requested_date= filters.get('selectedDate')
        
        
        rev_requested_time=[]
        
        for time in requested_time:
            rev_requested_time.append(time.split('-')[0])
        
        print(requested_time[0])
        
        cursor.execute('''SELECT * FROM fromCampus''')
        entries1 = cursor.fetchall()
        
        # print("\n\nentries:\n",entries1)
        # print("\n\n")
        
        for item in entries1:
            # if item[1] == uid:
            #     continue
            date = item[2].split(' ')[0]
            time = item[2].split(' ')[1]
            uid = item[1]
            cursor.execute( '''select * from Login where Uid = ?''', (item[1],))
            data = cursor.fetchone()
            # print("\n\n data:\n",data)
            # print("\n\n")
            Fname = data[0]
            Lname = data[1]
            Name = Fname + ' ' + Lname
            email_id=data[2]
            Gender = data[6]
            Batch = data[5]
            station= item[3]
            from_location="IIIT Campus"
            temp_tuple = (date, time, uid, Name, Gender, Batch, station, from_location, email_id, user_data[0][3]) #user_data[2] is user emailid
            # print("\nhello\n")
            AllEntries.append(temp_tuple)
        
        # /print("hello")
        
        cursor.execute('''SELECT * FROM toCampus''')
        entries1 = cursor.fetchall()
        # print(entries1)
        for item in entries1:
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
            email_id=data[2]
            station= "IIIT Campus"
            from_location=item[3]
            temp_tuple = (date, time, uid, Name, Gender, Batch,station,from_location, email_id, user_data[0][3])
            AllEntries.append(temp_tuple)
        
        # print(BookingEntries)
        cursor.execute( '''select fname from Login where Uid = ?''', (uid,))
        user = cursor.fetchone()
        # print("\n\nuser:", user)
        conn.commit()
        conn.close()

        # print(AllEntries)        
        # print(requested_batch)
        # print(requested_desti)
        # print(requested_date)
        # print(requested_start)
        # print(requested_time)
        
        
        # for starrting_point in 
        for entry in  AllEntries:
            
            if requested_start[0] != '':
                # print(entry[7])
                # print(requested_start)
                if entry[7] in requested_start:
                    print("here2")
                    if requested_date:
                        
                        if entry[0]==requested_date:
                        
                            if requested_desti[0] != '':
                                
                                if entry[6] in requested_desti:
                                
                                    if requested_batch[0] != '':
                                        
                                        if "All" in requested_batch:
                                            
                                            if requested_time[0] != '':

                                                isTimeinRange(entry, BookingEntries, rev_requested_time)
                                            else:            
                                                BookingEntries.append(entry)
                                                
                                                
                                        elif "UG5+" in requested_batch:
                                            if entry[5]=="UG5" and entry[5]=="UG6" and entry[5]=="UG7" and entry[5]=="UG8" and entry[5]=="UG9" and entry[5]=="UG10" and entry[5]=="UG11":
                                                
                                                if requested_time[0] != '':
                                                    print("hey2")
                                                    isTimeinRange(entry, BookingEntries, rev_requested_time)
                                                else:            
                                                    BookingEntries.append(entry)
                                                
                                        elif entry[5] in requested_batch:
                                            if requested_time[0] != '':
                                                print("hey3")
                                                isTimeinRange(entry, BookingEntries, rev_requested_time)
                                            else:            
                                                BookingEntries.append(entry)
            
 
                                    else:
                                        
                                        if requested_time[0] != '':
                                            print("hey4")
                                            isTimeinRange(entry, BookingEntries, rev_requested_time)
                                        else:            
                                            BookingEntries.append(entry)
                            
                            else:
                                if requested_batch[0] != '':
                                          
                                    if "All" in requested_batch:                                            
                                        if requested_time[0] != '':
                                            print("hey5")
                                            isTimeinRange(entry, BookingEntries, rev_requested_time)
                                        else:            
                                            BookingEntries.append(entry)
                                            
                                            
                                            
                                    elif "UG5+" in requested_batch:
                                        if entry[5]=="UG5" and entry[5]=="UG6" and entry[5]=="UG7" and entry[5]=="UG8" and entry[5]=="UG9" and entry[5]=="UG10" and entry[5]=="UG11":
                                            
                                            
                                            if requested_time[0] != '':
                                                print("hey6")
                                                isTimeinRange(entry, BookingEntries, rev_requested_time)
                                            else:            
                                                BookingEntries.append(entry)
                                                
                                    elif entry[5] in requested_batch:
                                        
                                        if requested_time[0] != '':
                                            print("hey7")
                                            isTimeinRange(entry, BookingEntries, rev_requested_time)
                                        else:            
                                            BookingEntries.append(entry)
        
 
                                else:
                                    if requested_time[0] != '':
                                        print("hey8")
                                        isTimeinRange(entry, BookingEntries, rev_requested_time)
                                    else:            
                                        BookingEntries.append(entry)
                    else:
                        if requested_desti[0] != '':
                                
                            if entry[6] in requested_desti:
                            
                                if requested_batch[0] !='':
                                    
                                    if "All" in requested_batch:
                                        if requested_time[0] != '':
                                            print("hey9")
                                            isTimeinRange(entry, BookingEntries, rev_requested_time)
                                        else:            
                                            BookingEntries.append(entry)
                                    elif "UG5+" in requested_batch:
                                        if entry[5]=="UG5" and entry[5]=="UG6" and entry[5]=="UG7" and entry[5]=="UG8" and entry[5]=="UG9" and entry[5]=="UG10" and entry[5]=="UG11":
                                            
                                            if requested_time[0] != '':
                                                print("hey10")
                                                isTimeinRange(entry, BookingEntries, rev_requested_time)
                                            else:            
                                                BookingEntries.append(entry)
                                    elif entry[5] in requested_batch:
                                        if requested_time[0] != '':
                                            print("hey11")
                                            isTimeinRange(entry, BookingEntries, rev_requested_time)
                                        else:            
                                            BookingEntries.append(entry)
 
                                else:
                                    
                                    if requested_time[0] != '':
                                        print("hey12")
                                        isTimeinRange(entry, BookingEntries, rev_requested_time)
                                    else:            
                                        BookingEntries.append(entry)
                    
                        else:
                            if requested_batch[0] != '':
                                if "All" in requested_batch:
                                        if requested_time[0] != '':
                                            print("hey13")
                                            isTimeinRange(entry, BookingEntries, rev_requested_time)
                                        else:            
                                            BookingEntries.append(entry)
                                elif "UG5+" in requested_batch:
                                    if entry[5]=="UG5" and entry[5]=="UG6" and entry[5]=="UG7" and entry[5]=="UG8" and entry[5]=="UG9" and entry[5]=="UG10" and entry[5]=="UG11":
                                        if requested_time[0] != '':
                                            print("hey14")
                                            isTimeinRange(entry, BookingEntries, rev_requested_time)
                                        else:            
                                            BookingEntries.append(entry)
                                elif entry[5] in requested_batch:
                                        if requested_time[0] != '':
                                            print("hey15")
                                            isTimeinRange(entry, BookingEntries, rev_requested_time)
                                        else:            
                                            BookingEntries.append(entry)
 
                            else:
                                if requested_time[0] != '':
                                    print("hey16")
                                    isTimeinRange(entry, BookingEntries, rev_requested_time)
                                else:            
                                    BookingEntries.append(entry)
                                                 
            else:
                
                if requested_date:
                    
                        if entry[0]==requested_date:
                        
                            if requested_desti[0] != '':
                                
                                if entry[6] in requested_desti:
                                
                                    if requested_batch[0] != '':
                                        if "All" in requested_batch:
                                            if requested_time[0] != '':
                                                print("hey17")
                                                isTimeinRange(entry, BookingEntries, rev_requested_time)
                                            else:            
                                                BookingEntries.append(entry)
                                        elif "UG5+" in requested_batch:
                                            if entry[5]=="UG5" and entry[5]=="UG6" and entry[5]=="UG7" and entry[5]=="UG8" and entry[5]=="UG9" and entry[5]=="UG10" and entry[5]=="UG11":
                                                if requested_time[0] != '':
                                                    print("hey18")    
                                                    isTimeinRange(entry, BookingEntries, rev_requested_time)
                                                else:            
                                                    BookingEntries.append(entry)
                                        elif entry[5] in requested_batch:
                                            if requested_time[0] != '':
                                                print("hey19")    
                                                isTimeinRange(entry, BookingEntries, rev_requested_time)
                                            else:            
                                                BookingEntries.append(entry)
            
                                    else:
                                        if requested_time[0] != '':
                                            print("hey20")    
                                            isTimeinRange(entry, BookingEntries, rev_requested_time)
                                        else:            
                                            BookingEntries.append(entry)
                            
                            else:
                                
                                if requested_batch[0] != '':  
                                    if "All" in requested_batch:
                                        if requested_time[0] != '':
                                            print("hey21")    
                                            isTimeinRange(entry, BookingEntries, rev_requested_time)
                                        else:            
                                            BookingEntries.append(entry)
                                    elif "UG5+" in requested_batch:
                                        if entry[5]=="UG5" and entry[5]=="UG6" and entry[5]=="UG7" and entry[5]=="UG8" and entry[5]=="UG9" and entry[5]=="UG10" and entry[5]=="UG11":
                                            if requested_time[0] != '':
                                                print("hey22")    
                                                isTimeinRange(entry, BookingEntries, rev_requested_time)
                                            else:            
                                                BookingEntries.append(entry)
                                    elif entry[5] in requested_batch:
                                        if requested_time[0] != '':
                                            print("hey23")    
                                            isTimeinRange(entry, BookingEntries, rev_requested_time)
                                        else:            
                                            BookingEntries.append(entry)
                                
                                else:
                                    if requested_time[0] != '':
                                        print("hey24")    
                                        isTimeinRange(entry, BookingEntries, rev_requested_time)
                                    else:            
                                        BookingEntries.append(entry)
                else:
                    if requested_desti[0] != '':
                        print("here")
                        print(entry[6]) 
                        print(requested_desti)
                        if entry[6] in requested_desti:
                            print("now")
                            if requested_batch[0] != '':
                                
                                if "All" in requested_batch:
                                    if requested_time[0] != '':
                                        print("hey25")    
                                        isTimeinRange(entry, BookingEntries, rev_requested_time)
                                    else:            
                                        BookingEntries.append(entry)
                                elif "UG5+" in requested_batch:
                                    if entry[5]=="UG5" and entry[5]=="UG6" and entry[5]=="UG7" and entry[5]=="UG8" and entry[5]=="UG9" and entry[5]=="UG10" and entry[5]=="UG11":
                                        if requested_time[0] != '':
                                            print("hey26")    
                                            isTimeinRange(entry, BookingEntries, rev_requested_time)
                                        else:            
                                            BookingEntries.append(entry)
                                elif entry[5] in requested_batch:
                                        if requested_time[0] != '':
                                            print("hey27")    
                                            isTimeinRange(entry, BookingEntries, rev_requested_time)
                                        else:            
                                            BookingEntries.append(entry)
 
                            else:
                                
                                if requested_time[0] != '':
                                    print("hey28")    
                                    isTimeinRange(entry, BookingEntries, rev_requested_time)
                                else:            
                                    BookingEntries.append(entry)
                        
                    else:
                        if requested_batch[0] != '':
                            
                            if "All" in requested_batch:
                                    if requested_time[0] != '':
                                        print("hey29")    
                                        isTimeinRange(entry, BookingEntries, rev_requested_time)
                                    else:            
                                        BookingEntries.append(entry)
                            elif "UG5+" in requested_batch:
                                if entry[5]=="UG5" and entry[5]=="UG6" and entry[5]=="UG7" and entry[5]=="UG8" and entry[5]=="UG9" and entry[5]=="UG10" and entry[5]=="UG11":
                                    if requested_time[0] != '':
                                        print("hey30")    
                                        isTimeinRange(entry, BookingEntries, rev_requested_time)
                                    else:            
                                        BookingEntries.append(entry)
                            elif entry[5] in requested_batch:
                                    if requested_time[0] != '':
                                        print("hey31")    
                                        isTimeinRange(entry, BookingEntries, rev_requested_time)
                                    else:            
                                        BookingEntries.append(entry)
                                
                        else:
            
                            if requested_time[0] != '':
                                print("hey32")  
                                isTimeinRange(entry, BookingEntries, rev_requested_time)
                            else:            
                                BookingEntries.append(entry)
                                            
                
        filtered_data = {'available_options': BookingEntries, 'user': user_data[0]}
        
        # print(filtered_data)
        
        return jsonify(filtered_data)
    
    except Exception as e:
        # print("Error occurred on line:", traceback.extract_tb(e.__traceback__)[0].lineno)
        print("Error:", e)
        return jsonify({'error': str(e)}), 500
    

@app.route('/about')
def about():
    token = session['token']
    with open('key.key', 'rb') as file:
        key = file.read()
    fernet = Fernet(key)
    uid = fernet.decrypt(token).decode()
    
    conn = sqlite3.connect('cabmates.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Login WHERE Uid = ?', (uid,))
    user = cursor.fetchone()

    conn.close()
    return render_template('about.html', fname=user[0], lname=user[1])


@app.route('/editprofilepage')
def editprofilepage():
    conn = sqlite3.connect('cabmates.db') 
    cursor = conn.cursor()
    token = session['token']
    with open('key.key', 'rb') as file:
        key = file.read()
    fernet = Fernet(key)
    uid = fernet.decrypt(token).decode()
    
    
    try:
        cursor.execute( '''
                        SELECT * FROM Login WHERE Uid = ?
                        ''', (uid,))
        user = cursor.fetchall()
        
        print(user)
    except Exception as e:
        print('An error occurred:', e)
        
    return render_template('/editprofilepage.html', user=user)


@app.route('/update_userData', methods=['POST'])
def update_userData():
    try:
        gender = request.form.get('gender')
        batch = request.form.get('batch')
        token = session['token']
        with open('key.key', 'rb') as file:
            key = file.read()
        fernet = Fernet(key)
        uid = fernet.decrypt(token).decode()
        
        conn = sqlite3.connect('cabmates.db')
        cursor = conn.cursor()

        cursor.execute('''
        UPDATE Login
        SET gender = ?, batch = ?
        WHERE Uid = ?
        ''', (gender, batch, uid))
        
        conn.commit()
        
        cursor.execute('SELECT * FROM Login WHERE Uid = ?', (uid,))
        user = cursor.fetchall()
        conn.close()

        # Redirect with a success message
        return redirect(url_for('editprofilepage', update_message='success'))
        
    except Exception as e:
        print('An error occurred:', e)
        return redirect(url_for('editprofilepage', update_message='error'))
    
    

    
if __name__ == '__main__':
    key = Fernet.generate_key()
    with open('key.key', 'wb') as file:
        file.write(key)
    app.run(debug=True)