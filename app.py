import praw
import prawcore
from flask import Flask, render_template, abort, request

reddit = praw.Reddit('sortReddit')
app = Flask(__name__)

@app.route('/')
def home():
    text = '<a href="%s">Authenticate with reddit</a>'
    return text % make_authorization_url()

def make_authorization_url():
    # Generate a random string for the state parameter
    # Save it for use later to prevent xsrf attacks
    from uuid import uuid4
    state = str(uuid4())
    save_created_state(state)
    url = reddit.auth.url(['identity', 'read'], state, 'temporary')
    return url

@app.route('/reddit_callback')
def reddit_callback():
    error = request.args.get('error', '')
    if error:
        return "Error: " + error
    state = request.args.get('state', '')
    if not is_valid_state(state):
        abort(403)
    code = request.args.get('code')
    access_token = get_token(code)
    return "Your reddit username is: %s" % get_username(access_token)

def save_created_state(state):
    pass

def is_valid_state(state):
    return True

def get_token(code):
    return reddit.auth.authorize(code)

def get_username(access_token):
    return reddit.user.me()

if __name__ == '__main__':
    app.run(debug=True)
