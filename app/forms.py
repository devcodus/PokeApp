from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, InputRequired


class PokemonCatchForm(FlaskForm):
    pokemon_name = StringField("Pokemon", validators = [DataRequired()])
    submit = SubmitField()