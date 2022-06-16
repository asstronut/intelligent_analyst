from flask_login import current_user, login_required, login_user, logout_user
from app import app, db, admin
from flask import flash, redirect, render_template, request, url_for
from app.forms import LoginForm, RegistrationForm
from app.models import Users
from app.admin import UserModelView
from werkzeug.urls import url_parse


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():   # if POST & data valid -> true
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        u = Users(name=form.name.data, email=form.email.data)
        u.set_password(password=form.password.data)
        db.session(u)
        db.commit()
        flash('Congratulations! Your account has been created!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/about')
@login_required
def about():
    return render_template('about.html')


@app.route('/portofolio')
@login_required
def portofolio():
    return render_template('portofolio.html')


@app.route('/contact')
@login_required
def contact():
    return render_template('contact.html')


@app.route('/menudashboard')
@login_required
def menudashboard():
    return render_template('menudashboard.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


admin.add_view(UserModelView(Users, db.session))
