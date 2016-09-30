from uuid import uuid1
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/retest_app.db'
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(200), primary_key=True)
    username = db.Column(db.String(80), unique=True)
    ip_address = db.Column(db.Integer)
    audience_id = db.Column(db.Integer)

    def __init__(self, username, ip_address, audience_id):
        self.id = uuid1().hex
        self.username = username
        self.ip_address = ip_address
        self.audience_id = audience_id


@app.route('/api/v1/ping')
def ping_response():
    return 'PONG'


@app.route('/api/v1/user', methods=['POST'])
def create_user():
    data = request.get_json(force=True)
    username = data['username']
    ip_address = data['ip']
    audience_id = data['audience_id']

    user_obj = User(username, ip_address, audience_id)
    db.session.add(user_obj)
    db.session.commit()
    return json.dumps({"success": True})


@app.route('/api/v1/users')
def list_users():
    all_users = User.query.all()

    user_list = []

    for user in all_users:
        user_dict = vars(user)
        del user_dict['_sa_instance_state']
        user_list.append(user_dict)

    return json.dumps({"users": user_list})

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
