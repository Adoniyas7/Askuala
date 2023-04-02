#==========================================================================
#                      Student Registration System                        #
#==========================================================================
#                             developed by:-                              #
#                          Adoniyas and Rediet                            #
#==========================================================================

import sqlite3
import pandas as pd
from datetime import datetime


connection = sqlite3.connect('Students.db')
cursor= connection.cursor()


def create_table():
    with connection:
        cursor.execute("""CREATE TABLE IF NOT EXISTS Students (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        First_name TEXT,
                        Middle_name TEXT,
                        Last_name TEXT,
                        Gender TEXT,
                        Date_of_birth TEXT,
                        Address TEXT,
                        Nationality TEXT,
                        Department TEXT,
                        Date_added TIMESTAMP
                        )""")
  

def insert_data(fname, mname, lname, gen, dob, addrs, natly, dept, date):
    with connection:
        cursor.execute("""INSERT INTO Students(
                        First_name,
                        Middle_name,
                        Last_name,
                        Gender,
                        Date_of_birth,
                        Address,
                        Nationality,
                        Department,
                        Date_added) 
                        VALUES(?,?,?,?,?,?,?,?,?)""",(fname,mname,lname,gen,dob,addrs,natly, dept, date))


def delete_data(id):
    with connection:
        cursor.execute("DELETE FROM Students WHERE id = ?",(id,))


def update_data(fname, mname, lname, gen, dob, addrs, natly, dept, id):
    with connection:
        cursor.execute("""UPDATE Students SET
                        First_name = ?,
                        Middle_name = ?,
                        Last_name = ?,
                        Gender = ?,
                        Date_of_birth = ?,
                        Address = ?,
                        Nationality = ?,
                        Department = ?
                        WHERE id = ?""",
                        (fname, mname, lname, gen, dob, addrs, natly, dept,id ))


def search_data(fname = '', mname = '', lname ='', gen  ='', dept ='', id ='', search_by = '', all = ''):
    space = ' '
    db_vals = {'Id':'id',
            'First Name': 'First_name',
            'Middle Name': 'Middle_name',
            'Last Name': 'Last_name',
            'Gender':'Gender',
            'Department':'Department',
            '':'First_name'
            }

    with connection:
        search_all = False
        search = fname
        if fname != '':
            search = fname.strip()
        elif mname !='':
            search = mname.strip()
        elif lname != '':
            search = lname.strip()
        elif gen != '':
            search = gen
        elif dept != '':
            search = dept
        elif id != '':
            search = id.strip()
        elif all != '':
            search = all.strip()
            search_all = True
        
        #search if search is not empty space
        if search != '':
            if search_all:
                cursor.execute("""SELECT * FROM students WHERE 
                            id LIKE '%'||?||'%' OR
                            First_name LIKE '%'||?||'%' OR
                            Middle_name LIKE '%'||?||'%' OR
                            Last_name LIKE '%'||?||'%' OR
                            Gender LIKE '%'||?||'%' OR
                            Date_of_birth LIKE '%'||?||'%' OR
                            Address LIKE '%'||?||'%' OR
                            Nationality LIKE '%'||?||'%' OR
                            Department LIKE '%'||?||'%'""",
                            (search, search ,search, search, search, search, search, search, search))
            else:
                #if search by is not gender search with like
                if gen == '':
                    cursor.execute(f"SELECT * FROM Students WHERE {db_vals[search_by]} Like '%'||?||'%'", (search, ))
                else:
                #if search by is gender dont use like because it will return male and female for male search because female contains male
                    cursor.execute(f"SELECT * FROM Students WHERE {db_vals[search_by]} = ?", (search, ))
                    
        
            row = cursor.fetchall()
            return row
        else:
            #if search is empty space return the sorted data
            return sort_data(db_vals[search_by])


def view_data():
    with connection:
        cursor.execute("SELECT * FROM Students ORDER BY First_name ASC")
        rows  = cursor.fetchall()
    return rows

def sort_data(value):
    if value == 'Date_added':
        order = 'DESC'
    else:
        order = 'ASC'

    with connection:
        cursor.execute(f"SELECT * FROM Students ORDER BY {value} {order}")
        # cursor.execute(f"SELECT * FROM Students ORDER BY {value} DESC")
        rows = cursor.fetchall()
    return rows


def save_db(path):
    query = 'SELECT * FROM Students'
    df =  pd.read_sql(query, connection, index_col='id')
    df.to_excel(path)

if __name__=='__main__':
    create_table()

