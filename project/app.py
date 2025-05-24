from website import create_app, db
from website.models import Chat_log, User
import uuid
from flask_socketio import SocketIO, join_room, leave_room, emit
from flask import request, redirect, url_for, session

app = create_app()
socketio = SocketIO(app)

rooms = {}

private_rooms ={}

def find_or_create_room(sid):
    for room_id, data in rooms.items():
        if not data['active'] and len(data['users']) < 2:
            data['users'].append(sid)
            return room_id
    room_id = str(uuid.uuid4())
    rooms[room_id] = {'users': [sid], 'active' : False}
    return room_id

@socketio.on('find_game')
def on_find_game():
    sid = session['name']
    room_id = find_or_create_room(sid)

    join_room(room_id)
    print("joined room")
    show_rooms()

    if len(rooms[room_id]['users']) == 2:
        rooms[room_id]['active'] = True
        print("starting the game!")
        socketio.emit('start_game', { 'room_id': room_id }, to = room_id)

def show_rooms():
    for room_id, date in rooms.items():
        print(f"room_id: {room_id} data:")
        print(f"active: {date['active']}")
        print(f"users: {date['users']}")

def show_private_rooms():
    for room_id, date in private_rooms.items():
        print(f"room_id: {room_id} data:")
        print(f"active: {date['active']}")
        print(f"users: {date['users']}")

@socketio.on('cancel')
def cancel():
    print("cancel")
    show_rooms()
    sid = session['name']
    for room_id, data in rooms.items():
        print(f'cancel - d {sid}')  
        if sid in data['users']:
            print(f"{sid} left the room")
            leave_room(room_id)
            data['users'].remove(sid)

            if not data['users']:
                del rooms[room_id]
            else:
                pass
            print("rooms:")
            show_rooms()
            return   
        
    for room_id, data in private_rooms.items():
        print(f'cancel private - d {sid}')  
        if sid in data['users']:
            print(f"{sid} left the private room")
            leave_room(room_id)
            data['users'].remove(sid)

            if not data['users']:
                del private_rooms[room_id]
            else:
                pass
            print("private rooms:")
            show_private_rooms()
            return    

@socketio.on('challange')
def challange(room_id, message, chat_id):
    sid = session['name']
    new_log = Chat_log(chat_id = chat_id, message = message, nadawca = User.query.filter(User.name==sid).first().id, link = room_id)
    db.session.add(new_log)
    db.session.commit()
    private_rooms[room_id] = {'users': [sid], 'active' : False}

    join_room(room_id)
    print("joined private room")
    show_private_rooms()

@socketio.on('leave-challange')
def leave_challange():
    sid = session['name']

    for room_id, data in private_rooms.items():
        if sid in data['users']:
            leave_room(room_id)
            print("left private room")
            data['users'].remove(sid)

            if not data['users']:
                del rooms[room_id]
            break

@socketio.on('join')
def join(room_id):
    sid = session['name']
    if private_rooms[room_id]:
        private_rooms[room_id]['users'].append(sid)
        join_room(room_id)
        print('joined private room')
        show_private_rooms()
        if len(private_rooms[room_id]['users']) == 2:
            private_rooms[room_id]['active'] = True
            print("starting the game!")
            socketio.emit('start_game', { 'room_id': room_id }, to = room_id)






if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
    #app.run(debug=True)
