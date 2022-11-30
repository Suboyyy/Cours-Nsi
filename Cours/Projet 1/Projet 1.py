from flask import Flask, render_template, request, redirect

# python -m flask --app "E:\NSI\term\Projet whalla gt pour\Cours\Projet 1\Projet 1.py" --debug run

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('template.html')


@app.route("/upload_img", methods=['POST', 'GET'])
def upload_img():
    form = request.form
    form_img = request.files['img']
    form_img.save(f"Cours/Projet 1/img/{form['pseudo']}{file_slice(form_img.filename)}")
    return redirect("/")


def file_slice(f):
    for i in range(len(f)):
        if f[i] == '.':
            return f[i:]
