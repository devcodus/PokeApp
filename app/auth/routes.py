from flask import Blueprint, render_template, request, redirect, url_for
from ..models import User
from .forms import UserCreationForm, LoginForm
from flask_login import login_user, logout_user, login_required

auth = Blueprint('auth', __name__, template_folder='auth_templates')


@auth.route('/signup', methods = ['GET', 'POST'])
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


            return redirect( url_for('auth.loginPage'))
    return render_template('signup.html', form = form)

@auth.route('/login', methods = ['GET', 'POST'])
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
        return redirect(url_for('homePage'))
    
    return render_template('login.html', form = form)
        
@auth.route('/logout', methods = ['GET'])
def logoutRoute():
    logout_user()

    return redirect(url_for('auth.loginPage'))