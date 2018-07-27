from flask import Blueprint, render_template
from flask_login import login_required
from spalt.models import Blogs

home = Blueprint('home', __name__)


@home.route('/main')
@login_required
def main():
	posts = Blogs.query.order_by(Blogs.date_created.asc())
	return render_template('home.html', posts=posts)