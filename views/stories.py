from flask import Response
from flask_restful import Resource
from models import Story
from . import get_authorized_user_ids
import json

class StoriesListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
    
    def get(self):
        # Your code here:
        #all stories of your followers and your own
        auth_users_ids = get_authorized_user_ids(self.current_user)
        print("AUTH USERS: ", auth_users_ids)
        # bookmarks = Bookmark.query.filter_by(user_id=auth_users_ids).all()
        stories = Story.query.filter_by(user_id=self.current_user.id).all()
        
        #QUESTION: how to query multiple ids at the same time
        # stories = Story.query.add_entity.filter(user_id=auth_users_ids).all()
        
        stories = Story.query.filter(Story.user_id.in_(auth_users_ids)).all()
        
        story_list_of_dictionaries = [
            story.to_dict() for story in stories
        ]
        print("STORY_DICT: ", story_list_of_dictionaries)
        
        return Response(json.dumps(story_list_of_dictionaries), mimetype="application/json", status=200)


def initialize_routes(api):
    api.add_resource(
        StoriesListEndpoint, 
        '/api/stories', 
        '/api/stories/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )
