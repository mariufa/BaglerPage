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
        return pushedAButton()
    elif request.method == 'GET':
        return render_template("names.html")


def pushedAButton():
    name = request.form['submit']
    if name == 'Score board':
        return redirect(url_for("scoreBoard"))
    else:
        return redirect(url_for('actions', name=name))


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
        return validUrl(name)
    else:
        return "Wrong name"


def validUrl(name):
    if request.method == 'POST':
        action = request.form['submit']
        return redirect(url_for('scoreBoard', action=action, name=name))
    else:
        return render_template("actions.html")


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
    if nameAndActionChosen(action, name) or scoreboardButtonPushed(action, name):
        return validScoreBoardUrl(action, name)
    else:
        return "Wrong url"


def validScoreBoardUrl(action, name):
    people = []
    people = loadPeopleFromDataBase()
    if nameAndActionChosen(action, name):
        people = updatePeople(name, people)
        writeToDatabase(people)
    return render_template("scoreboard.html", people=people)


def updatePeople(name, people):
    indexPerson = findPerson(name, people)
    if indexPerson >= 0:
        people[indexPerson].score += 1
    else:
        score = 1
        idTag = len(people) -1
        people.append(Person(idTag, name, score))
    return people

def findPerson(name, people):
    indexPerson = -1
    for i in range(len(people)):
        if name == people[i].name:
            indexPerson = i
            break
    return indexPerson


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
