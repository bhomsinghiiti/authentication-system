from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'arvind'
app.config['MYSQL_DB'] = 'student'

mysql = MySQL(app)

@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
	msg =''
	msg2=''
	if request.method == 'POST' and 'userID' in request.form and 'password' in request.form:
		userID = request.form['userID']
		password = request.form['password']
		cursor = mysql.connection.cursor()
		cursor.execute('SELECT * FROM student_data WHERE userID = % s AND user_password = % s', (userID, password, ))
		account = cursor.fetchone()
		cursor.close()
		if account:
			msg = userID
			cur=mysql.connection.cursor()
			cur.execute('SELECT * FROM  courses')
			data=cur.fetchall()
			cur.close()
			return render_template('home.html', msg = msg,msg2=data)
		else:
			msg = 'Incorrect username / password !'
	return render_template('login.html', msg = msg)


@app.route('/register', methods =['GET', 'POST'])
def register():
	msg = ''  
	if request.method == 'POST' and 'userID' in request.form and 'password' in request.form and 'mobile_no' in request.form and 'co_password' in request.form:
		userID = request.form['userID']
		password = request.form['password']
		co_password = request.form['co_password']
		contact_no = request.form['mobile_no']

		cursor = mysql.connection.cursor()
		cursor.execute('SELECT * FROM student_data WHERE userID = % s', (userID, ))
		account = cursor.fetchone()
		if co_password != password:   # checking condition if user exist or not 
			msg = 'please enter the same password'
		elif account:
			msg = 'Account already exists !'
		else:
			cursor.execute('INSERT INTO student_data VALUES ( % s, % s, % s)', (userID, password, contact_no if contact_no !='NA' else None, ))
			mysql.connection.commit()
			msg =userID
			cur=mysql.connection.cursor()
			cur.execute('SELECT * FROM  courses')
			data=cur.fetchall()
			cursor.close()
			return render_template('home.html',msg=msg ,msg2=data) 	
	return render_template('register.html', msg = msg)
if __name__=='__main__':
    app.run(debug=True)
