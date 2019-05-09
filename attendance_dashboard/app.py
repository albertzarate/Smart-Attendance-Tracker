#!venv/bin/python
import os
from flask import Flask, url_for, redirect, render_template, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required, current_user
from flask_security.utils import encrypt_password
import flask_admin
from flask_admin.contrib import sqla
from flask_admin import helpers as admin_helpers
from flask_admin import BaseView, expose

import database_connect
import database_access

# Create Flask application
app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)


# Define models
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __str__(self):
        return self.email


# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)


# Create customized model view class
class MyModelView(sqla.ModelView):

    def is_accessible(self):
            return True


    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))


    # can_edit = True
    edit_modal = True
    create_modal = True    
    can_export = True
    can_view_details = True
    details_modal = True

class UserView(MyModelView):
    column_editable_list = ['email', 'first_name', 'last_name']
    column_searchable_list = column_editable_list
    column_exclude_list = ['password']
    # form_excluded_columns = column_exclude_list
    column_details_exclude_list = column_exclude_list
    column_filters = column_editable_list


class Student():
    def __init__(self, id, name, present, late, absent):
        self.id = id
        self.name = name
        self.present = present
        self.late = late
        self.absent = absent

@app.route('/send_data', methods = ['POST'])
def api_message():
    if request.headers['Content-Type'] == 'text/plain':
        print(request.data)
        database_connect.send_to_db(request.data)
        return "Text Message: " + request.data

    elif request.headers['Content-Type'] == 'application/json':
        print(json.dumps(request.json))
        return "JSON Message: " + json.dumps(request.json)
    else:
        return "415 Unsupported Media Type ;)"

@app.route('/view_students')
def view_students():
    result = []
    data = database_access.sql_query()
    id = []
    name = []
    present = []
    late = []
    absent = []

    for val in data:
        result.append(Student(val[0], val[1], val[2], val[3], val[4]))


    return render_template("students.html",result=result)


@app.route('/get_all')
def get_table_data():
    data = database_access.sql_query()
    id = ""
    name = ""
    present = ""
    late = ""
    absent = ""

    for val in data:
        id = id + str(val[0]) + "!"
        name = name + str(val[1]) + "@"
        present = present + str(val[2]) + "#"
        late = late + str(val[3]) + "$"
        absent = absent + str(val[4]) + "%"

    return(id + ':' + name + ':' + present + ':' + late + ':' + absent)

# Flask views
@app.route('/')
def index():
    results = ""
    all = ""
    names = []
    lates = []
    present_data = []

    data = database_access.sql_query()
    num_of_students = len(data)
    total_late = 0
    total_present = 0
    total_absent = 0
    results = results + str(num_of_students) + "/"

    for val in data:
        all = all + str(val[0]) + " "
        all = all + str(val[1]) + " "
        all = all + str(val[2]) + " "
        all = all + str(val[3]) + " "
        all = all + str(val[4]) + " "



        names.append(val[1])
        total_late = val[3] + total_late
        lates.append(val[3])
        total_present = val[2] + total_present
        present_data.append(val[2])

        total_absent = val[4] + total_absent

    results = results + str(total_late) + "/"
    results = results + str(total_present) + "/"
    results = results + str(total_absent) + "/"

    for n in sorted(zip(present_data, names, lates), reverse=True)[:3]:
        results = results + str(n[1]) + "/"
        results = results + str(n[2]) + "/"

    return str(results) + ":" + str(all)

# Create admin
admin = flask_admin.Admin(
    app,
    'My Dashboard',
    base_template='my_master.html',
    template_mode='bootstrap3',
)



if __name__ == '__main__':

    # Build a sample db on the fly, if one does not exist yet.
    app_dir = os.path.realpath(os.path.dirname(__file__))

    # Start app
    app.run(host="0.0.0.0", port=9000, debug=True)
