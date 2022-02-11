from tabnanny import check
from flask import Response, request
from flask_restful import Resource
from models import Following, User, db
import json
from follow_dec import check_duplicate, check_int, check_invalid_user
# from my_decorators import id_is_integer_or_400_error, handle_db_insert_error

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

    # @id_is_integer_or_400_error
    @check_duplicate
    @check_int
    @check_invalid_user
    def post(self):
        #Follow someone new
        body = request.get_json()
        follower_id = body.get('user_id')
        
        follow = Following(self.current_user.id, follower_id)
        # print("COMMENT: ", comment)
            #commit the new record to the database
        db.session.add(follow)
        db.session.commit()
        return Response(json.dumps(follow.to_dict_following()), mimetype="application/json", status=201)


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
