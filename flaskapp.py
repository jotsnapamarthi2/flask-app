from flask import Flask, render_template, request, redirect, url_for, session
from flask import send_file
from io import StringIO
from flask import Flask, send_from_directory

app = Flask(_name_)
app.secret_key = "your_secret_key"
user = {'username': 'admin', 'password': 'admin'\
        ,'first_name': 'f_name', 'last_name': 'l_name', 'email': 'a@gmail.com', 'file_content': 'sample', 'file_length': 0}
users = {}


@app.route('/')
def index():
  return render_template('index.html')


multiple_users = []


app.config['UPLOAD_FOLDER'] = 'uploads'  # Create a folder named 'uploads' in your project directory
    
@app.route('/download')
def download_file():
    file_content = request.args.get('file_content')
    filename = "new_file.txt"
    with open(filename, 'w') as file:
        file.write(file_content)
    return send_file(filename, as_attachment=True)


@app.route('/register', methods=['POST'])
def register():
  username = request.form['username']
  password = request.form['password']
  first_name = request.form['first_name']
  last_name = request.form['last_name']
  email = request.form['email']
  file = request.files['file']
  file_contents = file.read().decode('utf-8')
  words = file_contents.split()
  num_words = len(words)
  no_of_words_in_file = num_words
  user = {
      'name': username,
      'password': password,
      'first_name': first_name,
      'last_name': last_name,
      'email': email,
      'file_content': file_contents,
      'file_length': no_of_words_in_file
  }
  multiple_users.append(user)
  return redirect(url_for('display_info', **user))


@app.route('/display_info')
def display_info():
  username = request.args.get('name')
  email = request.args.get('email')
  first_name = request.args.get('first_name')
  last_name = request.args.get('last_name')
  file_content = request.args.get('file_content')
  no_of_words_in_file = request.args.get('file_length')
  user_info = {
      'name': username,
      'email': email,
      'first_name': first_name,
      'last_name': last_name,
      'file_content' : file_content,
      'file_length': no_of_words_in_file
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
          'email': multiple_users[i]['email'],
          'file_content': multiple_users[i]['file_content'],
          'file_length': multiple_users[i]['file_length']
      }
      count = count + 1
      return redirect(url_for('display_info', **user))
  if (count == 0):
    return render_template('invalid_details.html')


if _name_ == '_main_':
  app.run(host='0.0.0.0', port=8080)
  # app.run(debug=True)
