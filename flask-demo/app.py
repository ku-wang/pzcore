from flask import Flask, render_template, request, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo
# from test_link import display_case


app = Flask(__name__)
app.secret_key = 'test'
# cases = display_case.display_case()
user_info = {'user': 'kwang', 'pwd': 'password'}


@app.route("/")
def hello():
    return render_template('base.html')


@app.route("/test1")
def gt():
    return render_template('build.html')


@app.route("/study")
def study():
    test1 = [1, 2, 3, 4, 5]
    return render_template("study.html", test1=test1)


@app.route("/login", methods=['POST', 'GET'])
def login():
    user_info = {'user': 'kwang', 'pwd': 'password'}

    if request.method == 'POST':

        if {'user': request.form.get('user'), 'pwd': request.form.get('pwd')} == user_info:
            return "success"
        elif not request.form.get('user') or not request.form.get('pwd'):
            flash("login failed")
    else:
        flash('')

    return render_template("form-login.html", user_info=user_info)


# wtf 方式实现 html 表单
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    pas2 = PasswordField('Pas2', validators=[DataRequired(), EqualTo('password', 'Not equal')])
    login = SubmitField('Login')


@app.route("/for_login", methods=['POST', 'GET'])
def for_login():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        if {'user': request.form.get('username'), 'pwd': request.form.get('password')} == user_info:
            return "Login Successfully ~"
        else:
            flash("Login Failed")

    else:
        if request.method == 'POST':
            flash('参数有误 ！')
        else:
            print('ss')
    return render_template("for_login.html", login_form=login_form)


# @app.route("/")
# def get_test():
#     info = ''
#     for case in cases:
#         info = info + str(case) + '\n'
#
#     return info


if __name__ == '__main__':
    app.config["JSON_AS_ASCII"] = False
    app.run()
