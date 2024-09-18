from flask import Blueprint, request, render_template, redirect
from flask_injector import inject
from flask_login import current_user
from app.services.blog.factory import BlogServiceFactory

blog = Blueprint("blog", __name__)

@blog.route('/')
@inject
def list_blog(blog_service: BlogServiceFactory):
    service = blog_service.get_service()
    return render_template('./blog/list.html', blogs=service.get_all())

@blog.route('/create')
def create_blog():
    return render_template("./blog/create.html")

@blog.route('/create', methods=['POST'])
@inject
def store_blog(blog_service: BlogServiceFactory):
    service = blog_service.get_service()
    blog_title = request.form.get('title')
    blog_content = request.form.get('content')
    blog_description = request.form.get('description')

    if not blog_title or not blog_content:
        return render_template('./blog/create.html', message="All Fields are Required.")
    
    try:
        service.create(title=blog_title, content=blog_content, description=blog_description, user_id=current_user.id)
    except Exception as e:
        return render_template('./blog/create.html', message=str(e))
    return redirect('/blogs')

@blog.route('/<id>')
@inject
def view_blog(blog_service: BlogServiceFactory, id):
    service = blog_service.get_service()
    blog = service.get_by_id(id)
    if not blog:
        return redirect('/blogs')
    author = service.get_author(blog.author_id)
    return render_template('./blog/view.html', blog=blog, author=author)

@blog.route('/<id>/edit')
@inject
def edit_blog(blog_service: BlogServiceFactory, id):
    service = blog_service.get_service()
    blog = service.get_by_id(id)
    if not blog:
        return redirect('/blogs')
    return render_template('./blog/edit.html', blog=blog)

@blog.route('/<id>', methods=['POST'])
@inject
def update_blog(blog_service: BlogServiceFactory, id):
    service = blog_service.get_service()
    blog = service.get_by_id(id)
    if not blog:
        return render_template('./blog/view.html', message="Page Not Found")
    
    blog_title = request.form.get('title')
    blog_description = request.form.get('description')
    blog_content = request.form.get('content')
    author = service.get_author(blog.author_id)
    
    if not blog_title or not blog_content or not blog_description:
        return render_template('./blog/view.html', blog=blog, message="All fields are required")
    
    service.update(blog, blog_title, blog_content, blog_description)
    return render_template('./blog/view.html', blog=blog, author=author)

@blog.route('/<id>/delete')
@inject
def delete_blog(blog_service: BlogServiceFactory, id):
    service = blog_service.get_service()
    blog = service.get_by_id(id)
    if not blog:
        return redirect('/blogs')
    service.delete(blog)
    return render_template('./user/profile.html', blogs=service.get_all(), user=current_user)

@blog.route('/<id>/like')
@inject
def like_blog(blog_service: BlogServiceFactory, id):
    service = blog_service.get_service()
    blog = service.get_by_id(id)
    if not blog:
        return redirect('/blogs')
    
    try:
        service.like(blog, current_user.id)
    except Exception as e:
        return render_template('./blog/view.html', blog=blog, message=e)
    
    return redirect(f'/blogs/{id}')

@blog.route('/<id>/dislike')
@inject
def dislike_blog(blog_service: BlogServiceFactory, id):
    service = blog_service.get_service()
    blog = service.get_by_id(id)
    if not blog:
        return redirect('/blogs')
    
    try:
        service.dislike(blog, current_user.id)
    except Exception as e:
        return render_template('./blog/view.html', blog=blog, message=e)
    
    return redirect(f'/blogs/{id}')
