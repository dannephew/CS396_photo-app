from flask import Response, request
from flask_restful import Resource
from . import can_view_post
import json
from models import db, Comment, Post
from my_decorators import id_is_integer_or_400_error, handle_db_insert_error
from comment_decorators import secure_comment, missing_text

class CommentListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    @id_is_integer_or_400_error
    @handle_db_insert_error
    @missing_text
    @secure_comment
    def post(self):
        # Your code here
        body = request.get_json()
        print("BODY: \n", body)
        text = body.get('text')
        # user_id = body.get('user_id')
        post_id = body.get('post_id')
        # print("USER_ID: ", user_id)
        print("text: ", text)
        print("POST_ID: ", post_id)
        print("user_id: ", self.current_user.id)
        #text, user_id, post_id
        
        comment = Comment(text, self.current_user.id, post_id)
        # print("COMMENT: ", comment)
            #commit the new record to the database
        db.session.add(comment)
        db.session.commit()
        return Response(json.dumps(comment.to_dict()), mimetype="application/json", status=201)
        
class CommentDetailEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
  
    def delete(self, id):
        # Your code here
        return Response(json.dumps({}), mimetype="application/json", status=200)


def initialize_routes(api):
    api.add_resource(
        CommentListEndpoint, 
        '/api/comments', 
        '/api/comments/',
        resource_class_kwargs={'current_user': api.app.current_user}

    )
    api.add_resource(
        CommentDetailEndpoint, 
        '/api/comments/<id>', 
        '/api/comments/<id>',
        resource_class_kwargs={'current_user': api.app.current_user}
    )
