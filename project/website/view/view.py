from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import current_user, login_required
from ..models import User, Game, Chat, Chat_log
from .. import db

view = Blueprint(
    "view",
    __name__,
    template_folder="templates",
    static_folder = "static",
    static_url_path="/view/static"
)



@view.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('view.stats', user_id = current_user.id))
    else:
        return redirect(url_for('auth.login'))

def find_chat_id(user_id):
    chat = Chat.query.filter(
        (
        (Chat.user1_id == current_user.id) &
        (Chat.user2_id == user_id)
        ) |
        (
        (Chat.user2_id == current_user.id) &
        (Chat.user1_id == user_id)
        )
    ).first()

    if chat is None:
        new_chat = Chat(user1_id = current_user.id, user2_id = user_id)
        db.session.add(new_chat)
        db.session.commit()
        chat = new_chat

    return chat.id


@view.route('/search')
@login_required
def search():
    query = request.args.get('q') + "%"
    
    if query:
        shows = User.query.filter((User.name != current_user.name) & (User.name.like(query))).all()
    else:
        shows = []
    user_list = [{"id": u.id, "name": u.name, "elo": u.elo, "chat": find_chat_id(u.id)} for u in shows]
    return jsonify(user_list)

@view.route('/stats<user_id>')
@login_required
def stats(user_id):
    games = Game.query.filter(
        (user_id == Game.white_id) or
        (user_id == Game.black_id)
    ).order_by(Game.date.desc()).all()

    return render_template('stats.html', games=games, c_user = current_user)

@view.route('/chat<chat_id>')
@login_required
def chat(chat_id):
    chat = Chat.query.filter(chat_id == Chat.id).first()
    if chat:
        messages = Chat_log.query.filter(chat.id == Chat_log.chat_id).all()
    else:
        flash("Coś poszło nie tak", category='error')
        return redirect(url_for('view.home'))

    return render_template('chat.html', c_user = current_user, chat = chat, messages = messages)