#import necessary methods and set up configs
from flask import Flask, request, render_template, redirect, flash, session

from flask_debugtoolbar import DebugToolbarExtension

from surveys import satisfaction_survey

app = Flask(__name__)


app.config["SECRET_KEY"] = "not-so-secret-key"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
debug = DebugToolbarExtension(app)

#initialize a list to store the answers
# responses = []

#for the sessions it must be initialized to string 
# that matches the original variable name
#set to a "constant" so that I know it will not change
SESSION_RES = "responses"


#initialize survey to an easier to handle variable
survey = satisfaction_survey


#Get the properties from the survey class, iintialize variables that are passed to the templates
@app.route('/')
def show_survey():
    """Shows the survey with instructions 
    and redirects the user to the next page"""
    title = survey.title
    instructions = survey.instructions
    return render_template("survey-start.html", title = title, instructions = instructions)



#"""the "post" must match the form action"""
@app.route('/start')
def start_survey():
    """Takes user to the survey questions"""
    #the session needs to commence when the survey starts
    session[SESSION_RES] = []
    return redirect('/questions/0')


#initialize the route for the survey.questions property
#the question index needs to not be hard coded use the <int:> or else everythin is a string
@app.route('/questions/<int:ques_id>')
#pass the qid into the function so as the responses increase it can correspond
def show_questions(ques_id):
    """Shows user the survey questions form
    with a button to proceed to the next question if the user 
    has"""
    #intialize responses list so the prewritten logic is still valid
    responses = session.get(SESSION_RES)

    if (responses is None):
        return redirect("/")
    #the survey.questions is used to control the survey, the logic is dictated around this object
    if (len(responses) == len(survey.questions)):
    #show thank you - using the questions route render different template without hardcoding
        return redirect('/thank-you')
    
    if (len(responses) != ques_id):
    #if user tries to access the questions out of order redirect to the response len
        flash(f"Invalid access for that question: {ques_id} is out of bounds")       
        return redirect(f'/questions/{len(responses)}')    
    question = survey.questions[ques_id]
    ques_id == len(responses)
    return render_template("question.html", question=question, q_idx=ques_id)

#initialize the route for the POST request that will handle the answers and redirects
@app.route('/answer', methods=["POST"])
def handle_answers():
    """Get's user's response and appends them to the responses and controls
    the question order"""

    #initialize variable to store in the responses
    choice = request.form['response']

    #reintialize the original responses list as the session list
    responses = session[SESSION_RES]
    responses.append(choice)
    session[SESSION_RES] = responses

    #proceed to the next question after a response
    print(responses)
    if (len(responses) == len(survey.questions)):
    #show thank you - using the questions route render different template without hardcoding
        return redirect('/thank-you')
    else:
        return redirect(f'/questions/{len(responses)}')

@app.route('/thank-you')
def thank_you():
    """Show's thank you page"""
    return render_template("thank-you.html")