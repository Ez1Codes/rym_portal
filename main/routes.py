from main import app
from flask import render_template, redirect, url_for, flash
from main.models import User, db, Activity,Blog
from main.forms import RegisterForm, LoginForm, ActivitiesForm,BlogForm
from flask_login import login_user, logout_user

@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home_page():
    activity = Activity.query.all()
    return render_template('index.html', activities=activity)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    logout_user()
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                                email=form.email_address.data,
                                password=form.password1.data,
                                about=form.about.data)
        db.session.add(user_to_create)
        db.session.commit()
        flash('Account ceated successfully! ', category='success')
        return redirect(url_for('user_blog'))

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error {err_msg}', category='danger')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash('You have successfully logged in', category='success')
            return redirect(url_for('user_blog'))
        else:
            flash('Invalid credentials! ', category='danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have successfully logged out", category='info' )
    return redirect(url_for("home_page"))

@app.route('/blog/add', methods=['GET', 'POST'])
def admin_blog():
    form = BlogForm()
    err_msg = {}
    
    if form.validate_on_submit():
        new_blog = Blog(blogname=form.blogname.data,
                        author=form.author.data,
                        content=form.blogcontent.data)
        db.session.add(new_blog)
        db.session.commit()
        flash("Blog created successfully", category='success')
        return redirect(url_for('user_blog'))
    

    if err_msg != {}:
        for err_msg in form.errors.values():
            flash(f"There was an erro {err_msg}", category='danger')

    return render_template('add_blog.html', form=form)


@app.route('/activities/add', methods=['GET', 'POST'])
def admin_activity():
    form = ActivitiesForm()
    err_msg = {}

    if form.validate_on_submit():
        new_activity = Activity(name=form.activity_name.data,
                                author=form.author.data,
                                desc=form.activity_desc.data,
                                date = form.date.data)
        db.session.add(new_activity)
        db.session.commit()
        flash("Activity added successfully", category='success')
        return redirect(url_for('user_activities'))

    if err_msg != {}:
        for err_msg in form.errors.values():
            flash(f"There was an error {err_msg}", category='danger')

    return render_template('add_activities.html', form=form)


@app.route('/blog')
def user_blog():
    blog = Blog.query.all()
    return render_template('userblog.html', blog=blog)


@app.route('/activities')
def user_activities():
    activities = Activity.query.all()
    return render_template('activities.html', activities=activities)


@app.route('/dashboard')
def dashboard():
   return render_template('dashboard.html')

@app.route('/post/<int:id>')
def post(id):
    post = Blog.query.get_or_404(id)
    return render_template('post.html', post=post)

@app.route('/post/edit/<int:id>',  methods=['GET', 'POST'])
def edit_post(id):
    post = Blog.query.get_or_404(id)
    form = BlogForm()
    if form.validate_on_submit():
        try:
            post.blogname = form.blognaname.data
            post.author = form.author.data
            post.content = form.blogcontent.data

            db.session.add(post)
            db.session.commit()
            flash("Post Updated Successfully", category='success')
            return redirect(url_for('post',id=post.id))
        except Exception as e:
            flash('there was an error updating post, try again later', category='danger')

    form.blogname.data = post.blogname
    form.author.data = post.author
    form.blogcontent.data = post.content 
    return render_template('edit_post.html', form=form)


@app.route('/post/delete/<int:id>')
def delete_post(id):
    post_to_delete = Blog.query.get_or_404(id)
    try:
        db.session.delete(post_to_delete)
        db.session.commit()
        flash("Post deleted successfully")
        blog = Blog.query.all()
        return render_template('userblog.html', blog=blog)

    except ValueError:
        post = Blog.query.all()
        return render_template('userblog.html')
        