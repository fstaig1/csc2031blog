# IMPORTS
import logging
import socket
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


# LOGGING
class SecurityFilter(logging.Filter):
    def filter(self, record):
        return "SECURITY" in record.getMessage()


fh = logging.FileHandler('CSC2031blog.log', 'w')
fh.setLevel(logging.WARNING)
fh.addFilter(SecurityFilter())
formatter = logging.Formatter('%(asctime)s : %(message)s', '%m/%d/%Y %I:%M:%S %p')
fh.setFormatter(formatter)

logger = logging.getLogger('')
logger.propagate = False
logger.addHandler(fh)

# CONFIG
app = Flask(__name__)
app.config['SECRET_KEY'] = 'LongAndRandomSecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['RECAPTCHA_PUBLIC_KEY'] = "6LfaX9ocAAAAABWeVBjjXEZTI5tmcxVkO0fDi32J"
app.config['RECAPTCHA_PRIVATE_KEY'] = "6LfaX9ocAAAAAOxnUEOo0NLzPjxI693BOmeuI9gj"

db = SQLAlchemy(app)


# HOME PAGE VIEW
@app.route('/')
def index():
    return render_template('index.html')


# ERROR PAGE VIEWS
@app.errorhandler(403)
def page_forbidden(error):
    return render_template('403.html'), 403


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500


# MAIN
if __name__ == '__main__':
    my_host = "127.0.0.1"
    free_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    free_socket.bind((my_host, 0))
    free_socket.listen(5)
    free_port = free_socket.getsockname()[1]
    free_socket.close()

    login_manager = LoginManager()
    login_manager.login_view = 'users.login'
    login_manager.init_app(app)

    from models import User


    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))


    # BLUEPRINTS
    from users.views import users_blueprint
    from blog.views import blog_blueprint

    app.register_blueprint(users_blueprint)
    app.register_blueprint(blog_blueprint)
    app.run(host=my_host, port=free_port, debug=True)
