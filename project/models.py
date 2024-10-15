from . import db
from datetime import datetime


class JHA(db.Model):
    __tablename__ = 'jha'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    job_description = db.Column(db.Text, nullable=False)
    job_location = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    steps = db.relationship('Step', backref='jha', cascade='all, delete-orphan', lazy=True)

class Step(db.Model):
    __tablename__ = 'step'


    id = db.Column(db.Integer, primary_key=True)
    jha_id = db.Column(db.Integer, db.ForeignKey('jha.id'), nullable=False)
    step_number = db.Column(db.Integer, nullable=False)
    step_description = db.Column(db.Text, nullable=False)
    
    hazards = db.relationship('Hazard', backref='step', cascade='all, delete-orphan', lazy=True)

class Hazard(db.Model):
    __tablename__ = 'hazard'

    id = db.Column(db.Integer, primary_key=True)
    step_id = db.Column(db.Integer, db.ForeignKey('step.id'), nullable=False)
    description = db.Column(db.Text, nullable=False)
    controls = db.Column(db.Text, nullable=False)
