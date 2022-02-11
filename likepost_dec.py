from datetime import datetime
import json
from flask import Response, request
from views import can_view_post
from models import LikePost

def check_duplicate(endpoint):
    def wrapper(self, post_id):
        liked_posts = LikePost.query.filter_by(user_id=self.current_user.id).all()
        # print("LIKED POSTS: ", liked_posts)
        #check that we haven't liked this post before
        for post in liked_posts:
            if int(post.post_id) == int(post_id):
                response_obj = {
                'message': 'You already follow follwer_id={0}'.format(post_id)
                }
                return Response(json.dumps(response_obj), mimetype="application/json", status=400)
        
        return endpoint(self, post_id)
    return wrapper


def check_int(endpoint):
    def wrapper(self, post_id):
        # print("HIIIIIIII")
        try:
            # body = request.get_json()
            # post_id = body.get('post_id')
            print("POST_ID: ", post_id)
            int(post_id)
            return endpoint(self, post_id)
            # print("IS INT?", int(post_id))
            # int(post_id)
            # return endpoint(self, post_id)
        except:
            response_obj = {
            'message': '{0} is not an int'.format(post_id)
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=400)
    return wrapper

def check_invalid_unauthorized(endpoint):
    def wrapper(self, post_id):
        #make sure user has access to it by checking they're following the user who is posting
        if can_view_post(post_id, self.current_user):
            return endpoint(self, post_id)
        else: 
            response_obj = {
                'message': 'You don\'t have access to post_id={0}'.format(post_id)
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=404)
    return wrapper