from app import app
from flask import render_template, request, redirect, url_for, Flask, jsonify
import requests

@app.route('/')
def homePage():
    greeting = "Welcome to my Pokemon app!"
    return render_template('index.html', greeting = greeting)

@app.route('/contact')
def contactPage():
    return{
        'yo': [
            'shoha', 'brandt'
        ]
    }
@app.route('/test')
def test():
    return {
        'hello':'world'
    }

@app.route('/test2')
def test2():
    return {
        'hello':'world2'
    }

@app.route('/pokeform', methods=['GET', 'POST'])
def pokePicker():
    return render_template('pokeform.html')

@app.route('/pokedata', methods=['GET', 'POST'])
def pokedata():
    name = request.form["pokemon_name"]
    url = f"https://pokeapi.co/api/v2/pokemon/{name}"
    my_pkmn = {}
    response = requests.get(url)
    if response.status_code == 200:
        pokemon = response.json()
        my_pkmn['Name'] = pokemon['name'].title()
        my_pkmn['abilityName'] = pokemon['abilities'][0]['ability']['name'].title()
        my_pkmn['baseXP'] = pokemon['base_experience']
        my_pkmn['shiny'] = pokemon["sprites"]['front_shiny']
        my_pkmn['attack'] = pokemon['stats'][1]['base_stat']
        my_pkmn['hp'] = pokemon['stats'][0]['base_stat']
        my_pkmn['defense'] = pokemon['stats'][2]['base_stat']

        print(my_pkmn)
        return render_template('pokedisplay.html', my_pkmn = my_pkmn)
    else:
        return jsonify({"error": "Pokemon not found."}), 404
    
