# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for
from baglerDbHelper import DbHelper, People


app = Flask(__name__)

validNames = ["Marius", "Olaug", "Finn", "Sofie", "Ole Kristian"]
validActions = ["Oppvask inn", "Oppvask ut", u"Søppel", u"Tørk overflater"]

@app.route('/', methods=['GET', 'POST'])
def namesIndex():
    """
    Function to handle page with names of the people.
    Args:
    Return: Either redirects to new page or show current name page.
    """
    if request.method == 'POST':
        name = request.form['submit']
        if name == 'Score board': # Check if score button was pushed
            return redirect(url_for("scoreBoard"))
        return redirect(url_for('actions', name=name))
    elif request.method == 'GET':
        return render_template("names.html")

@app.route('/<name>', methods=['GET', 'POST'])
def actions(name = None):
    """
    Page to show what actions one can do.
    Args: 
        name: Name of person to do action.
    Returns: Web page of actions or redirects to score board.
    """
    if name in validNames:

        if request.method == 'POST':
            action = request.form['submit']





            return redirect(url_for('scoreBoard', action=action, name=name))
        else:
            return render_template("actions.html")
    else:
        return "Wrong name"

@app.route('/score') #Show score without having to do an action.
@app.route('/<name>/<action>', methods=['GET', 'POST'])
def scoreBoard(action = None, name = None):
    """
    Shows update scoreboard.
    Args: 
        action: Action done by person
        name: Name of person
    Returns: Web page of score board.
    """
    # Load data
    dbhelper = DbHelper()
    dbhelper.loadCredentials()
    people = []
    people = dbhelper.loadData()

    if action in validActions and name in validNames:
        # Load data
        dbhelper = DbHelper()
        dbhelper.loadCredentials()
        people = []
        people = dbhelper.loadData()

        nameNotInDb = False
        indexPerson = 0

        for person in people:
            if name == person.name:
                nameNotInDb = True
                break
            indexPerson += 1

        if not nameNotInDb:
            people.append(People(len(people)-1, name, 1))
        else:
            people[indexPerson].score += 1
        dbhelper.saveData(people)

        return renderScoreBoard(people)

    elif action is None and name is None:
        return renderScoreBoard(people)
    else:
        return "Wrong url"

def renderScoreBoard(people):
    while(len(people) < len(validNames)):
        people.append(People(len(people)-1, None, None))

    return render_template("scoreboard.html",
           name1 = people[0].name, score1 = people[0].score,
           name2 = people[1].name, score2 = people[1].score,
           name3 = people[2].name, score3 = people[2].score,
           name4 = people[3].name, score4 = people[3].score,
           name5 = people[4].name, score5 = people[4].score)




if __name__ == "__main__":
    app.run(debug=True)
