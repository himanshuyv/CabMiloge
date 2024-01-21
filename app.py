from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def LogIn():
    return render_template('LogIn.html')


@app.route('/Get_Auth')
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
            if entry[3] == password :
                print('login sucessfull')
                return render_template('index.html')
            else :
                message='wrong password!'
                return render_template('LogIn.html')
        except:
            print('login failed')
            message='Email not found!'
            return render_template('LogIn.html')
        


@app.route('/Get_userData')
def Get_userData():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
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
            if entry[3] == password :
                print('login sucessfull')
                return render_template('index.html')
            else :
                message='wrong password!'
                return render_template('LogIn.html')
        except:
            print('login failed')
            message='Email not found!'
            return render_template('SignUp.html',message=message)

@app.route('/SignUp')
def SignUp():
    return render_template('SignUp.html')







if __name__ == '__main__':
    app.run(debug=True)
