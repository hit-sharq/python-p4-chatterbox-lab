from flask import Flask, request, make_response, jsonify
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

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'POST':
        message = Message(
            body=request.json['body'],
            username=request.json['username'],
        )
        db.session.add(message)
        db.session.commit()
        return jsonify(message.serialize), 201

    messages = Message.query.all()
    return jsonify([message.serialize for message in messages])


@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.get_or_404(id)

    if request.method == 'PATCH':
        data = request.get_json()
        for attr in data:
            setattr(message, attr, data[attr])
            
        db.session.add(message)
        db.session.commit()

        return make_response(message.to_dict(),200 )

    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()

        return make_response( {'deleted': True} , 200)
    
if __name__ == '__main__':
    app.run(port=5555)
