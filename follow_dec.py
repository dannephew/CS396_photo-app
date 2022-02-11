from datetime import datetime
import json
from flask import Response, request
from views import can_view_post
from models import Following, User

def check_duplicate(endpoint):
    def wrapper(self):
        body = request.get_json()
        #person we want to follow: 
        follower_id = body.get('user_id')
        #get list of people we already follow
        curr_following = Following.query.filter_by(user_id=self.current_user.id).all()
        
        for f in curr_following:
            if f.following_id == follower_id:
                response_obj = {
                'message': 'You already follow follwer_id={0}'.format(follower_id)
            }
                return Response(json.dumps(response_obj), mimetype="application/json", status=400)
        return endpoint(self)
    return wrapper
    #if person we want to follow is already part of the people we following

def check_int(endpoint):
    def wrapper(self):
        try: 
            body = request.get_json()
            #person we want to follow: 
            follower_id = body.get('user_id')
            int(follower_id)
            return endpoint(self)
        except: 
            return Response(
                json.dumps({'message': '{0} must be an integer.'.format(follower_id)}), 
                mimetype="application/json", 
                status=400
            )
    return wrapper

def check_invalid_user(endpoint):
    def wrapper(self):
        print("CHECKING INVALID USER")
        body = request.get_json()
        #person we want to follow: 
        follower_id = body.get('user_id')
        
        #get list of all ids of people they could possibly follow
        users_list = User.query.all()
        print("users_list: ", users_list)
        
        for user in users_list:
            if user.id == follower_id:
                return endpoint(self)
        return Response(
            json.dumps({'message': '{0} is not a user.'.format(follower_id)}), 
            mimetype="application/json", 
            status=404
        )
    return wrapper