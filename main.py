import mysql.connector
from flask import *
import os
from datetime import datetime

app = Flask(__name__)
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Welcome@123',
    port='3306',
    database='attendance',
    autocommit=True,
)
mycursor = mydb.cursor()
app.secret_key = os.urandom(24)


@app.before_request
def before_request():
    g.user = None
    if 'pass' in session:
        g.user = session['pass']


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['password'] == 'a' and request.form['username'] == 'a':
            session['pass'] = request.form['password']
            session['user'] = request.form['username']
            return redirect(url_for('main'))

        if request.form['password'] == 'b' and request.form['username'] == 'b':
            session['pass'] = request.form['password']
            session['user'] = request.form['username']
            return redirect(url_for('main'))

        if request.form['password'] == 'z' and request.form['username'] == 'z':
            session['pass'] = request.form['password']
            session['user'] = request.form['username']
            return redirect(url_for('admin'))

    return render_template('login.html')


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if g.user:
        mycursor.execute("SELECT * FROM attendance.attendance;")
        data = mycursor.fetchall()
        return render_template('admin.html', user=session['pass'], headings=mycursor.column_names, data=data)
    return redirect(url_for('login'))


@app.route('/main', methods=['GET', 'POST'])
def main():
    if g.user:
        return render_template('main.html')
    return redirect(url_for('login'))


@app.route('/submitted', methods=['GET', 'POST'])
def submitted():
    if g.user and request.method == 'POST':
        now = datetime.now()
        formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
        username = session['user']
        intime = request.form['intime']
        outtime = request.form['outtime']
        if intime is None and outtime is None:
            return redirect(url_for('main'))
        else:
            mycursor.execute("INSERT INTO attendance (Fullname,timedate, intime, outtime) VALUES ('{}','{}' ,{},{})".format(username, formatted_date, intime, outtime))
        return render_template('submitted.html')
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run()