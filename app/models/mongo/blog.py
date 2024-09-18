from mongoengine import Document, StringField, ReferenceField, IntField, DateTimeField
from datetime import datetime

class Blog(Document):
    title = StringField(max_length=100, required=True, unique=True)
    description = StringField(required=True)
    content = StringField(required=True)
    author_id = ReferenceField('User', required=True)
    created_at = DateTimeField(default=datetime.utcnow)
    likes = IntField(default=0)
    dislikes = IntField(default=0)

    meta = {
        'collection': 'blogs',
        'indexes': [
            'title',
            'author_id',
        ]
    }
