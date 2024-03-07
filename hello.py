from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)
moment = Moment(app)

class NameForm(FlaskForm):
    nome = StringField('Informe o seu nome:', validators=[DataRequired()])
    sobrenome = StringField('Informe o seu sobrenome:', validators=[DataRequired()])
    inst = StringField('Informe a sua instituição de ensino:', validators=[DataRequired()])
    disciplina = SelectField('Informe a sua disciplina:', choices=[('dsw', 'DSWA5'), ('dwb', 'DWBA4'), ('gest', 'Gestão de projetos')], validators=[DataRequired())
    submit = SubmitField('Submit')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    url = request.host_url
    ip = request.remote_addr
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, ip=ip, url=url, name=session.get('name'))