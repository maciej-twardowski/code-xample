from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField,\
    SubmitField, SelectField, HiddenField
from wtforms.validators import DataRequired, Length


# todo ~~~~~~~~~ Validation ~~~~~~~~~~


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[Length(min=4)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class LinksToDisplayForm(FlaskForm):
    tech = SelectField('Technology', validators=[], coerce=str)
    diff = SelectField('Difficulty', validators=[], coerce=str)
    submit = SubmitField('Display links')

    def set_tech_options(self, tech_options):
        self.tech.choices = tech_options

    def set_diff_options(self, diff_options):
        self.diff.choices = diff_options


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[Length(min=4)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[Length(min=4)])
    body = StringField('Body', validators=[])
    link = StringField('Link', validators=[Length(min=3)])
    tech = SelectField('Technology')
    diff = SelectField('Difficulty')
    submit = SubmitField('Add')

    def set_tech_options(self, tech_options):
        self.tech.choices = tech_options

    def set_diff_options(self, diff_options):
        self.diff.choices = diff_options
