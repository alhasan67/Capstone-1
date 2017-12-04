import logging
import random

from random import randint

from flask import Flask, render_template

from flask_ask import Ask, statement, question, session


app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)



@ask.launch
def new_game():

    welcome_msg = render_template('welcome')
    return question(welcome_msg)

@ask.intent("YesIntent")
def dice_roll():
    roll_message = "Your number is: " + str(random.randint(1,6))
    print ("Your number is: " + str(random.randint(1,6)))
    return question(roll_message)



if __name__ == '__main__':

    app.run(debug=True)
