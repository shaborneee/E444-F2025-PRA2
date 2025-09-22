from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, ValidationError, Email
from wtforms.fields import StringField, SubmitField

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
bootstrap = Bootstrap(app)
moment = Moment(app)

# Custom validator for '@' in email
def validate_at_symbol(form, field):
    if '@' not in field.data:
        raise ValidationError(f"Please include an '@' in the email address.'{form.name.data or 'User'}' is missing an '@'")

class NameForm(FlaskForm):
    name = StringField('What is your name?', 
                       validators=[DataRequired()])
    email = StringField(
        'What is your UofT Email address', 
        validators=[
            DataRequired(),
            validate_at_symbol
        ]
    )
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    email_invalid = False
    email_value = session.get('email') 

    if form.validate_on_submit():
        old_name = session.get('name')
        old_email = session.get('email')
        submitted_email = form.email.data.strip()

        if 'utoronto' not in submitted_email.lower():
            email_invalid = True
        else:
            email_value = submitted_email

            if old_name and old_name != form.name.data:
                flash(f"Changed your username to {form.name.data}")
            if old_email and old_email != submitted_email:
                flash(f"Changed your email to {submitted_email}")

            session['name'] = form.name.data
            session['email'] = submitted_email
            return redirect(url_for('index'))

    return render_template(
        'index.html',
        form=form,
        name=session.get('name'),
        email=email_value,
        email_invalid=email_invalid
    )

