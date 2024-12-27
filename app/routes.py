from flask import Blueprint, render_template

# Blueprint for main routes
main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html')

