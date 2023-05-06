import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import datetime

from sqlalchemy.sql import func

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_name = db.Column(db.String(100), nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(80), unique=True, nullable=False)
    # updated = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    desc = db.Column(db.Text)

    def __repr__(self):
        return f'<Job {self.job_name}>'


@app.route('/')
def index():
    jobs = Job.query.all()
    return render_template('home.html', jobs=jobs, utc_dt=datetime.datetime.utcnow())


def createJob(job, company, link):
    return Job(job_name=job, company_name=company, link=link)


def addToDB(job):
    db.session.add(job)
    db.session.commit()


with app.app_context():
    db.create_all()
    j2 = createJob("Manager", "Samsung", "ABC.com")
    addToDB(j2)
    app.run(debug=True)