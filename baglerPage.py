from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)

validNames = ["Marius", "Olaug", "Finn", "Sofie", "Ole Kristian"]
validActions = ["Oppvask inn", "Oppvask ut", "Soeppel", "Toerk overflater"]

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
            action = request.form['sumbit']
            return redirect(url_for("scoreBoard", action=action, name=name))
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
    if action in validActions and name in validNames:
        pass
    else:
        return "Wrong url"

    return render_template("scoreboard.html") 


if __name__ == "__main__":
    app.run(debug=True)
