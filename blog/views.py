from flask import Blueprint, render_template

blog_blueprint = Blueprint('blog', __name__, template_folder='templates')


@blog_blueprint.route('/blog')
def blog():
    return render_template('blog.html')