# constructor query cloud resources form
from flask_wtf import FlaskForm
from wtforms import DateTimeField, SubmitField
from wtforms.validators import DataRequired


class IcloudForm(FlaskForm):
    StartDate = DateTimeField('Start Date', validators=[DataRequired()])
    EndDate = DateTimeField('End Date', validators=[DataRequired()])
    submit = SubmitField('query')
