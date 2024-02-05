from flask import Flask, render_template, request, redirect, url_for, session
from flask import send_file
from io import StringIO

app = Flask(__name__)
app.secret_key = "your_secret_key"
user = {'username': 'admin', 'password': 'admin'\
        ,'first_name': 'f_name', 'last_name': 'l_name', 'email': 'a@gmail.com'}
users = {}


@app.route('/')
def index():
  return render_template('index.html')


multiple_users = []


@app.route('/register', methods=['POST'])
def register():
  username = request.form['username']
  password = request.form['password']
  first_name = request.form['first_name']
  last_name = request.form['last_name']
  email = request.form['email']
  user = {
      'name': username,
      'password': password,
      'first_name': first_name,
      'last_name': last_name,
      'email': email
  }
  multiple_users.append(user)
  return redirect(url_for('display_info', **user))


@app.route('/display_info')
def display_info():
  username = request.args.get('name')
  email = request.args.get('email')
  first_name = request.args.get('first_name')
  last_name = request.args.get('last_name')

  user_info = {
      'name': username,
      'email': email,
      'first_name': first_name,
      'last_name': last_name
  }
  return render_template('display_info.html', user_info=user_info)


@app.route('/login', methods=['POST'])
def login():
  count = 0
  username = request.form['username']
  password = request.form['password']
  for i in range(0, len(multiple_users)):
    if (multiple_users[i]['name']) == username and (
        multiple_users[i]['password']) == password:
      user = {
          'name': multiple_users[i]['name'],
          'password': multiple_users[i]['password'],
          'first_name': multiple_users[i]['first_name'],
          'last_name': multiple_users[i]['last_name'],
          'email': multiple_users[i]['email']
      }
      count = count + 1
      return redirect(url_for('display_info', **user))
  if (count == 0):
    return render_template('invalid_details.html')


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080)
  # app.run(debug=True)
