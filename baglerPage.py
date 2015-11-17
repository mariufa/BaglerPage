# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for
from baglerDbHelper import DbHelper, Person


app = Flask(__name__)

validNames = ["Marius", "Olaug", "Finn", "Sofie", "Ole Kristian"]
validActions = ["Oppvask inn", "Oppvask ut", u"Søppel", u"Tørk overflater"]

@app.route('/', methods=['GET', 'POST'])
def namesIndex():
    """
    Function to handle page with names of the people.

    Return:
        Either redirects to new page or show current name page.
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
    Returns:
        Web page of actions or redirects to score board.
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
    Returns:
        Web page of score board.
    """
    people = []
    people = loadPeopleFromDataBase()

    if nameAndActionChosen(action, name):
        # name may not be stored in database
        nameNotInDb = False
        indexPerson = 0

        # Search for name in database
        for person in people:
            if name == person.name:
                nameNotInDb = True
                break
            indexPerson += 1

        if not nameNotInDb:
            people.append(Person(len(people) - 1, name, 1))
        else:
            people[indexPerson].score += 1
        writeToDatabase(people)

        return render_template("scoreboard.html", people=people)

    elif scoreboardButtonPushed(action, name):
        return render_template("scoreboard.html", people=people)
    else:
        return "Wrong url"

def loadPeopleFromDataBase():
    """
    Loads people from database.

    Returns:
        List of people.
    """
    dbhelper = DbHelper()
    dbhelper.loadCredentials()
    return dbhelper.loadData()

def nameAndActionChosen(action, name):
    """
    Checks if chosen action and name is valid.

    Args:
        action: Action chosen by user. String.
        name: Name of the user. String.

    Returns:
        Boolean value.
    """
    return action in validActions and name in validNames

def writeToDatabase(people):
    """
    Writes list of people to database.

    Args:
        people: List of people to be written.
    """
    dbhelper = DbHelper()
    dbhelper.loadCredentials()
    dbhelper.saveData(people)

def scoreboardButtonPushed(action, name):
    """
    Check if no name and action is chosen.

    Args:
        action: Action chosen. String.
        name: Name of user. String.

    Returns:
        Boolean value.
    """
    return action is None and name is None


if __name__ == "__main__":
    app.run(debug=True)
    #app.run(host='0.0.0.0')
