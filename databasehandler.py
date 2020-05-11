import sqlite3
import collections
import time
from datetime import datetime

'''trida se stara o praci s databazi'''

class DatabaseHandler:

    def count_total(self):
        try:
            conn = sqlite3.connect('mydb.db')
            cursor = conn.cursor()
            print("Connected to SQLite")

            select_query = """SELECT SUM(increase) FROM table_energy"""
            cursor.execute(select_query)
            record = cursor.fetchall()
            result=record[0][0]
            cursor.close()
            return result
        
        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)
        finally:
            if (conn):
                conn.close()
                print("The SQLite connection is closed")


    def select_day(self,day,month,year):
        try:
            conn = sqlite3.connect('mydb.db')
            cursor = conn.cursor()
            print("Connected to SQLite")

            datetime_object= datetime(year,month,day)
            date=datetime_object.timestamp()
            
            day_begin=date
            day_end=day_begin+86400
            
            select_query = """SELECT * from table_energy WHERE time > ? AND time < ? """
            values = (day_begin, day_end)
            cursor.execute(select_query, values)
            
            records = cursor.fetchall()
            print("Total rows in that day are:  ", len(records))
            print("Printing each row")
            result = {}
            for row in records:
                print("time: ", row[0])
                print("increase: ", row[1])
                result[row[0]] = row[1]
            cursor.close()
            return result
        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)
        finally:
            if (conn):
                conn.close()
                print("The SQLite connection is closed")            

    def insert_row(self,time, increase):
        try:
            conn = sqlite3.connect('mydb.db')
            cursor = conn.cursor()
            print("Successfully Connected to SQLite")

            insert_query = "INSERT INTO table_energy(time, increase) VALUES (?, ?)"
            recordValues = (time, increase)
            count = cursor.execute(insert_query, recordValues)
            conn.commit()
            print("inserted ", cursor.rowcount)
            cursor.close()
        except sqlite3.Error as error:
            print("Failed to insert data into sqlite table", error)
        finally:
            if (conn):
                conn.close()
                print("The SQLite connection is closed")


    
