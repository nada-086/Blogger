from mongoengine import Document, StringField, DateTimeField, ReferenceField
from datetime import datetime

class BlogAction(Document):
    user_id = ReferenceField('User', required=True)
    blog_id = ReferenceField('Blog', required=True)
    action = StringField(max_length=10)
    created_at = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'blog_actions',
        'indexes': [
            'user_id',  # Adding an index for efficient querying by user
            'blog_id',  # Adding an index for efficient querying by blog
            {'fields': ['user_id', 'blog_id'], 'unique': True},  # Ensure one action per user-blog combination
        ]
    }
