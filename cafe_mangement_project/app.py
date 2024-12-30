from flask import Flask, render_template, redirect, request, url_for,flash
from werkzeug.security import generate_password_hash,check_password_hash
import mysql.connector

app=Flask(__name__)
app.secret_key='EV1806'

mydb=mysql.connector.connect(
    host="localhost",
    user='Emran18',
    password='891901',
    database='sample',
)

cursor=mydb.cursor()
@app.route('/')
def home():
    cursor.execute("SELECT * FROM menu")
    menu=cursor.fetchall()
    return render_template('login.html')
   
@app.route('/add_menu', methods=['GET','POST'])
def add_item():
    if request.method=='POST':
        try:
            item_name=request.form['item_name']
            price=request.form['price']
            cursor.execute("INSERT INTO menu(item_name,price) values(%s,%s)",(item_name,price))
            cursor.execute("SELECT * FROM menu")
            menu=cursor.fetchall()
            mydb.commit()
            return render_template('index.html',menu=menu)
        except Exception as e:
            return str(e)
    else:
        return render_template('index.html')

@app.route('/place_order',methods=['POST'])
def placeorder():
    item_name=request.form['item_name']
    quantity=int(request.form['quantity'])
    cursor.execute("select price from menu where item_name=%s",(item_name,))
    price=cursor.fetchone()[0]
    total_price=int(price)*int(quantity)
    cursor.execute("insert into orders(item_name, quantity, total_price) values(%s,%s,%s)",(item_name,quantity,total_price))
    mydb.commit()
    return redirect('/orders')

@app.route('/orders',methods=['GET','POST'])

def orders():
    cursor.execute("select*from orders")
    orders=cursor.fetchall()
    return render_template('orders.html',orders=orders)

@app.route('/register',methods=['GET','POST'])
def register():
    messages=''
    try:
        if request.method=='POST':
            firstname=request.form['firstname']
            lastname=request.form['lastname']
            email=request.form['email']
            username=request.form['username']
            password=request.form['password']
            cursor.execute("select * from user_details where email=%s and username=%s",(email,username,))
            user=cursor.fetchone()
            if user:
                messages="Email or username is already registered. Please try again with various Email and Password."
                return render_template('Registration.html',messages=messages)
            else:
                password_hash=generate_password_hash(password,method='pbkdf2:sha256',salt_length=16)
                cursor.execute("INSERT INTO user_details(firstname,lastname,email,username,password) values(%s,%s,%s,%s,%s)",(firstname,lastname,email,username,password_hash))
                mydb.commit()
                messages="Registration successful"
                return render_template('login.html',messages=messages)
        else:
            return render_template('Registration.html')
    except Exception as e:
        return str(e)

@app.route('/login', methods=['GET','POST'])
def login():
    messages=''
    try:
        if request.method=='POST':
            username=request.form['username']
            password=request.form['password']
            cursor.execute("select * from user_details where username=%s",(username,))
            user=cursor.fetchone()
            if user and check_password_hash(user[5],password):
                messages='Login successful'
                cursor.execute("SELECT * FROM menu")    
                menu=cursor.fetchall()
                return render_template('index.html',menu=menu)
                # return render_template('index.html',messages=messages)
            else:
                messages="Invalid username or password. Please try again."
                return render_template('login.html',messages=messages)
        else:
            return render_template('login.html')
    except Exception as e:
        return str(e)

app.run(debug=True)