from app import app

@app.route('/')
def homePage():
    return {
        'test': 'hi'
    }

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
