from flask import Response, request
from flask_restful import Resource
from models import User
from . import get_authorized_user_ids
import json

class SuggestionsListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    def get(self):
        # Your code here:
        #get all the users that current user isn't follow 
        
        #ids that cannot be recommended: 
        
        auth_users_ids = get_authorized_user_ids(self.current_user)
        
        # all_users = User.query.all()
        # recommendations = User.query.filter_by(id=self.current_user.id)
        
        recommendations = User.query.filter(User.id.not_in(auth_users_ids)).limit(7)
        
        
        # recommendations = User.query.filter(User.id.not_in(auth_users_ids)).all()

        
        dict = [
            recommendation.to_dict() for recommendation in recommendations
        ]
        
        return Response(json.dumps(dict), mimetype="application/json", status=200)


def initialize_routes(api):
    api.add_resource(
        SuggestionsListEndpoint, 
        '/api/suggestions', 
        '/api/suggestions/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )
