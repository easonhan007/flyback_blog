#-*- coding:utf8 -*-
import os
from flask import Flask, g, render_template, request, session, redirect, url_for, flash
from pymongo import Connection
import datetime
import markdown
from bson.objectid import ObjectId

ENV = os.getenv('ENV', 'development')

def vender_markdown(txt):
	return markdown.markdown(txt)

app = Flask(__name__)
if not ENV == 'production':
	app.debug = True
if ENV == 'production':
	from werkzeug.contrib.fixers import ProxyFix
	app.wsgi_app = ProxyFix(app.wsgi_app)

app.secret_key = '\x86\xdb;\x91\x9dQfX4\x151\xc0\xf1\x9c\xc1\xac\x87\xb1uk\x19$\xd0\xbb'
app.jinja_env.globals.update(vender_markdown=vender_markdown)

@app.before_request
def before_request():
	conn = Connection()
	g.db = conn.test 
	g.page_size = 5

def get_lists(page=1):
	skip = (page - 1) * g.page_size
	return g.db.posts.find().skip(skip).limit(g.page_size).sort('_id', -1)

def get_post(post_id):
	return g.db.posts.find_one({'_id': ObjectId(post_id)})

def update(post_id, data):
	return g.db.posts.update({'_id': ObjectId(post_id)}, data)

def is_logged_in():
	if 'user' in session: return True
	return False

def split_tags(tags):
	if not tags:
		return tags.split(' ')
	return []


@app.route('/')
def post_list():
	page = int(request.args.get('page', 1))
	posts = get_lists(page)
	return render_template('index.html', posts = posts)

@app.route('/show/<post_id>')
def show_post(post_id):
	post = get_post(post_id)
	if(post):
		return render_template('index.html', posts= [post])
	else:
		flash('Can not find post', 'warning')
		return redirect(url_for('post_list'))

@app.route('/login', methods=['POST', 'GET'])
def login():
	if request.method == 'GET':
		return render_template('login_form.html')

	if request.method == 'POST':
		user = g.db.users.find_one({'name': request.form['user_name'], 'password': request.form['password']})
		if(user):
			session['user'] = user['name']
			msg = 'Login successfully!'
			msg_type = 'success'
			action = 'post_list'
		else:
			msg = 'Can not login!'
			msg_type = 'danger'
			action = 'login'

		flash(msg, msg_type)
		return redirect(url_for(action))

@app.route('/logout')
def logout():
	session.pop('user', None)
	flash('Logout successfully', 'info')
	return redirect(url_for('post_list'))

@app.route('/admin/create_post', methods=['GET', 'POST'])
def create_post():
	if not is_logged_in(): 
		flash('You should login first', 'danger')
		return redirect(url_for('login'))

	if request.method == 'POST':
		data = request.form.to_dict()
		data['tags'] = split_tags(data['tags'])
		data['created_at'] = data['updated_at'] = datetime.datetime.now()
		data['creator'] = session['user']

		if not data['title']:
			flash('Title can not be empty', 'warning')
			return render_template('edit_post_form.html', post=data)

		if g.db.posts.insert(data):
			flash('Create post successfully', 'success')
			return redirect(url_for('post_list'))
		else:
			flash('Failed to create post', 'danger')
			return redirect(url_for('create_post'))

	return render_template('create_post_form.html')

@app.route('/admin/edit_post/<post_id>')
def edit_post(post_id):
	if not is_logged_in(): 
		flash('You should login first', 'danger')
		return redirect(url_for('login'))

	post = get_post(post_id)
	if(post):
		return render_template('edit_post_form.html', post=post)
	else:
		flash('Can not find this post', 'warning')
		return redirect(url_for('post_list'))

@app.route('/admin/update_post', methods=['POST'])
def update_post():
	if not is_logged_in(): 
		flash('You should login first', 'danger')
		return redirect(url_for('login'))

	data = request.form.to_dict()
	if not data['title']:
		flash('Title can not be empty', 'warning')
		return render_template('edit_post_form.html', post=data)
	
	data['tags'] = split_tags(data['tags'])
	data['updated_at'] = datetime.datetime.now()
	post_id = data.pop('id', None)
	update(post_id, data)
	flash('Edit successfully', 'success')
	return redirect(url_for('show_post', post_id=post_id))

if __name__ == '__main__':
	app.run()