from flask import Flask, render_template, request
import sqlite3
from bcrypt import gensalt,hashpw,checkpw

def hash_password(password):
    salt = gensalt()
    hashed_password = hashpw(password.encode('utf-8'), salt)
    return hashed_password

def check_password(entered_password, hashed_password):
    return checkpw(entered_password.encode('utf-8'), hashed_password)


app = Flask(__name__)

@app.route('/')
def LogIn():
    return render_template('LogIn.html')


@app.route('/Get_Auth', methods=['POST', 'GET'])
def Get_Auth():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = sqlite3.connect('cabmates.db') 
        cursor = conn.cursor()
        try:
            cursor.execute( '''
                            SELECT * FROM Login WHERE Email = ?
                            ''', (email,))
            entry=cursor.fetchone()
            conn.commit()
            conn.close()
            print(entry[3])
            if check_password(password, entry[3]) :
                print('login sucessfull')
                return render_template('index.html')
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

        hashpw = hash_password(Password)

        conn = sqlite3.connect('cabmates.db') 
        cursor = conn.cursor()
        try:
            cursor.execute('''
                        INSERT INTO Login (Fname, Lname, Email, Password)
                        VALUES (?, ?, ?, ?)
                        ''', (fname, lname, email, hashpw))
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

@app.route('/SignUp',methods=['POST', 'GET'])
def SignUp():
    return render_template('SignUp.html')







if __name__ == '__main__':
    app.run(debug=True)
