from flask import Response, request
from flask_restful import Resource
from models import User
from . import get_authorized_user_ids
import json

class SuggestionsListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    def get(self):
        pass
        # Your code here:
        #get all the users that current user isn't follow 
        
        #ids that cannot be recommended: 
        
        # auth_users_ids = get_authorized_user_ids(self.current_user)
        
        # all_users = User.query.all()
        
        # for user in all_users:
        #     for auth_user in auth_users_ids:
        #         #check if there's a match
        #         #if there is not a match, then you can add it to a list people you can recommend
        # return Response(json.dumps([]), mimetype="application/json", status=200)


def initialize_routes(api):
    api.add_resource(
        SuggestionsListEndpoint, 
        '/api/suggestions', 
        '/api/suggestions/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )
