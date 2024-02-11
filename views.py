from flask import Blueprint, render_template, flash
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import TelField, SubmitField
from wtforms.validators import DataRequired
import datetime
from . import db
from .models import TXTRecords
from . import models


# Create a Blueprint named 'views'
views = Blueprint('views', __name__)

# Define the welcome function for the homepage route
@views.route('/')
def home():
    return render_template('home.html', user=current_user)

# Define routes for other pages
@views.route('/bibliography')
def bibliography():
    return render_template('bibliography.html', user=current_user)

@views.route('/contact')
def contact():
    return render_template('contact.html', user=current_user)

@views.route('/make_wish')
def make_wish():
    return render_template('make_wish.html', user=current_user)

@views.route('/thankyou')
def thankyou():
    return render_template('thankyou.html', user=current_user)

# Define a form class for BMI input
class MyForm(FlaskForm):
    text = TelField('Enter here', validators=[DataRequired()])
    save_submit = SubmitField('Submit')

@views.route('/make_wish', methods=['GET', 'POST'])
# Ensure that the user is logged in to access this route
@login_required
def txt():
    # Initialize variables
    text = None
    # Create an instance of the MyForm class
    Form = MyForm()

    # If the form is submitted and passes validation
    if Form.validate_on_submit():
        try:
            text = str(Form.text.data)
            now = f'{datetime.datetime.now().date().strftime("%d-%m-%Y")}'
            
            if Form.save_submit.data:
                flash('Message Saved')
                new_record = TXTRecords(user_id=current_user.id, text=text, now=now)
                db.session.add(new_record)
                db.session.commit()
                
            Form.text.data = ''

        except ValueError:
            # Flash an error message for invalid input
            flash('Invalid input', category='error')

    return render_template('make_wish.html', form=Form, text=text, user=current_user)

@views.route('/wish')
def wish():
    # Get the user's data
    user = current_user
    email = user.email
    first_name = user.first_name
    txt_records = TXTRecords.query.filter_by(user_id=user.id).all()
    return render_template('wish.html', user=user, email=email, first_name=first_name, txt_records=txt_records)