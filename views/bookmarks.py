from flask import Response, request
from flask_restful import Resource
from models import Bookmark, db
import json

from my_decorators import id_is_integer_or_400_error, secure_bookmark, handle_db_insert_error, check_ownership_of_bookmark
from . import can_view_post

def get_path():
    return request.host_url + 'api/bookmarks/'

class BookmarksListEndpoint(Resource):
    #Lists all bookmarks
    #Create a new bookmark
    def __init__(self, current_user):
        self.current_user = current_user
    
    def get(self):
        #Goal is to only show the bookmarks associate with the current user
        #Use SQL Alchemy to execute query using the Bookmark model (from models folder)
        #When we return this list, it's serialized using JSON
            #Turn into list of dictionaries using JSON
        # Your code here
        bookmarks = Bookmark.query.filter_by(user_id=self.current_user.id).all()
        #print(bookmarks)
        
        # convert list of Bookmark model to a list of dictionaries
        bookmark_list_of_dictionaries = [
            bookmark.to_dict() for bookmark in bookmarks
        ]
        return Response(json.dumps(bookmark_list_of_dictionaries), mimetype="application/json", status=200)


    @id_is_integer_or_400_error
    @secure_bookmark
    #     #catches errors so we can only bookmark posts of people we're following or our own
    # @handle_db_insert_error
    #     #catches database error: if the post has already been bookmarked or not a valid post number
    def post(self):
        #get post_id from request body
        #check user is authorized to bookmark post 
        #check post_id exists and is valid 
        #if true: insert to database
        #return new bookmarked post (and bookmark id) to user as part of the response
        
        #data user sent: 
        body = request.get_json()
        print(body)
        post_id = body.get('post_id')
        #to create bookmark, need to pass it a user_id and post_id
        
        try: 
            bookmark = Bookmark(self.current_user.id, post_id)
            
            #commit the new record to the database
            db.session.add(bookmark)
            db.session.commit()
            
        except:
            import sys
            db_message = str(sys.exc_info()[1]) # stores DB error message
            print(db_message)                   # logs it to the console
            message = 'Database Insert error. Make sure your post data is valid.'
            post_data = request.get_json() #show user what they posted
            post_data['user_id'] = self.current_user.id #what the current user id is
            response_obj = {
                'message': message, 
                'db_message': db_message,
                'post_data': post_data #return everything 
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=400)
        
        return Response(json.dumps(bookmark.to_dict()), mimetype="application/json", status=201)

class BookmarkDetailEndpoint(Resource):
    #PATCH (updating), GET (individual bookmarks), DELETE individual bookmarks
    #CREATE a new bookmark
    def __init__(self, current_user):
        self.current_user = current_user
    
    @check_ownership_of_bookmark
    def delete(self, id):
        # Your code here
        # bookmark = Bookmark.query.get(id)
        Bookmark.query.filter_by(id=id).delete()
        db.session.commit()
        serialized_data = {
            'message': 'Bookmark {0} successfully deleted.'.format(id)
        }
        return Response(json.dumps(serialized_data), mimetype="application/json", status=200)



def initialize_routes(api):
    api.add_resource(
        BookmarksListEndpoint, 
        '/api/bookmarks', 
        '/api/bookmarks/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )

    api.add_resource(
        BookmarkDetailEndpoint, 
        '/api/bookmarks/<id>', 
        '/api/bookmarks/<id>',
        resource_class_kwargs={'current_user': api.app.current_user}
    )
