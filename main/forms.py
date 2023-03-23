from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,ValidationError
from wtforms.validators import Length, EqualTo, DataRequired, Email
from main.models import User,Activity,Blog
from flask_ckeditor import CKEditorField
from datetime import date
class RegisterForm(FlaskForm):

    def validate_username(self,username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exist')

    def validate_email_address(self,email_address_to_check):
        email_address = User.query.filter_by(email=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email already exist')

    username = StringField(label='User Name: ' , validators=[Length(min=4, max=30), DataRequired()])
    email_address = StringField(label='Email Address: ', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='password: ', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password: ', validators=[EqualTo('password1'), DataRequired()])
    about = StringField(label='About Yourself: ', validators=[DataRequired()])
    submit = SubmitField(label='submit')



class LoginForm(FlaskForm):
    username = StringField(label='username', validators=[DataRequired()])
    password = PasswordField(label='password', validators=[DataRequired()])
    submit = SubmitField(label='signin')


class ActivitiesForm(FlaskForm):

    activity_name = StringField(label='Activity name: ', validators=[DataRequired()])
    activity_desc = CKEditorField('Content', validators=[DataRequired()])
    date = StringField('Date', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    add = SubmitField(label='Ok')

    def validate_activity_name(self,name_to_check):
        activity_name = Activity.query.filter_by(name=name_to_check.data).first()
        if activity_name:
            raise ValidationError('Activity already exist')




class BlogForm(FlaskForm):

    blogname = StringField(label='Activity name: ', validators=[DataRequired()])
    blogcontent = CKEditorField('Content', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    create = SubmitField(label='Create Blog')

    def validate_blogname(self,blogname_to_check):
        blogname = Blog.query.filter_by(blogname=blogname_to_check.data).first()
        if blogname:
            raise ValidationError('Blog already exist')




class DeleteBlog(FlaskForm):
    submit = SubmitField(label='Delete')