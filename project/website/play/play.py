from flask import Blueprint, render_template

play = Blueprint(
    "play",
    __name__,
    template_folder="templates",
    static_folder="static"
)

@play.route('/game<room>')
def game(room):
    return render_template('base_play.html', room = room)