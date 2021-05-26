#
# Simple API gateway in Python
#
# Inspired by <https://github.com/vishnuvardhan-kumar/loadbalancer.py>
#

import os
import sys
import json
import http.client
import logging.config
import itertools

import bottle
from bottle import get, route, request, response, auth_basic
from requests.auth import HTTPBasicAuth
import requests.exceptions

import requests
from collections import deque


# Allow JSON values to be loaded from app.config[key]
#
def json_config(key):
    value = app.config[key]
    return json.loads(value)


# Set up app and logging
#
app = bottle.default_app()
app.config.load_config('./etc/gateway.ini')


logging.config.fileConfig(app.config['logging.config'])


# If you want to see traffic being sent from and received by calls to
# the Requests library, add the following to etc/gateway.ini:
#
#   [logging]
#   requests = true
#
if json_config('logging.requests'):
    http.client.HTTPConnection.debuglevel = 1

    requests_log = logging.getLogger('requests.packages.urllib3')
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True

    logging.debug('Requests logging enabled')


# Return errors in JSON
#
# Adapted from <https://stackoverflow.com/a/39818780>
#
def json_error_handler(res):
    if res.content_type == 'application/json':
        return res.body
    res.content_type = 'application/json'
    if res.body == 'Unknown Error.':
        res.body = bottle.HTTP_CODES[res.status_code]
    return bottle.json_dumps({'error': res.body})


app.default_error_handler = json_error_handler


# Disable warnings produced by Bottle 0.12.19 when reloader=True
#
# See
#  <https://docs.python.org/3/library/warnings.html#overriding-the-default-filter>
#
if not sys.warnoptions:
    import warnings
    warnings.simplefilter('ignore', ResourceWarning)


#adapted from https://stackoverflow.com/questions/52461587/basic-auth-authentication-in-bottle/52461939#52461939
#authentication part
@route('/users/<username>/<password>/')
def is_authenticated_user(username, password):
    #using Mockroblog, the API does not return true or false directly.
    #instead, the resources array will contain a record
    payload = {'username': username, 'password': password}
    logging.debug(f"payload: {payload}")
    upstream_server = get_upstream_servers('/users/')
    
    r = requests.get(upstream_server[0]  + '/users/', params=payload)
    logging.debug(r)
    
    r_json = r.json()
    if r_json:
        user_pass = r_json['resources']
        logging.debug(f"'resources': {user_pass}")
    if user_pass:
        return f"{username} is authenticated"
    else:
        return "Authentication Required"

# get the correct PORT numbers from the configuration file
def get_upstream_servers(url):
    logging.debug(f'url in func: {url}')
    if "/followers/" in url:
        url = "/users/"
    tempRoutes = "routes." + "'" + url + "'"
    logging.debug(f'tempRoute: {tempRoutes}')
    
    upstream_servers = json_config(tempRoutes) 
    logging.debug(f'upstream server in get: {upstream_servers}')
    
    if not upstream_servers:
        abort(503, "There is no post server available")
    
    
    for upstream_server in upstream_servers:
        try:
            r = requests.get(upstream_server)
            r.raise_for_status()
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            upstream_servers.remove(upstream_server)
            logging.debug(f"remove {upstream_server}")
            logging.debug(f"currents servers: {upstream_servers}")
        except requests.exceptions.HTTPError:
            if r.status_code >= 500:
                upstream_servers.remove(upstream_server)
            logging.debug(f"remove {upstream_server}")
            logging.debug(f"currents servers: {upstream_servers}")
        else:
            logging.debug("All is good")  
    # upstream_server = ModifiableCycle(upstream_servers)     
    return (upstream_servers)

@route('<url:re:.*>', method='ANY')
@auth_basic(is_authenticated_user)
def gateway(url):
    path = request.urlparts._replace(scheme='', netloc='').geturl()
    logging.debug(f"url: {url}") 
    logging.debug(f"path: {path}") 


    upstream_servers = get_upstream_servers(url)
    logging.debug(f"upstream servers: {upstream_servers}")
    upstream_server = upstream_servers[0]

    logging.debug(f"upstream server: {upstream_server}")
    upstream_url = upstream_server + path
    logging.debug('Upstream URL: %s', upstream_url)

    headers = {}
    for name, value in request.headers.items():
        if name.casefold() == 'content-length' and not value:
            headers['Content-Length'] = '0'
        else:
            headers[name] = value

    try:
        upstream_response = requests.request(
            request.method,
            upstream_url,
            data=request.body,
            headers=headers,
            cookies=request.cookies,
            stream=True,
        )
    except requests.exceptions.RequestException as e:
        logging.exception(e)
        response.status = 503
        return {
            'method': e.request.method,
            'url': e.request.url,
            'exception': type(e).__name__,
        }

    response.status = upstream_response.status_code
    for name, value in upstream_response.headers.items():
        if name.casefold() == 'transfer-encoding':
            continue
        response.set_header(name, value)
    return upstream_response.content

# adapted from https://stackoverflow.com/questions/24438153/modify-itertools-cycle
# helper function to remove an item from itertools cycle 
class ModifiableCycle(object):
    def __init__(self, items=()):
        self.deque = deque(items)
    def __iter__(self):
        return self
    def __next__(self):
        if not self.deque:
            return None
        item = self.deque.popleft()
        self.deque.append(item)
        return item
    next = __next__
    def delete_next(self):
        self.deque.popleft()
    def delete_prev(self):
        self.deque.pop()

'''Adding a new REST endpoint
Recall that Project 2 called for each service to have its own separate database. 
(If you did not complete Project 2, this is mocked up in the separate-dbs version of Mockroblog.)
This separation makes implementing the client-side API call getHomeTimeline(username) 
awkward because it requires two back-end service calls:
A call to the Users service (or users-queries service in Mockroblog) 
service to retrieve a list of the users that username follows
A call to the Timelines service (or timelines-queries service in Mockroblog) 
to retrieve the timelines for those users.
Implement a new REST endpoint in the gateway (e.g. @get('/home/<username>')) 
using the Requests library to make API calls to both services. If you are using Tuffix, the Requests module is already installed.
'''
@get('/home/<username>/')
@auth_basic(is_authenticated_user)
def home(username):
    # A call to the Users service (or users-queries service in Mockroblog)
    #  service to retrieve a list of the users that username follows
    payload = {'_facet': 'username', 'username': username, '_shape': 'array'}
    logging.debug(f"payload: {payload}")
    tempList = []
    following_server = get_upstream_servers('/users/following.json')
    r = requests.get(following_server[0] + '/users/following.json', params = payload)
    logging.debug(r.text)
    tempUsersFollowing = r.json()
    logging.debug(f"tempUserFollowing: {tempUsersFollowing}")
    for value in tempUsersFollowing:
        tempList.append(value['friendname'])
    logging.debug(f"tempList: {tempList}")
    logging.debug('done')

    # A call to the Timelines service (or timelines-queries service in Mockroblog) 
    # to retrieve the timelines for those users. 
    temp_servers = get_upstream_servers('/posts/')
    logging.debug(f"posts servers: {temp_servers}")
    # load balancer part
    # timelines_server = itertools.cycle(temp_servers) 
    users_timeline = []
    for user in tempList:
        user_payload = {'username': user, 'sort': "-timestamp"}
        
        try:
            if temp_servers:
                temp_timelines_server = temp_servers[0]
                logging.debug(f"temp_times_server: {temp_timelines_server}")
                user_reqs = requests.get(temp_timelines_server + '/posts/', params = user_payload, timeout= 1)
                temp_servers.append(temp_timelines_server)
                temp_servers.pop(0)
                logging.debug(f"New temp_servers: {temp_servers}")
                logging.debug(f"user_reqs: {user_reqs.status_code}")
        except:
            abort(503, "There is no server available")       
        # if (user_reqs.status_code >= 500):
        #     posts_servers_roundrobin.delete_prev()
        user_reqs_json = user_reqs.json()
        # added all the posts of the users that username is following into users_timeline
        if user_reqs_json:
            temp_res = user_reqs_json['resources']    
            for res in temp_res:
                users_timeline.append(res)

    response.status = 200
    return {'resources': users_timeline}  
  
#authentication part
@get('/')
@auth_basic(is_authenticated_user)
def homeNew():
    
  return ['hooray,you are authenticated! your info is {}'.format(request.auth)]
