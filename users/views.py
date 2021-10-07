from flask import Blueprint, render_template, request, flash
from app import db
from models import User
from users.forms import RegisterForm

users_blueprint = Blueprint('users', __name__, template_folder='templates')


@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user:
            flash('Username address already exists')
            return render_template('register.html', form=form)

        new_user = User(username=form.username.data, password=form.password.data)

        db.session.add(new_user)
        db.session.commit()
        print(request.form.get('username'))  # todo remove
        print(request.form.get('password'))  # TODO remove
        return login()

    return render_template('register.html', form=form)


@users_blueprint.route('/login')
def login():
    return render_template('login.html')