from bson import ObjectId
from mongoengine import DoesNotExist
from app.models.mongo.blog import Blog
from app.models.mongo.blog_action import BlogAction
from injector import inject
from flask_login import current_user

class MongoBlogService:
    @inject
    def __init__(self):
        pass

    def get_all(self):
        return Blog.objects()

    def get_author(self, author):
        try:
            return author.name
        except Exception:
            return None

    def create(self, title, content, description, user_id):
        if Blog.objects(title=title).first():
            raise Exception('Please, Choose a Unique Title for Your Blog.')
        new_blog = Blog(title=title, content=content, description=description, author_id=user_id)
        new_blog.save()

    def get_by_id(self, id):
        try:
            return Blog.objects.get(id=id)
        except DoesNotExist:
            return None

    def update(self, blog, title, content, description):
        blog.update(set__title=title, set__content=content, set__description=description)

    def delete(self, blog):
        if blog.author_id == current_user.id or current_user.role == "Admin":
            blog.delete()
        else:
            raise Exception("Unauthorized Action.")

    def like(self, blog, user_id):
        existing_action = BlogAction.objects(user_id=user_id, blog_id=blog.id).first()
        if existing_action:
            if existing_action.action == 'like':
                raise Exception('You have already liked this blog.')
            elif existing_action.action == 'dislike':
                existing_action.update(set__action='like')
                blog.update(inc__likes=1, dec__dislikes=1)
        else:
            BlogAction(user_id=user_id, blog_id=blog.id, action='like').save()
            blog.update(inc__likes=1)

    def dislike(self, blog, user_id):
        existing_action = BlogAction.objects(user_id=user_id, blog_id=blog.id).first()
        if existing_action:
            if existing_action.action == 'dislike':
                raise Exception('You have already disliked this blog.')
            elif existing_action.action == 'like':
                existing_action.update(set__action='dislike')
                blog.update(inc__dislikes=1, dec__likes=1)
        else:
            BlogAction(user_id=user_id, blog_id=blog.id, action='dislike').save()
            blog.update(inc__dislikes=1)