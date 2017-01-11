import pyrebase
import os
from flask import Flask, jsonify, request

app = Flask('wheretoeat')
config = {
    "apiKey": "AIzaSyBIjbqPZ2ZZ-KJ0T-0UNmydz6fzojhpVDI",
    "authDomain": "wheretoeat-f02f3.firebaseapp.com",
    "databaseURL": "https://wheretoeat-f02f3.firebaseio.com",
    "storageBucket": "wheretoeat-f02f3.appspot.com",
    "messagingSenderId": "414041625018"
}
firebase = pyrebase.initialize_app(config)


@app.route("/places/createplaces", methods=["POST"])
def create_places():
    auth = firebase.auth()
    user = auth.sign_in_with_email_and_password('wheretoeat@example.com', '123456')
    dict_places = request.get_json()
    for place in dict_places:
        firebase.database().child("places").push(place, user['idToken'])
    return 'ok'


@app.route("/places", methods=["GET"])
def get_places():
    auth = firebase.auth()
    user = auth.sign_in_with_email_and_password('wheretoeat@example.com', '123456')
    places = firebase.database().child("places").get(user['idToken'])
    return jsonify(places.val())


@app.route("/places/<id_place>/vote/<user>", methods=["POST"])
def post_vote(id_place, user):
    auth = firebase.auth()
    auth_user = auth.sign_in_with_email_and_password('wheretoeat@example.com', '123456')
    token = auth_user['idToken']
    users = firebase.database().child("places").child(id_place).child("votes_users").get(token).val()
    users.append(user)
    firebase.database().child("places").child(id_place).child("votes_users").set(users, auth_user['idToken'])
    return 'ok'


@app.route("/places/placeofday", methods=["GET"])
def place_day():
    auth = firebase.auth()
    auth_user = auth.sign_in_with_email_and_password('wheretoeat@example.com', '123456')
    token = auth_user['idToken']
    places = firebase.database().child("places").get(token)
    count = 0
    chosen_place = None
    for place in places.each():
        try:
            length_users = len(place.val()["votes_users"])
            if length_users > count:
                count = length_users
                chosen_place = place.val()
        except KeyError as e:
            pass
    return jsonify(chosen_place)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
