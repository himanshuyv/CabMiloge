@app.route('/submit_form', methods=['POST'])
def submit_form():
    if request.method == 'POST':
        email = request.form['email']
        datetime = request.form['datetime']
        pickup = request.form['pickup']
        destination = request.form['destination']

        conn = sqlite3.connect('cabmates.db') 
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO Cabmate (Email, DateTime, PickUp, Destination)
                VALUES (?, ?, ?, ?)
            ''', (email, datetime, pickup, destination))
            conn.commit()
            conn.close()
        except:
            print("constraint voilated in form")

        return render_template('test.html')
    

@app.route('/login', methods=['POST'])
def login():
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
                return render_template('test.html')
        except:
            print('login failed')
            return render_template('testlogin.html')
        
@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        password = request.form['password']
       

        conn = sqlite3.connect('cabmates.db') 
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO Login (Fname, Lname, Email, Password)
                VALUES (?, ?, ?, ?)
            ''', (fname, lname, email, password))
            conn.commit()
            conn.close()
            print('signup successfull')
            return render_template('testlogin.html')
        except:
            print('signup Fail')
            return render_template('testsignup.html')