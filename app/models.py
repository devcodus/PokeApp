from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    wins = db.Column(db.Integer, nullable=True)
    losses = db.Column(db.Integer, nullable=True)
    pokemon = db.relationship("Pokemon", backref="owner", lazy=True)
    pokedex = db.relationship("Pokedex", back_populates="user")


    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable = False)
    ability_name = db.Column(db.String(45), nullable = False)
    base_xp = db.Column(db.Integer, nullable = False)
    shiny = db.Column(db.String(200), nullable = False)
    attack = db.Column(db.Integer, nullable = False)
    hp = db.Column(db.Integer, nullable = False)
    defense = db.Column(db.Integer, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    pokedex = db.relationship('Pokedex', back_populates="pokemon")

    def __init__(self, name, ability_name, base_xp, shiny, attack, hp, defense, user_id):
        self.name = name
        self.ability_name = ability_name
        self.base_xp = base_xp
        self.shiny = shiny
        self.attack = attack
        self.hp = hp
        self.defense = defense
        self.user_id = user_id
        # self.pokedex = pokedex ## IS THIS CORRECT?

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

    def deleteFromDB(self):
        db.session.delete(self)
        db.session.commit()



class Pokedex(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    pokemon_id = db.Column(db.Integer, db.ForeignKey('pokemon.id'), nullable = False)
    user = db.relationship("User", back_populates="pokedex")
    pokemon = db.relationship("Pokemon", back_populates="pokedex")

   
    def __init__(self, user_id, pokemon_id):
        self.user_id = user_id
        self.pokemon_id = pokemon_id

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

    def deleteFromDB(self):
        db.session.delete(self)
        db.session.commit()

# Pokemon.pokedexes = relationship("Pokedex", back_populates="pokemon")
# User.pokedexes = relationship("Pokedex", back_populates="user")

## update flask db models in order to grap {{pokemon.pokedex_id}}