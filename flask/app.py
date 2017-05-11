# encoding: utf-8
from flask import Flask, request, Response
import json
import time

app = Flask(__name__, static_url_path='', static_folder='public')
app.add_url_rule('/', 'root', lambda: app.send_static_file('index.html'))


@app.route('/', methods=['GET', 'POST'])
def home():
  return '<h1>Home</h1>'


@app.route('/signin', methods=['GET'])
def signin_form():
  return '''<form action="/signin" method="post">
    <p><input name="username"></p>
    <p><input name="password" type="password"></p>
    <p><button type="submit">Sign In</button></p>
    </form>'''


@app.route('/signin', methods=['POST'])
def signin():
  if request.form['username'] == 'admin' and request.form['password'] == 'password':
    return '<h3>Hello admin</h3>'
  return '<h3>Bad Username or password</h3>'


@app.route('/api/comments', methods=['GET', 'POST'])
def comments_handler():
  with open('comments.json', 'r') as f:
    comments = json.loads(f.read())

  if request.method == 'POST':
    new_comment = request.form.to_dict()
    new_comment['id'] = int(time.time() * 1000)
    comments.append(new_comment)

    with open('comments.json', 'w') as f:
      f.write(json.dumps(comments, indent=4, separators=(',', ': ')))

  return Response(
    json.dumps(comments),
    mimetype='application/json',
    headers={
      'Cache-Control': 'no-cache',
      'Access-Control-Allow-Origin': '*'
    }
  )


if __name__ == '__main__':
  app.run(port=3000, debug=True)
