import os

from flask import Flask, session, render_template, request, redirect, flash
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql.expression import cast
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, session, flash


#encrypt
from passlib.hash import sha256_crypt


app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine)) 

  
@app.route("/")
def index():
	login = db.execute("SELECT * FROM login2").fetchall()
	return render_template("index.html", login=login)


@app.route("/registration", methods=["POST"])
def singup():
    """Registration Request."""
    
    #Get form information.
    user_name = request.form.get("user_name_su")
    user_pass = request.form.get("user_pass_su")
    
    if not user_name: 
        return render_template("error.html", message="#4 Invalid user name, please type one.")
    if not user_pass: 
            return render_template("error.html", message="#3 Invalid password, please type one.")
    
    try:
        if db.execute("SELECT * FROM login2 WHERE usr_name = :user_name",
                      {"user_name": user_name}).rowcount == 1:
            return render_template("error.html", message="#5 This user is already in user, please select another.")		

        db.execute("INSERT INTO login2 (usr_name, usr_pass) VALUES (:user_name, :user_pass)",
                   {"user_name": user_name, "user_pass": user_pass})
        db.commit()

        return render_template("registration.html")
        
    except ValueError:
        return render_template("error.html", message="#6 ERROR Please contact the server dba")


@app.route("/login", methods=["POST"])
def login():
    """Login Request."""
    #Get form information.
    user_name = request.form.get("user_name")
    user_pass = request.form.get("user_pass")
    app.secrety_key = str(user_pass)
    
    
    if not user_name: 
        return render_template("error.html", message="#9 Invalid user name")
    if not user_pass:
        return render_template("error.html", message="#10 Invalid password/password.")

    try:
        if db.execute("SELECT * FROM login2 WHERE usr_name = :user_name",
                      {"user_name": user_name}).rowcount == 0:
            return render_template("error.html", message="#8 No such user found in our data base")     

        autenticar()
    except ValueError:
        return render_template("error.html", user_name=form.request['user_name'],message="#2 We couldn't find any user with this password on our database")


@app.route('/autenticar', methods=['POST',])
def autenticar():
    user_name = request.form.get("user_name")
    user_pass = request.form.get("user_pass")

    if db.execute("SELECT * FROM login2 WHERE usr_name = :user_name AND usr_pass = :user_pass",
                      {"user_name": user_name, "user_pass" : user_pass}).rowcount == 1:
        user_id = db.execute("SELECT usr_id FROM login2 WHERE usr_name = :user_name",
                {"user_name": user_name}).fetchone()
            
        session['user_id'] = str(user_id)

        if 'user_id' not in session or session['user_id'] == None:
            return redirect('/')

        return render_template("logged2.html", user_name=user_name)
    else:
        flash('not logged in, try again!')
        return redirect('/loginroute')

@app.route('/logout')
def logout():
    session['user_id'] = None
    flash('bye see you later!')
    return redirect('/')


def book():
    """Lists all flights."""
    flights = db.execute("SELECT * FROM books").fetchall()
    return render_template("flights.html", flights=flights)


def load():
    f = open("books.csv")
    reader = csv.reader(f)
    for isbn, title, author, year in reader:
        db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
                    {"isbn": isbn, "title": title, "author": author, "year": year})
        """print(f"Added flight from {origin} to {destination} lasting {duration} minutes.")"""
    db.commit()





JSON_SORT_KEYS = False


















