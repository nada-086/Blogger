from app import db
from datetime import datetime

class BlogAction(db.Model):
    __tablename__ = 'blog_actions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'), nullable=False)
    action = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # user = db.relationship('User', backref=db.backref('actions', cascade='all, delete-orphan'))
    # blog = db.relationship('Blog', backref=db.backref('actions', cascade='all, delete-orphan'))
