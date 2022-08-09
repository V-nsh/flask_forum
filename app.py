from sqlite3 import IntegrityError
import requests
from flask import Flask, render_template, request, redirect, url_for, flash
import jinja2
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host = "127.0.0.1",
    port = "3306",
    database = "forum",
    user= "root",
    password = "password",
)

currPID = 0

"""
CREATE TABLE threads(post VARCHAR(500), title VARCHAR(50), id INT, userName VARCHAR(50), userEmail varchar(50), comments varchar(500), postID int);
"""

cursor = db.cursor(buffered=True)
cursor2 = db.cursor(buffered=True)

@app.route('/')
def main():
    # count = cursor.execute('SELECT COUNT(post) FROM threads')
    cursor2.execute("SELECT * FROM threads")
    data= cursor2.fetchall()
    return render_template('home.html', data=data)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        # i = request.form['id1']
        title1 = request.form['title1']
        desc = request.form['post']
        pid = request.form['postid']
        cursor.execute('INSERT INTO threads(title, post, postID) VALUES( %s, %s, %s)', (title1, desc, pid,))
        db.commit()

        cursor2.execute("SELECT * FROM threads")
        data= cursor2.fetchall()

        # count = cursor.execute('SELECT COUNT(comments) FROM threads') 
        # review comments later
        return render_template('home.html', data = data)
    return render_template('create.html')

@app.route('/thread', methods=['GET', 'POST'])
def thread():
    global currPID 
    # currPID= request.args.get('connectID')
    # cursor2.execute("SELECT * FROM threads WHERE postID=%s", (currPID,))
    # data = cursor2.fetchall()
    if request.method == 'POST':
        comment = request.form['comments']
        id = request.form['id1']
        user = request.form['user']
        currPID =  request.args['connectID']
        print(currPID)
        cursor.execute('UPDATE threads SET id=%s, userName=%s, comments=%s WHERE postID=%s', (id, user, comment, currPID))
        db.commit()
        cursor2.execute("SELECT * FROM threads")
        data = cursor2.fetchall()
        return render_template('thread.html', data = data)
        
    connPID = request.args.get('connectID')
    print(connPID)
    cursor2.execute("SELECT * FROM threads WHERE postID=%s", (connPID,))
    data = cursor2.fetchall()
    return render_template('thread.html', data = data)

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method =='POST':
        i= request.form['id2']
        cursor.execute('DELETE FROM threads WHERE id=%s', (i, ))

        cursor2.execute("SELECT * FROM threads")
        data = cursor2.fetchall()
        return render_template('thread.html', data=data)

    cursor2.execute("SELECT * FROM threads")
    data = cursor2.fetchall()
    return render_template('thread.html', data=data)

if __name__=="__main__":
    app.run(debug = True)