from deepdive.database import db
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class User(db.Model,UserMixin): #inherit db.Model from SQLAlchemy and UserMixin is a layer of security to check if something is in the session

    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(200),nullable=False)
    password = db.Column(db.String(250),nullable=False)
    project= db.Column(db.String(250),nullable=False)
    created_at = db.Column(db.DateTime,nullable=False,default=datetime.now)
    updated_at = db.Column(db.DateTime,nullable=False,default=datetime.now,onupdate=datetime.now)
    manual_analysis = db.relationship("ManualAnalysis",backref="users")

class ManualAnalysis(db.Model):

    __tablename__ = 'manual_analysis'

    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,ForeignKey('users.id'))
    diagfile = db.Column(db.String(200),nullable=False)
    rse_state = db.Column(db.String(100),nullable=False)
    build_package = db.Column(db.String(200),nullable=False)
    adk = db.Column(db.String(100),nullable=False)
    date_time = db.Column(db.DateTime)
    analysis = db.Column(db.String(1000),nullable=False)
    jira = db.Column(db.String(200),nullable=False)
    category = db.Column(db.String(200),nullable=False)
    device_error = db.Column(db.String(200),nullable=False)
    gsa = db.Column(db.String(200),nullable=False)
    hwtype = db.Column(db.String(200),nullable=False)
    motherboard = db.Column(db.String(200),nullable=False)
    dbmanager = db.Column(db.String(200),nullable=False)
    created_at = db.Column(db.DateTime,nullable=False,default=datetime.now)
    updated_at = db.Column(db.DateTime,nullable=False,default=datetime.now,onupdate=datetime.now)


class UploadAnalysis(db.Model):

    __tablename__ = 'upload_analysis'

    id = db.Column(db.Integer,primary_key=True)
    diagfile_name = db.Column(db.String(200),nullable=False)
    adk = db.Column(db.String(100),nullable=False)
    trace_check=  db.Column(db.String(100))
    build= db.Column(db.String(200),nullable=False)
    probdate  = db.Column(db.String(100),nullable=False)
    probtime = db.Column(db.String(100),nullable=False)
    trx_comp = db.Column(db.String(100))
    analysis = db.Column(db.String(1000),nullable=False)
    associated_jira = db.Column(db.String(200))
    category = db.Column(db.String(200),nullable=False)
    type_reboot = db.Column(db.String(100))
    fix_build = db.Column(db.String(100))
    detected = db.Column(db.String(100))
    assigned = db.Column(db.String(100))
    device_error = db.Column(db.String(200))
    gsa_version	= db.Column(db.String(200),nullable=False)
    full_mini = db.Column(db.String(100))
    hw_type	= db.Column(db.String(200),nullable=False)
    motherboard	= db.Column(db.String(200),nullable=False)
    sub_category = db.Column(db.String(100))
    rse_state = db.Column(db.String(100),nullable=False)
    storenum = db.Column(db.String(100))
    lanenum = db.Column(db.String(100))
    dbmgr = db.Column(db.String(200),nullable=False)


class RseFile(db.Model):

    __tablename__ = 'rse_reports'

    id = db.Column(db.Integer,primary_key=True)
    store = db.Column(db.String(500))
    country = db.Column(db.String(500))
    lane = db.Column(db.String(500))
    device = db.Column(db.String(500))
    rse_date = db.Column(db.String(500))
    rse_time = db.Column(db.String(500))
    tender_state = db.Column(db.String(500))
    state = db.Column(db.String(500))
    diagfile_name = db.Column(db.String(500))
    build = db.Column(db.String(500))
    time = db.Column(db.String(500))
    analysis = db.Column(db.String(1000))
    jira = db.Column(db.String(500))
    Category = db.Column(db.String(500))
    types_of_reboot = db.Column(db.String(500))
    gsa_version = db.Column(db.String(500))
    device_error = db.Column(db.String(500))
    assign = db.Column(db.String(500))
    second_review = db.Column(db.String(500))
    null_data = db.Column(db.String(500))
    jira_or_gsa = db.Column(db.String(500))
    operational_review = db.Column(db.String(500))
    hwtype = db.Column(db.String(500))
    motherboard = db.Column(db.String(500))
    operational_reviewed_by = db.Column(db.String(500))
    sa_server = db.Column(db.String(500))
    data = db.Column(db.String(500))
    adk = db.Column(db.String(500))
    ps_package = db.Column(db.String(500))
    fix_version = db.Column(db.String(500))


def is_active(self):
    return True

def is_authenticated(self):
    return True
