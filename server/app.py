from flask import Flask, render_template, request, send_file
from flask_sqlalchemy import SQLAlchemy as sqa
#from controller.send_email import send_email
from sqlalchemy.sql import func
from werkzeug import secure_filename

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:pSql1@localhost/email_height'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://prxovtwwdbqtgr:135b1d695365ce8c1099e4e2a9c75ff6e7b3ec58cf2affe46d75d9eccc65744a@ec2-54-227-237-223.compute-1.amazonaws.com:5432/d2b38uk7juqqfi?sslmode=require'
db = sqa(app)

class Data(db.Model):
    __tablename__ = "data"
    id = db.Column(db.Integer, primary_key = True)
    email_ = db.Column(db.String(120), unique = True)
    height_ = db.Column(db.Integer)

    def __init__(self, email_, height_):
        self.email_ = email_
        self.height_ = height_


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/success", methods = ['POST'])
def success():
    if request.method == "POST":
        email = request.form["email_name"]
        height = request.form["height_name"]
        if db.session.query(Data).filter(Data.email_ == email).count() == 0:
            data = Data(email, height)
            db.session.add(data)
            db.session.commit()
            average_height = db.session.query(func.avg(Data.height_)).scalar()
            average_height = round(average_height, 2)
            return render_template("success.html")
        return render_template('index.html', text = "Email already exists!")

@app.route("/uploaded", methods = ['POST'])
def upload():
    global file
    if request.method == "POST":
        file = request.files["file"]
        file.save(secure_filename("uploaded_" + file.filename))
        return render_template("uploaded.html", btn = "download.html")

@app.route("/download")
def download():
    return send_file("uploaded_" + file.filename, attachment_filename = "yourfile.csv", as_attachment = True)


if __name__ == "__main__":
    app.debug = True
    app.run()
