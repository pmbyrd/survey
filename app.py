#import necessary methods and set up configs
from flask import Flask, request, render_template, redirect, flash, url_for

from flask_debugtoolbar import DebugToolbarExtension

from surveys import satisfaction_survey

app = Flask(__name__)


app.config["SECRET_KEY"] = "not-so-secret-key"
# app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
debug = DebugToolbarExtension(app)

#intialize a list to store the answers
responses = []
#intialize survey to an easier to handle variable
survey = satisfaction_survey

@app.route('/')
def show_survey():
    """Shows the survey with instructions 
    and redirects the user to the next page"""
    title = survey.title
    instructions = survey.instructions

    return render_template("start.html", title = title, instructions = instructions)


@app.route('/survey', methods=['POST'])
def start_survey():
    """Starts the survey with the first question"""
    return redirect("/questions/0")


@app.route('/questions/<int:q_id>')
def show_question(q_id):
    """Shows each question in the survey based of the 
    its index in the questions attribute"""
    question = survey.questions[q_id]
    return render_template("questions.html", question=question, q_idx=q_id)


@app.route('/answers', methods=["POST"])
def get_answers():
    """Stores the users responses to the db"""
    #a fake db
    choice = request.form["answer"]
    responses.append(choice)
    #to control the redirects they must match a number, after at question is 
    # go to the next question if all questions go to thank you
  
    return redirect(f'/questions/{len(responses)}')


@app.route('/thank_you')
def show_thank_you():
    """Shows the thank you page at the end of the survey"""
    return render_template("thank_you.html")


# #get the user input

# #redirect to the next page

# #flash message if not in order

# #How to make it automatically preview the next question without hardcoding
# #the questions are in a list so they can be accessed by its index
# #need to not redirect immediately
# #use len() to control the redirects and order of how questions can be handled
# #I am essentially handling a click need to use conditional logic to control the order