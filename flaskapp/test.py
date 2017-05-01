from flask import Flask, render_template,redirect, request
from passlib.hash import pbkdf2_sha256
import sqlite3

D = 'database.db'

def insert(name,password):
	con1 = sqlite3.connect(D)
	cur1 = con1.cursor()
	cur1.execute("INSERT INTO LOGIN (username,password) values (?,?)", (name,password))
	con1.commit()
	con1.close()

def fetch():
	con2 = sqlite3.connect(D)
	cur2 = con2.cursor()
	cur2.execute("SELECT username, password from LOGIN")	
	data=cur2.fetchall()
	con2.close()
	return data

app = Flask(__name__)

@app.route("/",methods=['GET','POST'])

def login():
	flagu=0;
	flagp=0;
	nm=request.form['name'];
	pw=request.form['password'];
	if request.method == 'POST':
		data= database.fetch()
		for row in data:
			if nm==row[0]:
				flagu=1;
				if pbkdf2_sha256.verify(pw,row[1]):
					flagp=1;
		if flagu==0:
			return redirect(url_for('/register'))
		if flagp==0:
			return render_template('login.html', msg="Invalid Credentials. Please try again")
		else:
			return ("Successfully logged in!")	

	else:
			return render_template('login.html', msg="")

@app.route('/register', methods=['GET','POST'])
def register():
	nm=request.form['name'];
	pw=request.form['password'];	
	if request.method == 'POST':

		hash = pbkdf2_sha256.encrypt(pw, rounds=200000, salt_size=16)
		database.insert(nm, hash)
		return redirect('/')
	else:
		return render_template('register.html')


if __name__ == "__main__":
		app.run(debug= True)

