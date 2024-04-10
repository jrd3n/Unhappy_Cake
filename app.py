from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
import datetime

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.config['SECRET_KEY'] = 'mysecret'  # In production, use a secure and unique secret key

# This is a dummy user store for the sake of demonstration. In real life, you'd use a database.
users = {'gooduser': 
                    {'password': 'BSI120Kitemark',
                    'next_login_attempt' : None} ,
        'baduser': 
                    {'password': 'cookie',
                    'next_login_attempt' : None}}
                    
class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(username):
    if username not in users:
        return
    user = User()
    user.id = username
    return user

@app.route('/')
@login_required
def main():
    return render_template('main.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user_data = users.get(username)

        print(user_data)

        # If the user does not exist
        if user_data is None:
            #return "Invalid username", 401
            return render_template('login.html', message=f"User {username} not found!")

        # If the password matches
        if user_data['password'] == password:
            # Reset the next_login_attempt
            user_data['next_login_attempt'] = None
            
            # Here's where you would handle successful authentication
            user = User()
            user.id = username
            login_user(user)
            return redirect(url_for('main'))

        render_template('login.html', message='Login not successful!')

    message = request.args.get('message')  # Getting the message from URL parameter

    return render_template('login.html', message=message)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/pw_reset', methods=['GET', 'POST'])
def pw_reset():

    if request.method == 'POST':
        username = request.form['username']

        user_data = users.get(username)
        
        if user_data is not None:

            return redirect(url_for('login', message="reset email sent to user!"))  # Redirecting to a hypothetical 'login' route

        else:

            return render_template('password_reset.html', message=f"{username} does not exist")

    return render_template('password_reset.html', message= "")

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True, port=5000)