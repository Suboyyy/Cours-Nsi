from flask import Flask, render_template

# python -m flask --app "E:\NSI\term\Projet whalla gt pour\Cours\Exercices.py" --debug run

app = Flask(__name__)


@app.route("/template")
def template():
    return render_template("template1.html")


@app.route("/page_variable/<meteo>")
def page_variable(meteo):
    return f"<p>La météo actuel est : {meteo}</p>"