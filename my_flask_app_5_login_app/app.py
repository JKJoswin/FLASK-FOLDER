from flask import Flask,render_template,request,redirect,url_for,session,flash
import sqlite3
from werkzeug.security import generate_password_hash,check_password_hash

app=Flask(__name__)
def init_db():
    conn=sqlite3.connect('users.db')
    c=conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html',username=session['username'])
    return redirect(url_for('login'))

@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        username=request.form['username']
        password=request.form['password']

        hashed_pw=generate_password_hash(password)

        try:
            conn=sqlite3.connect('users.db')
            c=conn.cursor()
            c.execute("INSERT INTO users (username,password) VALUES (?,?)",(username,hashed_pw))
            conn.commit()
            conn.close()
            flash("Signup Successful! You can Login Now!","SUCCESS!")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Username already exists! Try a different one!","ERROR!")
        
        return render_template('signup.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username=request.form['username']
        password=request.form['password']

        conn=sqlite3.connect('users.db')
        c=conn.cursor()
        c.execute("SELECT password FROM users WHERE username=?",(username,))
        user=c.fetchone()
        conn.close()

        if user and check_password_hash(user[0],password):
            session['username']=username
            flash("Login Successful!","SUCCESS!")
            return redirect(url_for(home))
        else:
            flash("Invalid Username or Password!","ERROR!")
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username',None)
    flash("Logged out Successfully!","INFO!")
    return redirect(url_for('login'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)