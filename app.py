from flask import Flask, session, render_template, request, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = 'rock,paper,scissors'

choices = ['rock', 'paper', 'scissors']

def get_winner(user, computer):
    if user == computer:
        return "Draw!"
    
    if (
        (user == 'rock' and computer == 'scissors') or
        (user == 'paper' and computer == 'rock') or
        (user == 'scissors' and computer == 'paper')
    ):
        return "User wins!"  # Capitalized for consistent checking
    return "Computer wins!"

@app.route('/')
def home():
    # Initialize score session tracker keys
    if "wins" not in session:
        session["wins"] = 0
        session["losses"] = 0
        session["draw"] = 0  # 🌟 Key is "draw" (singular)

    return render_template('index.html')  # Flask passes session to templates automatically

@app.route('/play', methods=['POST'])
def play():
    user_choice = request.form['choice']
    computer_choice = random.choice(choices)
    winner = get_winner(user_choice, computer_choice)

    # 🌟 Fixed case-matching and matched session keys perfectly:
    if winner == "User wins!":
        session["wins"] += 1
    elif winner == "Computer wins!":
        session["losses"] += 1
    else:
        session["draw"] += 1  # 🌟 Changed from "draws" to match home() initialization
        
    return render_template(
        'results.html', 
        user_choice=user_choice,  # Fixed variable name to match template usage
        computer_choice=computer_choice, 
        winner=winner
    )

@app.route('/reset')
def reset():
    session["wins"] = 0
    session["losses"] = 0
    session["draw"] = 0
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)