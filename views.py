from app import app, model
from app import db
from flask import render_template, request, flash, redirect, url_for
import base64
from flask_login import login_user, current_user, login_required, logout_user
from .forms import LoginForm
from .forms import RegisterForm
from .forms import UserDateForm


@app.route('/')
@app.route('/index')
def index():
	text = {'asdf': 'asdgf'}
	numbers = ["asds", "afsd", "asdsa", "asdfasd", "asfasd", "agasdasd", "gasdasdf"]
	numbers_next = [(numbers[3]), numbers[5]]
	return render_template("index.html", out_text=text['asdf'], title="asdasdas", numbers=numbers_next)


@app.route('/base')
def person():
	return render_template("base.html")


@app.route('/contacts')
def contacts():
	return render_template("contacts.html")


@app.route('/about')
def about():
	return render_template("about.html")


@app.route('/services')
def services():
	return render_template("services.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegisterForm()
	if form.validate_on_submit():
		login = form.loginField.data
		userCred = model.UserCredentials.query.filter_by(login=login).first()
		if userCred != None:
			flash("Email exists")
			render_template("register.html", form=form)
		else:
			password = form.passwordField.data
			user = model.User()
			db.session.add(user)
			db.session.commit()
			db.session.refresh(user)
			userCred = model.UserCredentials(login, password, user.id)
			db.session.add(userCred)
			db.session.commit()
			db.session.refresh(userCred)
			flash(userCred.id)
			login_user(user)
			return redirect(url_for('user_data'))
	return render_template("register.html", form=form)


@app.route('/group')
def group():
	if current_user.is_authenticated:
		if current_user.type_id == 1:
			users = model.User.query.all()
			for us in users:
				picture = model.Picture.query.filter_by(user_id=us.id).first()
				us.picture = base64.b64encode(picture.picture).decode("utf-8")
			return render_template("group.html", users=users)
		else:
			if model.m2m_user_group.query.filter_by(user_id=current_user.id).first() == None:
				return render_template("group.html", group = None, users = None)
			else:
				group_id = model.m2m_user_group.query.filter_by(user_id=current_user.id).first().group_id
				group = model.Group.query.filter_by(id = group_id).first()
				m2m_users = model.m2m_user_group.query.filter_by(group_id=group.id).all()
				users = []
				for user in m2m_users:
					users.append(model.User.query.filter_by(id = user.user_id).first())
				return render_template("group.html", group=group, users = users)
	else:
		return redirect(url_for('login'))


@app.route('/user_data', methods=['GET', 'POST'])
def user_data():
	if current_user.is_authenticated:
		form = UserDataForm()
		if form.validate_on_submit():
			current_user.name = form.nameField.data
			current_user.surname = form.surnameField.data
			current_user.lastname = form.lastnameField.data
			db.session.add(current_user)
			db.session.commit()

		return render_template("user_data.html", form=form)



@app.route('/user_info')
def user_info():
	if current_user.is_authenticated:
		m2m_u_s = model.UserSubject.query.filter_by(user_id=current_user.id).all()
		subjects = []
		pictures = model.Picture.query.filter_by(user_id=current_user.id).all()
		for pic in pictures:
			pic.picture = base64.b64encode(pic.picture).decode("utf-8")
			for i in m2m_u_s:
				subjects.append(model.Subject.query.filter_by(id=i.subject_id).first())
				return render_template('user_info.html', user=current_user, user_type=current_user.type_id, subjects=subjects, pictures=pictures)
			else:
				return redirect(url_for('login'))


@app.route('/subject_info')
def subject_info():
	subject_id = request.args.get('subject_id')
	subject = model.Subject.query.filter_by(id=subject_id).first()
	m2m_u_s = model.UserSubject.query.filter_by(subject_id=subject_id).all()
	students = []

	for i in m2m_u_s:
		if model.User.query.filter_by(id=i.user_id).first().type_id == 2:
			students.append(model.User.query.filter_by(id=i.user_id).first())
			flash(i.user_id)
			for i in students:
				if i == None:
					continue
				else:
					picture = model.Picture.query.filter_by(user_id=i.id).first()
					i.picture = base64.b64encode(picture.picture).decode("utf-8")
					return render_template('subject_info.html', subject=subject, user_type=current_user.type_id, students=students)


@app.route('/login', methods=['GET', 'POST'])
def login():
	if not current_user.is_authenticated:
		form = LoginForm()
		if form.validate_on_submit():
			userCredentials = model.UserCredentials.query.filter_by(login=form.loginField.data).first()
			if userCredentials is None:
				flash('no such user')
			else:
				if userCredentials.password == form.passwordField.data:
					user = model.User.query.filter_by(id=userCredentials.id).first()
					flash('Login good')
					user_type = model.UserType.query.filter_by(id=user.type_id).first()
					login_user(user)
					return redirect(url_for('user_info'))
				else:
					flash('incorrect password')
					return render_template('login.html', title='login', form=form)
	else:
		return redirect(url_for('user_info'))
		return render_template('login.html', title='login', form=form)


@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('login'))
