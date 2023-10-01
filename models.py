from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import validates


db=SQLAlchemy()

class Hero(db.Model):
    __tablename__ = 'hero'
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(50), index=True)
    super_name=db.Column(db.String(50), index=True)
    created_at=db.Column(db.DateTime, default=datetime.utcnow)
    updated_at=db.Column(db.DateTime, default=datetime.utcnow)
    hero_powers=db.relationship('Hero_powers', backref='hero')
    
    

class HeroPowers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String(1000000), unique=True, index=True)
    hero_id = db.Column(db.Integer, db.ForeignKey('hero.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('power.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    powers = db.relationship('Power', backref='hero_powers')
    
    
    @validates('strength')
    def validate_strength(self, key, strength):
        if not strength:
            raise ValueError('Strength is required.')
        if len(strength) > 1000000:
            raise ValueError('Strength must be less than or equal to 1000000 characters.')
        return strength
    
class Power(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(50), unique=False, index=True)
    description=db.Column(db.Text(), unique=False, index=True)
    created_at=db.Column(db.DateTime, default=datetime.utcnow)
    updated_at=db.Column(db.DateTime, default=datetime.utcnow)
    
    
    
    @validates('description')
    def validate_description(self, key, description):
        if not description:
            raise ValueError('Description is required.')
        if len(description) > 255:
            raise ValueError('Description must be less than or equal to 255 characters.')
        return description