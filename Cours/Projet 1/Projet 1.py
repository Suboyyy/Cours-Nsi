from flask import Flask, render_template, request, redirect
import sqlite3

# Pour windows : python -m flask --app "E:\NSI\term\Projet whalla gt pour\Cours\Projet 1\Projet 1.py" --debug run
# Pour Linux : export FLASK_APP="/media/suboy/USB/NSI/term/Projet whalla gt pour/Cours/Projet 1/Projet 1.py"
#              export FLASK_DEBUG=1
#              flask run

app = Flask(__name__)


# Variables
img_dir = "Cours/Projet 1/img/"
db_dir = "Cours/Projet 1/pictures.db"


@app.route("/")
def index():
    return render_template('template.html')


@app.route("/upload_img", methods=['POST', 'GET'])
def upload_img():
    form_pseudo = request.form['pseudo']
    form_img = request.files['img']
    db = sqlite3.connect(db_dir)
    cur = db.cursor()
    res = cur.execute("SELECT user_name FROM users")
    db.commit()
    res = res.fetchall()
    if form_pseudo in res:
        user_id = cur.execute(f'SELECT user_id FROM users WHERE user_name = {form_pseudo}')
        user_id = user_id.fetchone()
        nb_pict = cur.execute(f'SELECT nb_pictures FROM users WHERE user_name = {form_pseudo}')
        nb_pict = nb_pict.fetchone()
        db.commit()
        file_name = f"{form_pseudo}{nb_pict[0]}{file_slice(form_img.filename)}"
        cur.execute(f"INSERT INTO photos (name, user_id) VALUES ({file_name}, {user_id[0]})")
        cur.execute(f"UPDATE users SET nb_pictures = {nb_pict + 1} WHERE user_name = {form_pseudo}")
        db.commit()
    else:
        cur.execute(f"INSERT INTO users (user_name, nb_pictures) VALUES ({form_pseudo}, '1')")
        db.commit()
        nb_pict = 1
        file_name = f"{form_pseudo}{nb_pict}{file_slice(form_img.filename)}"
        user_id = cur.execute(f'SELECT user_id FROM users WHERE user_name = {form_pseudo}')
        db.commit()
        user_id = user_id.fetchone()
        cur.execute(f"INSERT INTO photos (name, user_id) VALUES ({file_name}, {user_id[0]})")
        file_name = ""
    form_img.save(f"{img_dir}{file_name}")
    return redirect("/")


def file_slice(f):
    for i in range(len(f)):
        if f[i] == '.':
            return f[i:]
