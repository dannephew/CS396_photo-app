from datetime import datetime
import json
from flask import Response, request
from views import can_view_post
from models import Post

def check_int(endpoint):
    def wrapper(self, id):
        # print("HIIIIIIII")
        try:
            # body = request.get_json()
            # post_id = body.get('id')
            # print("POST_ID: ", post_id)
            int(id)
            return endpoint(self, id)
            # print("IS INT?", int(post_id))
            # int(post_id)
            # return endpoint(self, post_id)
        except:
            response_obj = {
            'message': '{0} is not an int'.format(id)
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=400)
    return wrapper

def check_invalid_unauthorized(endpoint):
    def wrapper(self, id):
        #has to be post user owns
        # print("CURR POST")
        user_posts = Post.query.filter_by(user_id=self.current_user.id).all()
        # print("USER_POSTS: ", user_posts.)
        for post in user_posts:
            if post.user_id == self.current_user.id:            
                return endpoint(self, id)
        
        response_obj = {
            'message': 'You don\'t have access to post_id={0}'.format(id)
        }
        return Response(json.dumps(response_obj), mimetype="application/json", status=404)
    return wrapper
