from datetime import datetime
import json
from flask import Response, request
from views import can_view_post
from models import Comment

def id_is_integer_or_400_error(func):
    def wrapper(self, *args, **kwargs):
        try:
            body = request.get_json()
            # print(body)
            id = body.get('post_id')
            int(id)
            return func(self, *args, **kwargs)
        except:
            return Response(
                json.dumps({'message': '{0} must be an integer.'.format(id)}), 
                mimetype="application/json", 
                status=400
            )
    return wrapper


def secure_comment(endpoint_function):
    def outer_func_w_security_checks(self):
        #check for security and only execute func if security check passes
        # print('PRINT: About to issue post endpoint function.')
        body = request.get_json()
        post_id = body.get('post_id')
        # print(post_id)
        #print("Can_view_post result: ", can_view_post(post_id, self.current_user))
        if can_view_post(post_id, self.current_user):
            # print("PASSED SECURE_BOOKMARK CHECK")
            return endpoint_function(self)
        else:
            response_obj = {
                'message': 'You don\'t have access to post_id={0}'.format(post_id)
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=404)
    return outer_func_w_security_checks

def missing_text(endpoint):
    def wrapper(self, *args, **kwargs):
        body = request.get_json()
        text = body.get('text')
        if text != None: 
            return endpoint(self, *args, **kwargs)
        else: 
            response_obj = {
                'message': 'No text for this comment.'
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=400)
    return wrapper

def DELETE_check_int(endpoint):
    def wrapper(self, id):
        try: 
            int(id)
            return endpoint(self, id)
        except:
            return Response(
                json.dumps({'message': '{0} must be an integer.'.format(id)}), 
                mimetype="application/json", 
                status=400
            )
    return wrapper
            
def DELETE_check_invalid_unauthorized(endpoint):
    def wrapper(self, id):
        print("CHECK INVALID UNAHTORIZED")
            #this is the comment id
            #user must have created comment 
            #find all of user's comments, then see if there is a match 
            #OR find the owner of the commend, and see if it matches current user
        # Bookmark.query.filter_by(user_id=self.current_user.id).all()
        
        # comment = Comment.query.filter_by(id = id).all()
        # print("COMMENT: ", comment)
        # print("COMMENT.USER_ID: ", comment.user_id)
        
        # if comment.user_id == self.current_user.id:
        #     # print("PASSED SECURE_BOOKMARK CHECK")
        #     return endpoint(self, id)
        
        user_comments = Comment.query.filter_by(user_id = self.current_user.id).all()
        print("CURR COMMENT ID: ", id)
        print("USER COMMENTS: ", user_comments)
        for c in user_comments:
            print("CHECKING COMMENT ID: ", c.id)
            if int(c.id) == int(id):
                print("found a match")
                return endpoint(self, id)
            print("not a match")
        else:
            response_obj = {
                'message': 'Either the post doesn\'t exist, or you don\'t have access to post_id={0}'.format(id)
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=404)
    return wrapper