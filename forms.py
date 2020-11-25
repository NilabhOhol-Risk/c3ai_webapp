from flask_wtf import FlaskForm
from datetime import date, timedelta
from wtforms import (Form
,FloatField
, validators
,SelectField)
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email
from wtforms_components import DateRange

STATE_CHOICES = [('Alabama'), ('Alaska'), ('Arizona')
                , ('Arkansas'), ('California'), ('Colorado')
                , ('Connecticut'), ('Delaware'),('District of Columbia'), ('Florida')
                , ('Georgia'),('Hawaii'), ('Idaho')
                , ('Illinois'), ('Indiana'), ('Iowa')
                , ('Kansas'), ('Kentucky'), ('Louisiana')
                , ('Maine'), ('Maryland'),('Massachusetts')
                , ('Michigan'), ('Minnesota'), ('Mississippi')
                , ('Missouri'), ('Montana'), ('Nebraska'), ('Nevada')
                , ('New Hampshire'), ('New Jersey'), ('New Mexico')
                , ('New York'), ('North Carolina'), ('North Dakota')
                , ('Ohio'), ('Oklahoma'), ('Oregon'), ('Pennsylvania'),('Puerto Rico')
                , ('Rhode Island'), ('South Carolina'),('South Dakota')
                , ('Tennessee'), ('Texas'), ('Utah'), ('Vermont')
                , ('Virginia'), ('Washington'), ('West Virginia')
                , ('Wisconsin'), ('Wyoming')
                ]

testing_kits_key = [0, 0.25, 0.50, 0.75 , 1, 1.5, 2, 3, 4, 5, 6, 7, 8, 9, 10]
n_95_masks_key = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 125, 150, 175, 200,300,400]
num_days = [10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]
vaccines_key = [0, 0.25, 0.50, 0.75 , 1, 1.5, 2, 3, 4, 5, 6, 7, 8, 9, 10]
key_adult_fraction= [0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50]


class InputForm(Form):
    state = SelectField('State', choices=STATE_CHOICES)
    counties = SelectField('County', choices=[])
    num_fatalities_7 = FloatField('COVID-19 fatalities during time period',validators=[validators.InputRequired()])
    normalcy_choices = SelectField('Normalcy Level', choices=[])
    # normalcy = FloatField('Desired Normalcy',validators=[validators.InputRequired()])
    num_kits = SelectField('# Testing kits per 1000 per day:',choices=testing_kits_key)
    num_masks = SelectField('# PPE per 1000 per day:',choices=n_95_masks_key)
    num_vaccines = SelectField('Vaccine availability:',choices=vaccines_key)
    num_days = SelectField('# Days in time period',choices=num_days)
    num_cases_3_weeks = FloatField('# Cases in last 3 weeks ',validators=[validators.InputRequired()])
    l1_risk_key_adults_fraction = SelectField('Low-risk key adults not living in crowding (L1)',choices=key_adult_fraction)
    h1_risk_key_adults_fraction = SelectField('High-risk key adults not living in crowding (H1)',choices=key_adult_fraction)
    h2_risk_key_adults_fraction = SelectField('High-risk key adults living in crowding (H2)',choices=key_adult_fraction)

class output_form(Form):
    normalcy_choices = SelectField('Normalcy Level', choices=[])
    
class DateForm(Form):
    date_field_cases_start = DateField('Enter Start Date',default=date.today()- timedelta(days = 1))
    date_field_cases_end = DateField('Enter End Date',default=date.today()- timedelta(days = 1))
    num_cases_3_weeks_date = DateField('Enter Date',default=date.today()- timedelta(days = 1))

    def validate_on_submit(self):
        result = super(DateForm, self).validate()
        if (self.date_field_cases_start.data>self.date_field_cases_end.data):
            return False
        else:
            return result
