from random import random

from flask import Flask, redirect, request, session, url_for
from flask import render_template

app = Flask(__name__)
choices = ['rock', 'paper', 'scissors']

def get_winner(user, computer):
    if user == computer:
        return "Draw!"
    
    if (
      (user == 'rock' and computer == 'scissors') or
      (user == 'paper' and computer == 'rock') or
      (user == 'scissors' and computer == 'paper')
    ):   
        return "user wins!"
    return "computer wins!"

@app.route('/')
def home():
    if "wins" not in session:

      session["wins"] = 0
      session["losses"] = 0
      session["draws"] = 0
    
    return render_template('index.html',session=session)
@app.route('/play',methods=['POST'])
def play():
    user_choice = request.form['choice']
    computer_choice = random.choice(choices)
    winner = get_winner(user_choice, computer_choice)

    if winner == "user wins!":
        session["wins"] += 1
    elif winner == "computer wins!":
        session["losses"] += 1
    else:
        session["draws"] += 1
    return render_template('results.html',
                           user_choice=user_choice,
                           computer_choice=computer_choice,
                           winner=winner,
                           session=session)

@app.route('/reset', methods=['POST'])
def reset():
    session["wins"] = 0
    session["losses"] = 0
    session["draws"] = 0
    return redirect(url_for('home'))
if __name__ == '__main__':
    app.run(debug=True)