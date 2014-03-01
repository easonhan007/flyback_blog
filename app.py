from flask import Flask
from flask import g
from pymongo import Connection
from flask import render_template

app = Flask(__name__)
app.debug = True

@app.before_request
def before_request():
	conn = Connection()
	g.db = conn.test 
	g.page_size = 5

def get_lists(page=1):
	skip = (page - 1) * g.page_size
	return g.db.post.find().skip(skip).limit(g.page_size)

def get_post(id):
	return g.db.post.find_one({'_id': id})

def get_lasted_post():
	return g.db.post.find_one()

@app.route('/')
def post_list():
	print(get_lasted_post())
	return render_template('index.html')

if __name__ == '__main__':
    app.run()