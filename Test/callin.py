from flask import Flask, render_template, request
from gem import generate

app = Flask(__name__)
responses=generate()
# Variable containing your HTML code
@app.route('/')
def home():
    # Pass the 'responses' variable to the 'home.html' template
    return render_template('home.html', content=responses)

