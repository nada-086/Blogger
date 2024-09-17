from flask import Blueprint, request, jsonify, render_template, redirect
from flask_injector import inject
from flask_login import current_user
from app.models.blog import Blog
from app.services.blog import BlogService
from app.models.blog_action import BlogAction

blog = Blueprint("blog", __name__)

@blog.route('/')
@inject
def list_blog(blog_service: BlogService):
    return render_template('./blog/list.html', blogs=blog_service.get_all())

@blog.route('/create')
def create_blog():
    return render_template("./blog/create.html")

@blog.route('/create', methods=['POST'])
@inject
def store_Blog(blog_service: BlogService):
    blog_title = request.form.get('title')
    blog_content = request.form.get('content')
    blog_description = request.form.get('description')

    if not blog_title and not blog_content:
        return render_template('./blog/create.html', message="All Fields are Required.")
    
    try:
        blog_service.create(title=blog_title, content=blog_content, description=blog_description, user_id=current_user.id)
    except Exception as e:
        return render_template('./blog/create.html', message=e)
    return redirect('/blogs')

@blog.route('/<id>')
@inject
def view_blog(blog_service: BlogService, id):
    blog = blog_service.get_by_id(id)
    if not Blog:
        return redirect('/blogs')
    author = blog_service.get_author(blog.author_id)
    return render_template('./blog/view.html', blog=blog, author=author)

@blog.route('/<id>/edit')
@inject
def edit_blog(Blog_service: BlogService, id):
    blog = Blog_service.get_by_id(id)
    if not blog:
        return redirect('/blog')
    return render_template('./blog/edit.html', blog=blog)

@blog.route('/<id>', methods=['POST'])
@inject
def update_blog(blog_service: BlogService, id):
    blog = blog_service.get_by_id(id)
    if not blog:
        return render_template('./blog/view.html', message="Page Not Found")
    blog_title = request.form.get('title')
    blog_description = request.form.get('description')
    blog_content = request.form.get('content')
    if not blog_title or not blog_content or not blog_description:
        return render_template('./blog/view.html', blog=blog, message="All fields are required.")
    blog_service.update(Blog, blog_title, blog_content, blog_description)
    return render_template('./blog/view.html', blog=blog)

@blog.route('/<id>/delete')
@inject
def delete_Blog(blog_service: BlogService, id):
    blog = blog_service.get_by_id(id)
    if not blog:
        return redirect('/blogs')
    blog_service.delete(blog)
    return render_template('./user/profile.html', blog=blog_service.get_all())

@blog.route('/<id>/like')
def like_blog(blog_service: BlogService, id):
    blog = blog_service.get_by_id(id)
    if not blog:
        return redirect('/blogs')
    try:
        blog_service.like(blog, current_user)
    except Exception as e:
        return render_template('./blog/view.html', blog=blog, message="You already liked it.")
    return redirect(f'/blogs/{id}')

@blog.route('/<id>/dislike')
def dislike_blog(blog_service: BlogService, id: int):
    blog = blog_service.get_by_id(id)
    if not blog:
        return redirect('/blogs')
    try:
        blog_service.dislike(blog, current_user)
    except Exception as e:
        return render_template('./blog/view.html', blog=blog, message="You already disliked it.")
    return redirect(f'/blogs/{id}')
