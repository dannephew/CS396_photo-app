from datetime import datetime
import json
from flask import Response, request
from views import can_view_post
from models import Bookmark

def secure_bookmark(endpoint_function): 
    def outer_function_with_security_checks(self):
        return endpoint_function(self)
    return outer_function_with_security_checks

# # Decorator Format:
# # https://realpython.com/primer-on-python-decorators/

# #########################################
# # Example 1: Functions can be arguments #
# #########################################
# # Say you have two greetings and you want a 
# # convenient way to use either:

# def greeting1(name):
#     return f"Hello {name}"

# def greeting2(name):
#     return f"What up {name}"

# def greet(greeter_func, name):
#     print(greeter_func(name))

# greet(greeting1, 'Bob')
# greet(greeting2, 'Maria')


# ###########################################
# # Example 2: Functions can be defined and # 
# # invoked inside of other functions.      #
# ###########################################
# def parent():
#     print("Printing from the parent() function")

#     def first_child():
#         print("Printing from the first_child() function")

#     def second_child():
#         print("Printing from the second_child() function")

#     second_child()
#     first_child()

# parent()


# ###############################
# # Example 3: Functions can be # 
# # returned and invoked later. #
# ###############################
# def parent(num):
#     def first_child():
#         return "Hi, I am Emma"

#     def second_child():
#         return "Call me Liam"

#     if num == 1:
#         return first_child
#     else:
#         return second_child

# f1 = parent(1)
# f2 = parent(2)

# print(f1)
# print(f2)
# print(f1())
# print(f2())

# ###################################
# # Example 4: Your First Decorator #
# ###################################
# '''
# * A decorator takes a function as an argument, 
#   and then wraps some functionality around it.
# * Useful for error checking and security
# '''
# def my_decorator(func):
#     def wrapper():
#         print("Something is happening before the function is called.")
#         func()
#         print("Something is happening after the function is called.")
#     return wrapper

# def say_hi():
#     print('Hi')

# def say_bye():
#     print('Bye')

# say_hi_plus_extras = my_decorator(say_hi)
# say_bye_plus_extras = my_decorator(say_bye)

# print(say_hi_plus_extras)
# print(say_bye_plus_extras)
# say_hi_plus_extras()
# say_bye_plus_extras()


# ################################
# # Example 5: "Syntactic Sugar" #
# ################################
# def my_decorator(func):
#     def wrapper():
#         print("Something is happening before the function is called.")
#         func()
#         print("Something is happening after the function is called.")
#     return wrapper

# @my_decorator
# def say_hi():
#     print('Hi')

# @my_decorator
# def say_bye():
#     print('Bye')

# print(say_hi)
# print(say_bye)
# say_hi()
# say_bye()


# ############################
# # Example 6: args & kwargs #
# ############################
# '''
# Sometimes you want to use a decorator but you don't know 
# how many arguments the inner function will have. If this
# is the case, you can use "args" and "kwargs".

# * args hold a list of any positional parameters
# * kwargs hold a dictionary of any keyword parameters.

# Using this strategy, you can apply your decorator to
# multiple functions with different function signatures. 
# '''
# def security(func):
#     def wrapper(username, *args, **kwargs):
#         if username == 'sjv':
#             # pass all of the arguments to the inner function
#             func(username, *args, **kwargs)
#         else:
#             print('Unauthorized')
#     return wrapper

# @security
# def query_users(username, limit=5, order_by='last_name'):
#     print('filter criteria:', username, limit, order_by)

# @security
# def query_posts(username, before_date=datetime.now()):
#     print('filter criteria:', username, before_date)

# print('\nquerying users table...')
# query_users('sjv', limit=10)

# print('\nquerying posts table...')
# query_posts('hjv4599')


# #######################################
# # Example 7: Flask + SQL Alchemy Demo #
# #######################################
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

#Checks for 99999 errors
def handle_db_insert_error(endpoint_function):
    
    def outer_function(self, *args, **kwargs):
        #purpose of outer function is to catch errors; it is otherwise identical to the endpoint_function
        try:
            return endpoint_function(self, *args, **kwargs)
        except:
            import sys
            db_message = str(sys.exc_info()[1]) # stores DB error message
            #print(db_message)                   # logs it to the console
            message = 'Database Insert error. Make sure your post data is valid.'
            post_data = request.get_json()
            post_data['user_id'] = self.current_user.id
            response_obj = {
                'message': message, 
                'db_message': db_message,
                'post_data': post_data 
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=404)
    return outer_function

def check_duplicate(endpoint_func):
    def security_check(self):
        body = request.get_json()
        post_id = body.get('post_id')
        #get all post_ids of user
        print("POST_ID: ", post_id)
        bookmark_id = body.get('id')
        bookmarks = Bookmark.query.filter_by(user_id=self.current_user.id).all()
        print("ALL BOOKMARKS: ", bookmarks)
        for b in bookmarks:
            print("INSIDE FOR LOOP")
            print("Bookmark: ", b.post_id)
            if b.id == bookmark_id:
                print("DUPLICATE FOUND")
                response_obj = {
                'message': 'You have already bookmarked post_id={0}'.format(post_id)
            }
                return Response(json.dumps(response_obj), mimetype="application/json", status=400)
        return endpoint_func(self)
    print("DUPLICATE NOT FOUND")
    return security_check

def secure_bookmark(endpoint_function):
    def outer_func_w_security_checks(self):
        #check for security and only execute func if security check passes
        # print('PRINT: About to issue post endpoint function.')
        body = request.get_json()
        post_id = body.get('post_id')
        # print(post_id)
        #print("Can_view_post result: ", can_view_post(post_id, self.current_user))
        if can_view_post(post_id, self.current_user):
            ######################
            print("PASSED SECURE_BOOKMARK CHECK")
            return endpoint_function(self)
        else:
            response_obj = {
                'message': 'You don\'t have access to post_id={0}'.format(post_id)
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=404)
    return outer_func_w_security_checks

def check_ownership_of_bookmark(endpoint_function):
    def outer_func_w_security_checks(self, id):
        #print(id)
        print("CHECKING OWNERSHIP")
        bookmark = Bookmark.query.get(id)
        print("Bookmark: ", bookmark)
        if bookmark.user_id == self.current_user.id:
            print("BOOKMARK INSIDE USER LIST")
            return endpoint_function(self, id)
        else:
            print("NO MATCH")
            response_obj = {
                'message': 'You did not create bookmark id={0}'.format(id)
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=404)
    return outer_func_w_security_checks

def DELETE_id_is_integer_or_400_error(endpoint_func):
    def security_check(self, id):
        print("ID: ", id)
        try: 
            #this is the bookmark id
            int(id)
            print("int(): ", int(id))
            return endpoint_func(self, id)
        except: 
            response_obj = {
                'message': '{0} is not an int'.format(id)
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=400)
    return security_check
    
    

def DELETE_check_ownership_of_bookmark(endpoint_function):
    def outer_func_w_security_checks(self, id):
        #print(id)
        print("CHECKING OWNERSHIP")
        bookmark = Bookmark.query.get(id)
        if bookmark == None: 
            print("Bookmark == None")
            response_obj = {
                'message': 'You did not create bookmark id={0}'.format(id)
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=404)
        if bookmark.user_id == self.current_user.id:
            print("BOOKMARK INSIDE USER LIST")
            return endpoint_function(self, id)
        else:
            print("NO MATCH")
            response_obj = {
                'message': 'You did not create bookmark id={0}'.format(id)
            }
            return Response(json.dumps(response_obj), mimetype="application/json", status=404)
    return outer_func_w_security_checks


#Cannot use can_view_post (bc inserting bookmark id) and also don't need to. 
# def DELETE_secure_bookmark(endpoint_function):
    
#     def outer_func_w_security_checks(self, id):
#         #check for security and only execute func if security check passes
#         # print('PRINT: About to issue post endpoint function.')
#         #print("Can_view_post result: ", can_view_post(post_id, self.current_user))
#         print("DELETE: CHECKING SECURE BOOKMARK")
#         if can_view_post(id, self.current_user):
#                 #we're using the bookmark id, so cannot use can_view_post
#             print("INSIDE IF CAN_VIEW_POST")
#             return endpoint_function(self)
#         else:
#             print("CANNOT VIEW POST")
#             response_obj = {
#                 'message': 'You don\'t have access to post_id={0}'.format(id)
#             }
#             return Response(json.dumps(response_obj), mimetype="application/json", status=404)
#     return outer_func_w_security_checks