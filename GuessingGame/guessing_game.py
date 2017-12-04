import logging

from random import randint

from flask import Flask, render_template

from flask_ask import Ask, statement, question, session


app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)
global answer


@ask.launch
def new_game():
    global answer
    welcome_msg = render_template('welcome')
    answer = randNum()
    return question(welcome_msg)

@ask.intent("GameIntent")
def ready():
    game_msg = render_template('game')
    return question(game_msg)



@ask.intent("GuessIntent", convert={'one': int})
def guess(one):
    global answer

    flag = False #

    result = check(answer,one)
    if (answer == one):
        msg = render_template('win')
        print("Good job, You guessed my number in {} guesses!")
        flag = True
        return statement("Good job!")

    if (answer < one):
        msg = render_template('high')
        return question("Your guess is too High.")

    if (answer > one):
        msg = render_template('low')
        print ("Your guess is too low.")
        return question("Your guess is too Low.")


@ask.session_ended
def session_ended():
    return "{}", 200
    #
    # if (flag == False):
    #     msg = render_template('lose')
    #     print("Nope. The number I was thinking of was {}")
    #     return statement("Nope. The number I was thinking of was {}")


def check(answer,number):
    if (answer == number):
        return 0
    if (answer > number) :
        return -1
    if (answer < number) :
        return 1

def randNum():
    number = randint(1, 20)
    return number

@ask.intent('AMAZON.HelpIntent')
def help():
    help_text = render_template('help')
    return question(help_text)


@ask.intent('AMAZON.StopIntent')
def stop():
    bye_text = render_template('bye')
    return statement(bye_text)


@ask.intent('AMAZON.CancelIntent')
def cancel():
    bye_text = render_template('bye')
    return statement(bye_text)


if __name__ == '__main__':

    app.run(debug=True)
