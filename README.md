# Capstone-1
ACS Capstone 1

Today's guest post comes from John Wheeler, the creator of Flask-Ask. John has been programming for two decades and has written for O'Reilly and IBM developerWorks.

This post introduces Flask-Ask, a new Python micro-framework that significantly lowers the bar for developing Alexa skills. Flask-Ask is a Flask extension that makes building voice user interfaces with the Alexa Skills Kit easy and fun. We'll learn it by building a simple game that asks you to repeat three numbers backwards. Knowing Python and Flask are not required, but some experience programming will help.

Create the Skill
To start, you'll need Python installed. If you're on a recent version of OS X or Linux, Python comes preinstalled. On Mac, you can find installation instructions here. You may also need to install pip, which can be found here. On Windows, follow these installation instructions. Once Python and pip are installed, open a terminal, and type the below command to install Flask-Ask. Note: You might need to precede it with sudo on Unix if you get permission errors. 

pip install flask-ask
Next, create a new file called memory_game.py with the code below:

import logging

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

def next_round():

    numbers = [randint(0, 9) for _ in range(3)]

    round_msg = render_template('round', numbers=numbers)

    session.attributes['numbers'] = numbers[::-1]  # reverse

    return question(round_msg)


@ask.intent("AnswerIntent", convert={'first': int, 'second': int, 'third': int})

def answer(first, second, third):

    winning_numbers = session.attributes['numbers']

    if [first, second, third] == winning_numbers:

        msg = render_template('win')

    else:

        msg = render_template('lose')

    return statement(msg)


if __name__ == '__main__':

    app.run(debug=True)
Flask-Ask lets you separate code and speech with templates. Create a file named templates.yaml in the same location as memory_game.py, and add the following to it:

welcome: Welcome to memory game. I'm going to say three numbers for you to repeat backwards. Ready?

round: Can you repeat the numbers {{ numbers|join(", ") }} backwards?

win: Good job!

lose: Sorry, that's the wrong answer.
Now, the skill is ready to run.

Run the Skill
Back in the terminal, cd into the location of your files and type:

python memory_game.py
A development server launches on http://127.0.0.1:5000/, and the skill is almost ready to configure in Amazon's Developer Portal.

Before configuration, the skill must run behind a public HTTPS server or AWS Lambda function. Setting up either would be impediments right now. Fortunately, there's ngrok to the rescue!

ngrok is a command-line program that opens a secure tunnel to localhost and exposes that tunnel behind an HTTPS endpoint. ngrok makes it so Alexa can talk to your code right away. Follow the next three steps to generate a public HTTPS endpoint to 127.0.0.1:5000.

Download the ngrok client for your operating system.
Unzip it to a location you can remember.
Open up a new terminal, cd into the location, and enter:
on Unix/Mac:

./ngrok http 5000
on Windows:

ngrok.exe http 5000
ngrok displays a status message similar to the one below. Note: The status message you see will be different.

ngrok by @inconshreveable


Tunnel Status                 online

Version                       2.0.25/2.1.1

Region                        United States (us)

Web Interface                 http://127.0.0.1:4040

Forwarding                    http://20ba2c6f.ngrok.io -> localhost:5000

Forwarding                    https://20ba2c6f.ngrok.io -> localhost:5000
Make note of the last HTTPS endpoint (in the example above, it's: https://20ba2c6f.ngrok.io). Now, let's configure the skill in Amazon's developer portal.

Configure the Skill
Make sure you're logged into your Amazon developer account, and go to your list of Alexa skills. Click the "Add a New Skill" button. Configure each section as outlined below:

Skill Information Settings
Leave the "Skill Type" set to "Custom Interaction Model"
Enter "Memory Game" (without quotes) for both the "Name" and "Invocation Name" fields.
Interaction Model Settings
Copy the JSON below into the "Intent Schema" field. Don't worry about "Custom Slot Types".

{

    "intents": [{

        "intent": "YesIntent"

    }, {

        "intent": "AnswerIntent",

        "slots": [{

            "name": "first",

            "type": "AMAZON.NUMBER"

        }, {

            "name": "second",

            "type": "AMAZON.NUMBER"

        }, {

            "name": "third",

            "type": "AMAZON.NUMBER"

        }]

    }]

}
Copy the utterances below into the "Sample Utterances" field.

YesIntent yes

YesIntent sure

                  

AnswerIntent {first} {second} {third}

AnswerIntent {first} {second} and {third}
Configuration Settings
Make sure the HTTPS radio button is selected for the "Endpoint" field.
Enter the HTTPS endpoint from ngrok into the textfield.
Don't bother with "Account Linking".
SSL Certificate Settings
It's important to choose the second radio button with the label because that's what ngrok uses.

My development endpoint is a subdomain of a domain that has a wildcard certificate from a certificate authority.

We don't need to go through any other screens. Simply make sure the information on all sections above are saved.

Test the Skill
Now, it's time to test your skill with the following interaction sequence with your Alexa-enabled device. If you need a test tool, try EchoSim.io:

You: "Alexa, start memory game"

Alexa: "Welcome to memory game. I'm going to say three numbers for you to repeat backwards. Ready?"

You: "Yes"

Alexa: "Can you repeat the numbers 9, 1, 3 backwards?"

You: "Three, one, nine."

Alexa: "Good job!"

That's it, memory_game.py exercises a lot of the Alexa Skills Kit functionality through Flask-Ask, but there's a lot more Flask-Ask can do. To see all the features, check out the Flask-Ask documentation.

Thanks to John Wheeler for another useful tool for our developers.

