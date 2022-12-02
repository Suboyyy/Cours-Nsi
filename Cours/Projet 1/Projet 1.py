from flask import Flask, render_template, request, redirect
import sqlite3

# Pour windows : python -m flask --app "E:\NSI\term\Projet whalla gt pour\Cours\Projet 1\Projet 1.py" --debug run
# Pour Linux : export FLASK_APP="/media/suboy/USB/NSI/term/Projet whalla gt pour/Cours/Projet 1/Projet 1.py"
#              export FLASK_DEBUG=1
#              flask run

app = Flask(__name__)

# Variables
img_dir = "E:/NSI/term/Projet whalla gt pour/Cours/Projet 1/img/"
# img_dir = "/media/suboy/USB/NSI/term/Projet whalla gt pour/Cours/Projet 1/img/"
db_dir = r"E:\NSI\term\Projet whalla gt pour\Cours\Projet 1\pictures.db"


# db_dir = "/media/suboy/USB/NSI/term/Projet whalla gt pour/Cours/Projet 1/pictures.db"


@app.route("/")
def index():
    show = []
    db = sqlite3.connect(db_dir)
    cur = db.cursor()
    photos = cur.execute("SELECT name FROM photos ORDER BY ordre")
    photos = photos.fetchall()
    db.close()
    if len(photos) == 0:
        pass
    elif len(photos) < 10:
        for i in range(len(photos) - 1, 0, -1):
            show.append(photos[i][0])
    else:
        for i in range(9, 0, -1):
            show.append(photos[i][0])
    return render_template('template.html', show_pic=show, img_dir=img_dir)


@app.route("/upload_img", methods=['POST', 'GET'])
def upload_img():
    form_pseudo = request.form['pseudo']
    form_img = request.files['img']
    db = sqlite3.connect(db_dir)
    cur = db.cursor()
    try:
        cur.execute(f"INSERT INTO users (user_name, nb_pictures) VALUES ('{form_pseudo}', '0')")
        db.commit()
    except:
        pass
    user_id = cur.execute(f"SELECT user_id FROM users WHERE user_name = '{form_pseudo}'")
    user_id = user_id.fetchone()
    nb_pict = cur.execute(f"SELECT nb_pictures FROM users WHERE user_name = '{form_pseudo}'")
    nb_pict = nb_pict.fetchone()
    file_name = f"{form_pseudo}{nb_pict[0]}{file_slice(form_img.filename)}"
    cur.execute(f"INSERT INTO photos (name, user_id) VALUES ('{file_name}', {user_id[0]})")
    cur.execute(f"UPDATE users SET nb_pictures = {nb_pict[0] + 1} WHERE user_name = '{form_pseudo}'")
    db.commit()
    form_img.save(f"{img_dir}{file_name}")
    db.close()
    return redirect("/")


def file_slice(f):
    for i in range(len(f)):
        if f[i] == '.':
            return f[i:]
