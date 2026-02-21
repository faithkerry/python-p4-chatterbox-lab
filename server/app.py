from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)
db.init_app(app)

# ==========================
# ROUTES
# ==========================

# GET /messages - all messages ordered by created_at
@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return jsonify([m.to_dict() for m in messages]), 200

# POST /messages - create a new message
@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    if not data or not data.get('body') or not data.get('username'):
        return jsonify({'error': 'body and username are required'}), 400

    msg = Message(body=data['body'], username=data['username'])
    db.session.add(msg)
    db.session.commit()
    return jsonify(msg.to_dict()), 201

# GET /messages/<id> - single message by ID
@app.route('/messages/<int:id>', methods=['GET'])
def get_message_by_id(id):
    msg = Message.query.get_or_404(id)
    return jsonify(msg.to_dict()), 200

# PATCH /messages/<id> - update message body
@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    data = request.get_json()
    msg = Message.query.get_or_404(id)
    if 'body' in data:
        msg.body = data['body']
    db.session.commit()
    return jsonify(msg.to_dict()), 200

# DELETE /messages/<id> - delete a message
@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    msg = Message.query.get_or_404(id)
    db.session.delete(msg)
    db.session.commit()
    return jsonify({'message': 'Message deleted'}), 200

# ==========================
# RUN SERVER
# ==========================
if __name__ == '__main__':
    app.run(port=5555, debug=True)