from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask import redirect, Flask, render_template, request, url_for, make_response
from data import db_session
from data.profils import Profile
from data.search_history import History
from data.bookmark import Bookmarks
import requests
from werkzeug.security import generate_password_hash, check_password_hash

db_session.global_init("db/users.db")

app = Flask(__name__)

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class Buttons(FlaskForm):
    submit = SubmitField("Закладки")
    submit1 = SubmitField("История")
    submit2 = SubmitField("Ссылка")


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        if check_profils(form.username.data, form.password.data):
            return redirect('/success', success(login))
        else:
            return render_template('login.html',
                                   message="Неправильный логин или пароль",
                                   form=form)
    return render_template("login.html", form=form)
    # global message
    # message = " "
    # if request.method == 'GET':
    #     return f"""<!DOCTYPE html>
    # <!-- Coding By CodingNepal - youtube.com/codingnepal -->
    # <html lang="en" dir="ltr">
    #   <head>
    #     <meta charset="utf-8">
    #     <title>Animated Login Form | CodingNepal</title>
    #     <link rel="stylesheet" href="{url_for('static', filename='css/2.css')}">
    #   </head>
    #   <body>
    #     <div class="center">
    #       <h1>Login</h1>
    #       <form method="post">
    #         <div class="txt_field">
    #           <input type="text" name="text" required >
    #           <span></span>
    #           <label>Username</label>
    #         </div>
    #         <div class="txt_field">
    #           <input type="password" name="password" required >
    #           <span></span>
    #           <label>Password</label>
    #         </div>
    #         <div class="pass">Forgot Password?</div>
    #         <input type="submit" value="Login">
    #         <div>{url_for(message)}</div>
    #       </form>
    #     </div>
    #
    #   </body>
    # </html>"""
    # elif request.method == 'POST':
    #     if request.form["text"] == "tt" and request.form["password"]:
    #         return redirect('/success')
    #     else:
    #         global message
    #         message = "Неправильный логин или пароль"


@app.route('/success', methods=['GET', 'POST'])
def success(login):
    form = Buttons()
    if form.is_submitted():
        if form.submit.data:
            return redirect("/bookmarks", bookmarks(login))
        if form.submit1.data:
            print(2)
        if form.submit2.data:
            return redirect("https://t.me/Project3_3_bot")
    # # if form.validate_on_submit():
    # #     return redirect("https://t.me/Project3_3_bot")
    return render_template('button.html', form=form)


@app.route("/cookie_test")
def cookie_test():
    visits_count = int(request.cookies.get("visits_count", 0))
    if visits_count:
        res = make_response(
            f"Вы пришли на эту страницу {visits_count + 1} раз")
        res.set_cookie("visits_count", str(visits_count + 1),
                       max_age=60 * 60 * 24 * 365 * 2)
    else:
        res = make_response(
            "Вы пришли на эту страницу в первый раз за последние 2 года")
        res.set_cookie("visits_count", '1',
                       max_age=60 * 60 * 24 * 365 * 2)
    return visits_count


@app.route('/unsuccess', methods=['GET', 'POST'])
def unsuccess():
    return render_template('404.html')


def check_profils(login, password):
    db_sess = db_session.create_session()
    if login in [prof.login for prof in db_sess.query(Profile).all()]:
        if check_password_hash(db_sess.query(Profile).filter(Profile.login == login).first().hashed_password, password):
            return True
        return False
    return False


@app.route("/bookmarks", methods=['GET', 'POST'])
def bookmarks(login):
    print(return_bookmarks(login))
    return f"{return_bookmarks(login)}"


def return_bookmarks(login):
    db_sess = db_session.create_session()
    user = db_sess.query(Profile).filter(Profile.login == login).first()
    chat_id = int(user.chat_id)
    return [prof.reguest for prof in db_sess.query(Bookmarks).filter(Bookmarks.chat_id == chat_id).all()]




if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
