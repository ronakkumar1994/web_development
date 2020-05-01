from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy,request
from datetime import datetime
from flask_mail import Mail
import json

with open('config.json','r') as c:
    params=json.load(c)["params"]

app = Flask(__name__)
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params['gmail-user'],
    MAIL_PASSWORD=params['gmail-password']
)
mail = Mail(app)

if (params['local_server']):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

db = SQLAlchemy(app)


class Contact(db.Model):
    srno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(25), unique=True, nullable=False)
    phone = db.Column(db.String(11),  nullable=False)
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
        mail.send_message('new enquiry from '+name,
                          sender=email,recipients=[params['gmail-user']],
                          body=message+"\n"+phone+"\n"+email
                          )
    return render_template('contact.html')


app.run(debug=True)

