from app import app
from flask import render_template, request, redirect, url_for, Flask, jsonify
import requests
from .forms import UserCreationForm, LoginForm
from .models import User, Pokemon
from flask_login import login_user, logout_user, current_user
from sqlalchemy import select 

@app.route('/')
def homePage():
    greeting = "Welcome to my Pokemon app!"

    

    return render_template('index.html', greeting = greeting)

@app.route('/contact')
def contactPage():
    return render_template('contact.html')

 
@app.route('/signup', methods = ['GET', 'POST'])
def signUpPage():
    form = UserCreationForm()
    print(request.method+' test')

    if request.method == 'POST':
        print(form.validate_on_submit())
        if form.validate_on_submit(): ## this form isn't being validated for some reason ... how to check?
            print("success!")
        #     username = form.username.data
        #     email = form.email.data
        #     password = form.password.data

        #     print(username, email, password)


            username = form.username.data
            email = form.email.data
            password = form.password.data

            print(username, email, password)

            #add user to the DB

            user = User(username, email, password)
            print(user)

            # db.session.add(user)
            # db.session.commit()
            user.saveToDB()


            return redirect( url_for('loginPage'))
    return render_template('signup.html', form = form)

@app.route('/login', methods = ['GET', 'POST'])
def loginPage():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate():

            username = form.username.data
            password = form.password.data

            user = User.query.filter_by(username = username).first()
            if user:
                #if user exists, check if pw's match
                print(user)

                if user.password == password:
                    login_user(user)
                    print('successfully logged in!')

                else:
                    print('wrong password')
            else:
                print("user doesn't exist")
    
    return render_template('login.html', form = form)
        
@app.route('/logout', methods = ['GET'])
def logoutRoute():
    logout_user()

    return redirect(url_for('loginPage'))
        
@app.route('/pokeform', methods=['GET', 'POST'])
def pokePicker():
    return render_template('pokeform.html')

@app.route('/pokedata', methods=['GET', 'POST'])
def pokedata():
    print(request.form['pokemon_name'])
    if request.form != "":
        name = request.form["pokemon_name"].lower()
        print(name)
        url = f"https://pokeapi.co/api/v2/pokemon/{name}"
        my_pkmn = {}
        response = requests.get(url)
    else:
        return jsonify({"error": "Pokemon not found."}), 404

    if response.status_code == 200 and name:
        pokemon = response.json()
        my_pkmn['Name'] = pokemon['name'].title()   
        my_pkmn['abilityName'] = pokemon['abilities'][0]['ability']['name'].title()
        my_pkmn['baseXP'] = pokemon['base_experience']
        my_pkmn['shiny'] = pokemon["sprites"]['front_shiny']
        my_pkmn['attack'] = pokemon['stats'][1]['base_stat']
        my_pkmn['hp'] = pokemon['stats'][0]['base_stat']
        my_pkmn['defense'] = pokemon['stats'][2]['base_stat']

        pokename = my_pkmn['Name']
        ability_name = my_pkmn['abilityName']
        base_xp = my_pkmn['baseXP']
        shiny = my_pkmn['shiny']
        attack = my_pkmn['attack']
        hp = my_pkmn['hp']
        defense = my_pkmn['defense']

        pokemon = Pokemon(pokename, ability_name, base_xp, shiny, attack, hp, defense, current_user.id ) ## USER_ID ?
        print(pokemon.name)
        pokemon.saveToDB()

        print(my_pkmn)
        return render_template('pokedisplay.html', my_pkmn = my_pkmn)
    else:
        return jsonify({"error": "Pokemon not found."}), 404

    
   
@app.route('/my-pokemon', methods = ['GET', 'POST'])
def myPokemon():
    # my_pokemon = Pokemon.query.all()
    my_pokemon = Pokemon.query.filter(Pokemon.user_id == current_user.id).all()
    

    return render_template('pokedex.html', my_pokemon = my_pokemon)
