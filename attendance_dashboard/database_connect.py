import mysql.connector

import smtplib


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="cmpe",
    database="trackerdb"
    )


def send_mail():

    gmail_user = 'smart.attendance.tracker.iot@gmail.com'  
    gmail_password = 'cmpe195e'

    sent_from = gmail_user  
    to = ['trebla111@gmail.com']  
    SUBJECT = 'Attendance Data For the Week!'  
    TEXT = 'Albert was present for 5 days this week. Akash was not in class all week. Priyank was in class 3 days this week.'

    message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)



    try:  
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, message)
        server.close()

        print 'Email sent!'
    except:  
        print 'Something went wrong...'

def send_to_db(name):
    
    mycursor = mydb.cursor()

    print(name)

    if name != 'Unknown':

        sql = "UPDATE student SET days_present = days_present + 1 WHERE name = " + "'" + name + "'" + ";"
        print(sql)

        mycursor.execute(sql)
        mydb.commit()
        print(mycursor.rowcount, "record(s) affected")
        if (mycursor.rowcount == 0):
            sql = "INSERT INTO student VALUES ('" + name + "', 1, NULL);"
            mycursor.execute(sql)
            mydb.commit()
            print(mycursor.rowcount, "record(s) affected")

    send_mail()

