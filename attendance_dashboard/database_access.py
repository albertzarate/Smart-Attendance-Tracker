import mysql.connector
from wtforms import Form, StringField, SelectField, TextField, TextAreaField, SubmitField, validators, ValidationError
import smtplib




class EmployeeSearchForm(Form):
    choices = [('first_name', 'First Name'),
               ('emp_no', 'Employee Number')]
    select = SelectField('Search for search:', choices=choices)
    search = StringField('')


def sql_query():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="cmpe",
        database="trackerdb"
    )
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM student;")
    data = cursor.fetchall()
    return data



def send_mail(to_mail, subject, message):
    gmail_user = 'link.me.connect@gmail.com'
    gmail_password = 'mlink#22'

    sent_from = gmail_user
    to = [str(to_mail)]
    SUBJECT = str(subject)
    TEXT = str(message)

    message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, message)
        server.close()
    except:
        print("Something Went Wrong!")