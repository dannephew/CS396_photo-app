from tabnanny import check
from flask import Response
from flask_restful import Resource
from models import LikePost, db
import json
from . import can_view_post
from likepost_dec import check_duplicate, check_int, check_invalid_unauthorized, DEL_check_int, DEL_check_invalid_unauthorized


class PostLikesListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    
    @check_int
    @check_invalid_unauthorized
    @check_duplicate
    def post(self, post_id):        
        #user_id, post_id
        # try: 
            # int(post_id)
        like = LikePost(self.current_user.id, post_id)
        db.session.add(like)
        db.session.commit()        
        return Response(json.dumps(like.to_dict()), mimetype="application/json", status=201)

        

class PostLikesDetailEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    @DEL_check_int
    @DEL_check_invalid_unauthorized
    def delete(self, post_id, id):
        LikePost.query.filter_by(id=id).delete()
        db.session.commit()
        serialized_data = {
            'message': 'Like {0} successfully deleted.'.format(id)
        }
        return Response(json.dumps(serialized_data), mimetype="application/json", status=200)



def initialize_routes(api):
    api.add_resource(
        PostLikesListEndpoint, 
        '/api/posts/<post_id>/likes', 
        '/api/posts/<post_id>/likes/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )

    api.add_resource(
        PostLikesDetailEndpoint, 
        '/api/posts/<post_id>/likes/<id>', 
        '/api/posts/<post_id>/likes/<id>/',
        resource_class_kwargs={'current_user': api.app.current_user}
    )
