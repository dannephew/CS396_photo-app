from flask import Response, request
from flask_restful import Resource
from models import Following, User, db
import json

def get_path():
    return request.host_url + 'api/posts/'

class FollowingListEndpoint(Resource):
    def __init__(self, current_user):
        self.current_user = current_user
    
    def get(self):
        # get all data where user_id (id of the follower) == current_user
        following = Following.query.filter_by(user_id=self.current_user.id).all()
        print("FOLLOWING LIST: ", following)
        following_list_of_dictionaries = [
            f.to_dict_following() for f in following
        ]
        return Response(json.dumps(following_list_of_dictionaries), mimetype="application/json", status=200)

    def post(self):
        # Your code here
        return Response(json.dumps({}), mimetype="application/json", status=201)


class FollowingDetailEndpoint(Resource):
    def __init__(self, current_user):
        self.current_user = current_user
    
    def delete(self, id):
        # Your code here
        return Response(json.dumps({}), mimetype="application/json", status=200)


def initialize_routes(api):
    api.add_resource(
        FollowingListEndpoint, 
        '/api/following', 
        '/api/following/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )
    api.add_resource(
        FollowingDetailEndpoint, 
        '/api/following/<id>', 
        '/api/following/<id>/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )
