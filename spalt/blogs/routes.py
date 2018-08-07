from flask import Blueprint, render_template, redirect, url_for, request
from spalt.blogs.forms import PostForm
from flask_login import current_user, login_required
from spalt import db
from spalt.models import User, Blogs

blogs = Blueprint('blogs', __name__)

@blogs.route('/new/post', methods=['POST', 'GET'])
@login_required
def  create_post():
	forumType = ['Entertainment', 'Sports', 'Educational', 'Business', 'Economic', 'Money', 'Business', 'Technology']

	form = PostForm()
	if form.validate_on_submit():
		blogs = Blogs(topic=form.topic.data, content=form.content.data, author=current_user, forum_type=request.form['option'])
		db.session.add(blogs)
		db.session.commit()
		return redirect(url_for('home.main'))
	return render_template('createpost.html', form=form, forums=forumType, form_title='Create New Post')

@blogs.route('/post/<int:blog_id>', methods=['GET', 'POST'])
@login_required
def post(blog_id):
	post = Blogs.query.get_or_404(blog_id)
	return render_template('post.html', post=post)

@blogs.route('/post/<int:blog_id>/update', methods=['GET', 'POST'])
@login_required
def post_update(blog_id):
	form = PostForm()
	post = Blogs.query.get_or_404(blog_id)
	if post.author != current_user:
		abort(403)
	if form.validate_on_submit():
		post.topic = form.topic.data
		post.content = form.content.data
		db.session.commit()
		return redirect(url_for('home.main', blog_id=post.id))
	elif request.method == 'GET':
		form.topic.data = post.topic
		form.content.data = post.content
	return render_template('createpost.html', post=post, form=form, form_title='Update Post')

@blogs.route('/post/<int:blog_id>/delete', methods=['GET', 'POST'])
@login_required
def post_delete(blog_id):
	post = Blogs.query.get_or_404(blog_id)	
	if post.author == current_user:
		db.session.delete(post)
		db.session.commit()
		return redirect(url_for('home.main'))
	return render_template('post.html')