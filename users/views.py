from flask import Blueprint, render_template, request
from users.forms import RegisterForm

users_blueprint = Blueprint('users', __name__, template_folder='templates')


@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        print(request.form.get('username'))
        print(request.form.get('password'))
        return login()

    return render_template('register.html', form=form)


@users_blueprint.route('/login')
def login():
    return render_template('login.html')