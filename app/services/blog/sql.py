from app.models.sql.blog import Blog
from app.models.sql.user import User
from app.models.sql.blog_action import BlogAction
from flask_sqlalchemy import SQLAlchemy
from flask_injector import inject
from flask_login import current_user


class SQLiteBlogService:
    @inject
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def get_all(self):
        return self.db.session.query(Blog).all()
    
    def get_author(self, author_id):
        author = self.db.session.query(User).filter_by(id=author_id).first()
        return author.name

    def create(self, title, content, description, user_id):
        blog = self.db.session.query(Blog).filter_by(title=title).first()
        if (blog):
            raise Exception('Please, Choose a Unique Title for Your Blog.')
        new_blog = Blog(title=title, content=content, description=description, author_id=user_id)
        self.db.session.add(new_blog)
        self.db.session.commit()

    def get_by_id(self, id):
        return self.db.session.query(Blog).filter_by(id=id).first()

    def update(self, blog, title, content, description):
        blog.title = title
        blog.content = content
        blog.description = description
        self.db.session.commit()

    def delete(self, blog):
        if blog.author_id == current_user.id or current_user.role == "Admin":
            self.db.session.delete(blog)
            self.db.session.commit()
        else:
            raise Exception("Unauthorized Action.")



    def like(self, blog, user_id):
        existing_action = self.db.session.query(BlogAction).filter_by(user_id=user_id, blog_id=blog.id).first()
        if existing_action:
            if existing_action.action == 'like':
                raise Exception('You have already liked this blog.')
            elif existing_action.action == 'dislike':
                existing_action.action = 'like'
                blog.likes += 1
                blog.dislikes -= 1
        else:
            blog_action = BlogAction(user_id=user_id, blog_id=blog.id, action='like')
            blog.likes += 1
            self.db.session.add(blog_action)
        self.db.session.commit()


    def dislike(self, blog, user_id):
        existing_action = self.db.session.query(BlogAction).filter_by(user_id=user_id, blog_id=blog.id).first()
        if existing_action:
            if existing_action.action == 'dislike':
                raise Exception('You have already disliked this blog.')
            elif existing_action.action == 'like':
                existing_action.action = 'dislike'
                blog.likes -= 1
                blog.dislikes += 1
        else:
            blog_action = BlogAction(user_id=user_id, blog_id=blog.id, action='dislike')
            blog.dislikes += 1
            self.db.session.add(blog_action)
        self.db.session.commit()