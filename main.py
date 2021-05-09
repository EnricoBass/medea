from flask import Flask, render_template, redirect, url_for, flash, abort, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
import os


class HomepageForm(FlaskForm):
    name = StringField("Inserisci quì il tuo nome", validators=[DataRequired()])
    submit = SubmitField("Inizia il gioco")


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') #'8BYkEfBA6O6donzWlSihBXox7C0sKR6c'
Bootstrap(app)

# This part is required to log in a user so that I can link information to that profile.
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///medea_quiz.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    ranking = db.Column(db.Integer)

db.create_all()

@app.route('/', methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated:
        logout_user()
    form = HomepageForm()
    if form.validate_on_submit():
        if User.query.filter_by(name=form.name.data).first():
            flash("Mi dispiace, questo nome utente è già stato preso. Provane un altro.")
            return redirect(url_for('home'))
        new_user = User(
            name=form.name.data,
            score=0,
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('question1'))
    return render_template('index.html', form=form)


@app.route('/question1', methods=['GET', 'POST'])
@login_required
def question1():
    if request.args.get('check_answer'):
        player_answer = request.args.get("answer")
        if player_answer == 'True':
            answer = False
        else:
            answer = True
            answer_to_update = User.query.get(current_user.id)
            answer_to_update.score = 25
            db.session.commit()
        return render_template('question1.html', answer_given=True, answer=answer)
    return render_template('question1.html')


@app.route('/question2', methods=['GET', 'POST'])
@login_required
def question2():
    if request.args.get('check_answer'):
        player_answer = request.args.get("answer")
        if player_answer == 'True':
            answer = True
            answer_to_update = User.query.get(current_user.id)
            answer_to_update.score = answer_to_update.score + 25
            db.session.commit()
        else:
            answer = False
        return render_template('question2.html', answer_given=True, answer=answer)
    return render_template('question2.html')


@app.route('/question3', methods=['GET', 'POST'])
@login_required
def question3():
    if request.args.get('check_answer'):
        player_answer = request.args.get("answer")
        if player_answer != 'True':
            answer = True
            answer_to_update = User.query.get(current_user.id)
            answer_to_update.score = answer_to_update.score + 25
            db.session.commit()
        else:
            answer = False
        return render_template('question3.html', answer_given=True, answer=answer)
    return render_template('question3.html')


@app.route('/question4', methods=['GET', 'POST'])
@login_required
def question4():
    if request.args.get('check_answer'):
        player_answer = request.args.get("answer")
        if player_answer == 'True':
            answer = True
            answer_to_update = User.query.get(current_user.id)
            answer_to_update.score = answer_to_update.score + 25
            db.session.commit()
        else:
            answer = False
        return render_template('question4.html', answer_given=True, answer=answer)
    return render_template('question4.html')


@app.route('/question5', methods=['GET', 'POST'])
@login_required
def question5():
    if request.args.get('check_answer'):
        player_answer = request.args.get("answer")
        if player_answer == 'True':
            answer = True
            answer_to_update = User.query.get(current_user.id)
            answer_to_update.score = answer_to_update.score + 25
            db.session.commit()
        else:
            answer = False
        return render_template('question5.html', answer_given=True, answer=answer)
    return render_template('question5.html')


@app.route('/ranking', methods=['GET', 'POST'])
def ranking():
    all_users = User.query.order_by(User.score).all()
    if all_users != None:
        all_users.reverse()
        for i in range(len(all_users)):
            all_users[i].ranking = i+1
        db.session.commit()
        logout_user()
        return render_template('ranking.html', users=all_users)
    return render_template('ranking.html', users=None)


@app.route('/delete')
def delete():
    answer = request.args.get('answer')
    if answer == 'True':
        all_users = db.session.query(User).all()
        for user in all_users:
            db.session.delete(user)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('delete.html')

if __name__ == "__main__":
    app.run(debug=True)
