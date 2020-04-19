from app import app, request, make_response, jsonify, userNote
import jwt
import datetime
import json
import flask_cors
from functools import wraps


usersData = [ userNote.UserNote(1, 'Jakub', 'Pierwsza notatka Jakuba'), userNote.UserNote(2, 'Michał', 'Pierwsza notatka Michała'), userNote.UserNote(3, 'Jakub', 'Druga notatka Jakuba'), userNote.UserNote(4, 'Paweł', 'Pierwsza notatka Pawła') ]


# Decorator that validates user Json Web Token
def validate_user_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.form.get('token')

        if not token:
            return jsonify({'message' : 'Token in invalid'}), 403

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message' : 'Token is invalid'}), 403

        return f(*args, **kwargs)

    return decorated



# User login endpoint
@app.route("/login", methods=['POST'])
def login():
    urlUsername = request.form.get('username')
    urlPassword = request.form.get('password')

    if urlUsername == 'AdminLogin' and urlPassword == 'AdminPassword':
        token = jwt.encode({'user' : urlUsername, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        
        # For testing purposes
        print(token.decode('UTF-8'))
        return jsonify({'token' : token.decode('UTF-8')})

    return jsonify({'message' : 'Could not verify!'})






# Return all notes
@app.route("/getAll", methods=['GET'])
def getAll():
    results = [obj.to_dict() for obj in usersData]
    return json.dumps({"All notes": results})


# Add new note
@app.route("/addNew", methods=['POST'])
def addNew():
    try:
        newNoteId = request.form.get('id')
        newNoteUsername = request.form.get('username')
        newNoteBody = request.form.get('note')
        usersData.append(userNote.UserNote(int(newNoteId), newNoteUsername, newNoteBody))
        return jsonify({'message' : 'Note was successfully added'})
    except:
        return jsonify({'message' : 'Unable to add a new note'})


# Detele note by Id
@app.route("/delete", methods=['DELETE'])
def delete():
    try:
        noteId = request.form.get('id')
        for i, o in enumerate(usersData):
            if o.id == int(noteId):
                del usersData[i]
                break

        return jsonify({'message' : 'Note was successfully deleted'})
    except:
        return jsonify({'message' : 'Unable to delete the note'})












