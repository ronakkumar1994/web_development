from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy,request
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/test_web'
db = SQLAlchemy(app)


class Contact(db.Model):
    '''sr.no, name, email, phone, message, date'''
    srno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(25), unique=True, nullable=False)
    phone = db.Column(db.String(10),  nullable=False)
    message = db.Column(db.String(80), nullable=False)
    date = db.Column(db.String(12), nullable=False)


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/post")
def post():
    return render_template('post.html')

@app.route("/contact", methods=['GET','POST'])
def contact():
    if (request.method=='POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        entry = Contact(name=name, email=email, phone=phone,message=message,date=datetime.now())
        db.session.add(entry)
        db.session.commit()
    return render_template('contact.html')


app.run(debug=True)

