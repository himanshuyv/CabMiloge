from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def LogIn():
    return render_template('LogIn.html')


@app.route('/index')
def index():
    # conn = sqlite3.connect('cabmates.db') 
    # cursor = conn.cursor()
    # try:
    #     cursor.execute( '''
    #                     SELECT * FROM Cabmate
    #                     ''')
    #     entry=cursor.fetchall()
    #     conn.commit()
    #     conn.close()
       
    #     return render_template('test.html')
    # except:
    #     print('login failed')
    #     return render_template('testlogin.html')
    # return render_template('index.html',)
    return render_template('index.html')

@app.route('/SignUp')
def SignUp():
    return render_template('SignUp.html')




if __name__ == '__main__':
    app.run(debug=True)
