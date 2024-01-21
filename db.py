import sqlite3
from datetime import datetime, timedelta

conn = sqlite3.connect('cabmates.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Login (
        Fname TEXT,
        Lname TEXT,
        Email TEXT PRIMARY KEY,
        Batch TEXT,
        Gender TEXT,
        Password TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Cabmate (
        BookingID INTEGER PRIMARY KEY AUTOINCREMENT,
        Email TEXT,
        DateTime DATETIME,
        PickUp TEXT,
        Destination TEXT,
        UNIQUE (Email, DateTime)
    )
''')

cursor.execute('''
                INSERT INTO Cabmate (Email, Datetime, Pickup, Destination)
                VALUES (?, ?, ?, ?)
            ''', ('fname', 'lname', 'email', 'password'))

cursor.execute('SELECT * FROM Cabmate')
cabmate_entries = cursor.fetchall()

for item in cabmate_entries:
    print(item)

cursor.execute('SELECT * FROM Login')
cabmate_entries = cursor.fetchall()

for item in cabmate_entries:
    print(item)


def add_duration_to_iso_datetime(datetime_str, hours=0, minutes=0, seconds=0):
    input_datetime = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M')
    duration_to_add = timedelta(hours=hours, minutes=minutes, seconds=seconds)
    result_datetime = input_datetime + duration_to_add
    result_datetime_str = result_datetime.strftime('%Y-%m-%dT%H:%M')
    return result_datetime_str

def subtract_duration_from_iso_datetime(datetime_str, hours=0, minutes=0, seconds=0):
    input_datetime = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M')
    duration_to_subtract = timedelta(hours=hours, minutes=minutes, seconds=seconds)
    result_datetime = input_datetime - duration_to_subtract
    result_datetime_str = result_datetime.strftime('%Y-%m-%dT%H:%M')
    return result_datetime_str

def GetCabmate(Datetime, interval):
    print(Datetime)
    start_datetime = subtract_duration_from_iso_datetime(Datetime,hours=interval)
    end_datetime = add_duration_to_iso_datetime(Datetime,hours=interval)
    cursor.execute('''
        SELECT * FROM Cabmate
        WHERE DateTime >= ? AND DateTime <= ?
    ''', (start_datetime, end_datetime))

    cabmates_within_interval = cursor.fetchall()
    return cabmates_within_interval

#***input format****
# Datetime = '2024-01-21T10:00'
# interval = 1
# selected_batches = {'UG1': True, 'UG2': True, 'UG3': False, 'UG4': True, 'UG5': False, 'PG1': False, 'PG2': True}
# selected_genders = {'Male': True, 'Female': False, 'Others': True}
def GetFilteredCabmate(Datetime, interval,selected_batches, selected_genders):
    start_datetime = subtract_duration_from_iso_datetime(Datetime,hours=interval)
    end_datetime = add_duration_to_iso_datetime(Datetime,hours=interval)
    selected_batches_list = [batch for batch, selected in selected_batches.items() if selected]
    selected_genders_list = [gender for gender, selected in selected_genders.items() if selected]
    datequery = '''
        AND Cabmate.DateTime >= '{}' AND Cabmate.DateTime <= '{}'
    '''.format(start_datetime, end_datetime)

    query = '''
        SELECT Login.*, Cabmate.*
        FROM Login
        INNER JOIN Cabmate ON Login.Email = Cabmate.Email
        WHERE Login.Batch IN ({})
        AND Login.Gender IN ({})'''.format(','.join(['"{}"'.format(batch) for batch in selected_batches_list]),
            ','.join(['"{}"'.format(gender) for gender in selected_genders_list]))
    query=query+datequery
    cursor.execute(query)
    qualified_cabmates = cursor.fetchall()
    return qualified_cabmates

def removeEntry(BookId):
    try:
        cursor.execute('''
                        DELETE from Cabmate WHERE BookingID=?
                        ''', (BookId,))
        print("Removed Successfully")
    except:
        print("Deletion Failed")

        


# in_interval=GetCabmate('2024-01-20T00:57',4)
# print(in_interval)




# Example usage:
# input_time_str = '05:30:00'
# result_time_str = subtract_duration_from_time(input_time_str, hours=9)

# print(result_time_str)


