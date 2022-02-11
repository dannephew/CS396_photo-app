from flask import Response, request
from flask_restful import Resource
from models import Post, User, db
from . import can_view_post, get_authorized_user_ids
import json
from sqlalchemy import and_
from post_dec import check_int, check_invalid_unauthorized, DEL_check_int, DEL_check_invalid_unauthorized

def get_path():
    return request.host_url + 'api/posts/'


class PostListEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user

    def get(self):
        # TODO: 
        # 1. No security implemented; 
        # 2. limit is hard coded (versus coming from the query parameter)
        # 3. No error checking
        
        #get all posts of user
        limit = request.args.get('limit')
        print("FIRST LIMIT: ", limit)
        if limit:
            try:
                limit = int(limit)
            except:
                return Response(json.dumps({'message': 'Limit must be an integer between 1 and 50'}), mimetype="application/json", status=400)
            if limit > 50 or limit < 1:
                return Response(json.dumps({'message': 'Limit must be an integer between 1 and 50'}), mimetype="application/json", status=400)
        else:
            limit = 20
        print("LIMIT: ", limit)
        posts = Post.query.filter_by(user_id=self.current_user.id).order_by(Post.pub_date.desc()).limit(limit).all()

        # posts = posts.limit(3)
        print("POSTS: ", posts)
        #print(bookmarks)
        
        # convert list of Bookmark model to a list of dictionaries
        posts_list_of_dictionaries = [
            post.to_dict() for post in posts
        ]
        
        # data = Post.query.limit(20).all()

        # data = [
        #     item.to_dict() for item in data
        # ]
        return Response(json.dumps(posts_list_of_dictionaries), mimetype="application/json", status=200)


    def post(self):
        body = request.get_json()
        image_url = body.get('image_url')
        caption = body.get('caption')
        alt_text = body.get('alt_text')
        print(image_url)
        print(caption, alt_text)
        user_id = self.current_user.id # id of the user who is logged in
        if not image_url:
            return Response(json.dumps({'message': 'No image'}), mimetype="application/json", status=400)
        # create post:
        post = Post(image_url, user_id, caption, alt_text)
        db.session.add(post)
        db.session.commit()
        return Response(json.dumps(post.to_dict()), mimetype="application/json", status=201)
        
class PostDetailEndpoint(Resource):

    def __init__(self, current_user):
        self.current_user = current_user
        
    @check_int
    @check_invalid_unauthorized
    def patch(self, id):
        post = Post.query.get(id)

        # a user can only edit their own post:
        if not post or post.user_id != self.current_user.id:
            return Response(json.dumps({'message': 'Post does not exist'}), mimetype="application/json", status=404)
       

        body = request.get_json()
        post.image_url = body.get('image_url') or post.image_url
        post.caption = body.get('caption') or post.caption
        post.alt_text = body.get('alt_text') or post.alt_text
        
        # commit changes:
        db.session.commit()        
        return Response(json.dumps(post.to_dict()), mimetype="application/json", status=200)
    
    @DEL_check_int
    @DEL_check_invalid_unauthorized
    def delete(self, id):

        # a user can only delete their own post:
        post = Post.query.get(id)
        if not post or post.user_id != self.current_user.id:
            return Response(json.dumps({'message': 'Post does not exist'}), mimetype="application/json", status=404)
       

        Post.query.filter_by(id=id).delete()
        db.session.commit()
        serialized_data = {
            'message': 'Post {0} successfully deleted.'.format(id)
        }
        return Response(json.dumps(serialized_data), mimetype="application/json", status=200)

    @DEL_check_int
    @DEL_check_invalid_unauthorized
    def get(self, id):
        post = Post.query.get(id)

        # if the user is not allowed to see the post or if the post does not exist, return 404:
        if not post or not can_view_post(post.id, self.current_user):
            return Response(json.dumps({'message': 'Post does not exist'}), mimetype="application/json", status=404)
        
        return Response(json.dumps(post.to_dict()), mimetype="application/json", status=200)

def initialize_routes(api):
    #PostListEndpoint: GET, POST
    api.add_resource(
        PostListEndpoint, 
        '/api/posts', '/api/posts/', 
        resource_class_kwargs={'current_user': api.app.current_user}
    )

    #Detail: Post (single), PATCH, DELETE
    api.add_resource(
        PostDetailEndpoint, 
        '/api/posts/<id>', '/api/posts/<id>/',
        resource_class_kwargs={'current_user': api.app.current_user}
    )


    # I set up the system with Professor Sarah Van Wart during office hours, which took a while. Postgres was not being recognized as a valid role, 
    # so I had to run the following command: ALTER DATABASE postgres OWNER TO postgres;