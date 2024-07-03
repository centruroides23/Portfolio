from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Email


class ContactForm(FlaskForm):
    name = StringField(render_kw={"class": "form-input"}, label="Name", validators=[InputRequired()])
    email = StringField(render_kw={"class": "form-input"}, label="Email", validators=[InputRequired(), Email()])
    phone = StringField(render_kw={"class": "form-input"}, label="Phone Number", validators=[InputRequired()])
    message = StringField(render_kw={"class": "form-input"}, label="Message")
    submit = SubmitField(render_kw={"class": "form-btn"}, label="Send Message")
