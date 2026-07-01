from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Optional

class TripForm(FlaskForm):
    destination = StringField("Destination", validators=[DataRequired(), Length(min=2, max=50)])
    start_date = DateField("Departure date", validators=[DataRequired()])
    end_date = DateField("Return date", validators=[DataRequired()])
    budget = IntegerField("Total Budget (USD)", default=1, validators=[DataRequired(), NumberRange(min=1)])
    travelers = IntegerField("Travelers", default=1, validators=[DataRequired(), NumberRange(min=1)])
    style = StringField("Travel style", validators=[Optional()])
    interests = StringField("Interests", validators=[Optional()])
    submit = SubmitField("Build my 3 plans")