from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField,\
    SubmitField, SelectField, HiddenField
from wtforms.validators import DataRequired, ValidationError, EqualTo, InputRequired


# todo ~~~~~~~~~ Validation ~~~~~~~~~~


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
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
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

    # def validate_username(self, username):
    #     user = User.query.filter_by(username=username.data).first()
    #     if user is not None:
    #         raise ValidationError('Please use a different username.')


class PostForm(FlaskForm):
    author_name = HiddenField(validators=[])
    title = StringField('Title', validators=[InputRequired('Title required')])
    body = StringField('Body', validators=[])
    link = StringField('Link', validators=[])
    tech = SelectField('Technology') #validators=[], coerce=str
    diff = SelectField('Difficulty') #, validators=[], coerce=str
    submit = SubmitField('Add')

    def set_tech_options(self, tech_options):
        self.tech.choices = tech_options

    def set_diff_options(self, diff_options):
        self.diff.choices = diff_options
