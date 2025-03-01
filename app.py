from flask import Flask, render_template, request, jsonify, make_response
from flask_restful import Api, Resource
import requests
import pusher
from os import environ

app = Flask(__name__)
api = Api(app)


class Main(Resource):
    def get(self):
        data = {'pusher_key': environ["PUSHER_KEY"], 'pusher_cluster': environ["PUSHER_CLUSTER"]}
        return make_response(render_template('index.html', data=data))

class Chat(Resource):
    def post(self):
        try:
            name = request.json['name']
            message = request.json['message']
            pusher_client = pusher.Pusher(
                app_id=environ["PUSHER_APP_ID"],
                key=environ["PUSHER_KEY"],
                secret=environ["PUSHER_SECRET"],
                cluster=environ["PUSHER_CLUSTER"],
                ssl=True
            )
            data = {
                'name': name,
                'message': message
            }

            pusher_client.trigger('channel-chat', 'event-chat', data)
            return jsonify({"status": True, "message":''})
        except Exception as ex:
            ret_json = {
                'status' : False,
                "message": "Something went wrong! Please try again."
            }
            return jsonify(ret_json)


api.add_resource(Chat, '/chat')
api.add_resource(Main, '/')

if __name__=="__main__":
    app.run(debug=True)