Group members: Cindy Quach, Dalisa Nguyen, Tevin Vu
1. In the terminal, run this command to start microservices
$ foreman start 
or 
$ foreman start -m gateway=1,users=1,timelines=3,user-queries=1,timeline-queries=1

1. File gateway.ini information:
- [routes]
'/users/' = ["http://localhost:5100"]  --> users services
'/users/following.json' = ["http://localhost:5300"] --> users services
'/followers/' = ["http://localhost:5100"] --> users services
'/posts/' = ["http://localhost:5200", "http://localhost:5201", "http://localhost:5202"] --> timelines services
'/timelines/posts.json' = ["http://localhost:5400"] --> timelines services 



2. Sample API calls
*** createUser(username, email, password) *** 
http -a ProfGofman:secur POST localhost:5000/users/ username=ProfGofman email=Gofman@gmail.com password=secur
HTTP/1.0 201 Created
Content-Length: 79
Content-Type: application/json
Date: Tue, 25 May 2021 02:54:16 GMT
Link: </users/9>; rel=self, </users/9>; rel=related
Server: Werkzeug/1.0.1 Python/3.6.0

{
    "email": "Gofman@gmail.com",
    "id": 9,
    "password": "secur",
    "username": "ProfGofman"
}

*** authenticateUser(username, password) ***
$ http --verbose -a ProfGofman:secur GET 'localhost:5000/users/?username=ProfGofman&password=secur'
GET /users/?username=ProfGofman&password=secur HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Authorization: Basic UHJvZkdvZm1hbjpzZWN1cg==
Connection: keep-alive
Host: localhost:5000
User-Agent: HTTPie/2.4.0



HTTP/1.0 200 OK
Content-Length: 95
Content-Type: application/json
Date: Tue, 25 May 2021 02:57:16 GMT
Etag: "27c230b17e9ea7acf74b8e664caae208"
Server: Werkzeug/1.0.1 Python/3.6.0

{
    "resources": [
        {
            "email": "Gofman@gmail.com",
            "id": 9,
            "password": "secur",
            "username": "ProfGofman"
        }
    ]
}

#authenticateUser() doesn't require HTTP Basic authentication
*** authenticateUser(username, password) ***
http --verbose http://localhost:5000/users/ProfAvery/password/
GET /users/ProfAvery/password/ HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Host: localhost:5000
User-Agent: HTTPie/2.4.0



HTTP/1.0 200 OK
Content-Length: 26
Content-Type: text/html; charset=UTF-8
Date: Wed, 26 May 2021 02:54:31 GMT
Server: WSGIServer/0.2 CPython/3.6.0

ProfAvery is authenticated



*** addFollower(username, usernameToFollow) ***
http -a ProfGofman:secur POST localhost:5000/followers/ follower_id=9 following_id=2
HTTP/1.0 201 Created
Content-Length: 43
Content-Type: application/json
Date: Tue, 25 May 2021 02:58:49 GMT
Link: </followers/12>; rel=self, </followers/12>; rel=related, </users/9>; rel=related
Server: Werkzeug/1.0.1 Python/3.6.0

{
    "follower_id": 9,
    "following_id": 2,
    "id": 12
}

*** getUserTimeline(username) ***
http -a ProfAvery:password GET 'localhost:5000/posts/?username=ProfAvery&sort=-timestamp'
HTTP/1.0 200 OK
Content-Length: 456
Content-Type: application/json
Date: Tue, 25 May 2021 03:01:04 GMT
Etag: "e9c728790d62022a8ad9a3389a776845"
Server: Werkzeug/1.0.1 Python/3.6.0

{
    "resources": [
        {
            "id": 1,
            "text": "Meanwhile, at the R1 institution down the street... https://uci.edu/coronavirus/messages/200710-sanitizer-recall.php",
            "timestamp": "2021-03-25 13:09:31",
            "username": "ProfAvery"
        },
        {
            "id": 2,
            "text": "FYI: https://www.levels.fyi/still-hiring/",
            "timestamp": "2021-03-25 13:09:31",
            "username": "ProfAvery"
        },
        {
            "id": 3,
            "text": "Yes, the header file ends in .h. C++ is for masochists.",
            "timestamp": "2021-03-25 13:09:31",
            "username": "ProfAvery"
        }
    ]
}


id=$(http -a ProfGofman:secur GET 'localhost:5000/followers/?follower_id=9&following_id=2' | jq '.resources[0].id')
???  gateway http -a ProfGofman:secur DELETE localhost:5000/followers/$id
HTTP/1.0 204 No Content
Content-Length: 0
Date: Tue, 25 May 2021 03:03:04 GMT
Server: Werkzeug/1.0.1 Python/3.6.0


*** getPublicTimeline() ***
$ http --verbose -a ProfGofman:secur GET 'localhost:5000/posts/?sort=-timestamp'
GET /posts/?sort=-timestamp HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Authorization: Basic UHJvZkdvZm1hbjpzZWN1cg==
Connection: keep-alive
Host: localhost:5000
User-Agent: HTTPie/2.4.0



HTTP/1.0 200 OK
Content-Length: 1418
Content-Type: application/json
Date: Tue, 25 May 2021 03:06:02 GMT
Etag: "32286e4d43ec8a6bcf65cf5fae46144f"
Server: Werkzeug/1.0.1 Python/3.6.0

{
    "resources": [
        {
            "id": 9,
            "text": "Let buy some Tesla stock",
            "timestamp": "2021-04-05 04:50:20",
            "username": "Ammania"
        },
        {
            "id": 8,
            "text": "All of me",
            "timestamp": "2021-04-02 22:28:41",
            "username": "JohnLegend"
        },
        {
            "id": 7,
            "text": "Let's get some boba",
            "timestamp": "2021-03-30 04:23:02",
            "username": "Ammania"
        },
        {
            "id": 6,
            "text": "#cpsc315 #engr190w NeurIPS is $25 for students and $100 for non-students this year! https://medium.com/@NeurIPSConf/neurips-registration-opens-soon-67111581de99",
            "timestamp": "2021-03-25 13:09:31",
            "username": "Beth_CSUF"
        },
        {
            "id": 5,
            "text": "I keep seeing video from before COVID, of people not needing to mask or distance, and doing something like waiting in line at Burger King. YOU'RE WASTING IT!",
            "timestamp": "2021-03-25 13:09:31",
            "username": "KevinAWortman"
        },
        {
            "id": 4,
            "text": "If academia were a video game, then a 2.5 hour administrative meeting that votes to extend time 15 minutes is a fatality. FINISH HIM",
            "timestamp": "2021-03-25 13:09:31",
            "username": "KevinAWortman"
        },
        {
            "id": 3,
            "text": "Yes, the header file ends in .h. C++ is for masochists.",
            "timestamp": "2021-03-25 13:09:31",
            "username": "ProfAvery"
        },
        {
            "id": 2,
            "text": "FYI: https://www.levels.fyi/still-hiring/",
            "timestamp": "2021-03-25 13:09:31",
            "username": "ProfAvery"
        },
        {
            "id": 1,
            "text": "Meanwhile, at the R1 institution down the street... https://uci.edu/coronavirus/messages/200710-sanitizer-recall.php",
            "timestamp": "2021-03-25 13:09:31",
            "username": "ProfAvery"
        }
    ]
}


*** getHomeTimeline(username) ***
$ friends=$(http -a ProfAvery:password GET 'localhost:5000/users/following.json?_facet=username&username=ProfAvery&_shape=array' | jq --raw-output 'map(.friendname) | join(",")') 
$ http -a ProfAvery:password GET "http://localhost:5000/timelines/posts.json?_sort_desc=timestamp&_shape=array&username__in=$friends"

HTTP/1.0 200 OK
Content-Length: 244
Content-Type: application/json; charset=utf-8
Date: Tue, 25 May 2021 03:10:02 GMT
Referrer-Policy: no-referrer
Server: uvicorn

[
    {
        "id": 6,
        "text": "#cpsc315 #engr190w NeurIPS is $25 for students and $100 for non-students this year! https://medium.com/@NeurIPSConf/neurips-registration-opens-soon-67111581de99",
        "timestamp": "2021-03-25 13:09:31",
        "username": "Beth_CSUF"
    }
]

*** postTweet(username, text) ***
$ http -a ProfGofman:secur POST localhost:5000/posts/ username=ProfGofman text='I will teach Web Security next semester.'

HTTP/1.0 201 Created
Content-Length: 118
Content-Type: application/json
Date: Tue, 25 May 2021 03:12:59 GMT
Link: </posts/10>; rel=self, </posts/10>; rel=related
Server: Werkzeug/1.0.1 Python/3.6.0

{
    "id": 10,
    "text": "I will teach Web Security next semester.",
    "timestamp": "2021-05-25 03:12:59",
    "username": "ProfGofman"
}


*** New Rest Endpoint Test ***
$ http -a Ammania:easy GET localhost:5000/home/Ammania/

HTTP/1.0 200 OK
Content-Length: 1024
Content-Type: application/json
Date: Tue, 25 May 2021 03:16:37 GMT
Server: WSGIServer/0.2 CPython/3.6.0

{
    "resources": [
        {
            "id": 1,
            "text": "Meanwhile, at the R1 institution down the street... https://uci.edu/coronavirus/messages/200710-sanitizer-recall.php",
            "timestamp": "2021-03-25 13:09:31",
            "username": "ProfAvery"
        },
        {
            "id": 2,
            "text": "FYI: https://www.levels.fyi/still-hiring/",
            "timestamp": "2021-03-25 13:09:31",
            "username": "ProfAvery"
        },
        {
            "id": 3,
            "text": "Yes, the header file ends in .h. C++ is for masochists.",
            "timestamp": "2021-03-25 13:09:31",
            "username": "ProfAvery"
        },
        {
            "id": 6,
            "text": "#cpsc315 #engr190w NeurIPS is $25 for students and $100 for non-students this year! https://medium.com/@NeurIPSConf/neurips-registration-opens-soon-67111581de99",
            "timestamp": "2021-03-25 13:09:31",
            "username": "Beth_CSUF"
        },
        {
            "id": 9,
            "text": "Let buy some Tesla stock",
            "timestamp": "2021-04-05 04:50:20",
            "username": "Ammania"
        },
        {
            "id": 7,
            "text": "Let's get some boba",
            "timestamp": "2021-03-30 04:23:02",
            "username": "Ammania"
        },
        {
            "id": 8,
            "text": "All of me",
            "timestamp": "2021-04-02 22:28:41",
            "username": "JohnLegend"
        }
    ]
}

3. Load Balancing

Command Terminal:
$ http -a Ammania:easy GET localhost:5000/home/Ammania/

HTTP/1.0 200 OK
Content-Length: 1024
Content-Type: application/json
Date: Tue, 25 May 2021 03:16:37 GMT
Server: WSGIServer/0.2 CPython/3.6.0

Foreman Terminal:
20:16:25 timelines.1        | 127.0.0.1 - - [25/May/2021 20:16:25] "GET / HTTP/1.1" 200 -
20:16:25 gateway.1          | reply: 'HTTP/1.0 200 OK\r\n'
20:16:25 gateway.1          | DEBUG in root: All is good
20:16:25 gateway.1          | header: Content-Type header: Content-Length header: Server header: Date send: b'GET / HTTP/1.1\r\nHost: localhost:5201\r\nUser-Agent: python-requests/2.24.0\r\nAccept-Encoding: gzip, deflate\r\nAccept: */*\r\nConnection: keep-alive\r\n\r\n'
20:16:25 timelines.2        | 127.0.0.1 - - [25/May/2021 20:16:25] "GET / HTTP/1.1" 200 -
20:16:25 gateway.1          | reply: 'HTTP/1.0 200 OK\r\n'
20:16:25 gateway.1          | DEBUG in root: All is good
20:16:25 gateway.1          | header: Content-Type header: Content-Length header: Server header: Date send: b'GET / HTTP/1.1\r\nHost: localhost:5202\r\nUser-Agent: python-requests/2.24.0\r\nAccept-Encoding: gzip, deflate\r\nAccept: */*\r\nConnection: keep-alive\r\n\r\n'
20:16:25 timelines.3        | 127.0.0.1 - - [25/May/2021 20:16:25] "GET / HTTP/1.1" 200 -
20:16:25 gateway.1          | reply: 'HTTP/1.0 200 OK\r\n'
20:16:25 gateway.1          | DEBUG in root: All is good
20:16:25 gateway.1          | DEBUG in root: posts servers: ['http://localhost:5200', 'http://localhost:5201', 'http://localhost:5202']
20:16:25 gateway.1          | DEBUG in root: temp_times_server: http://localhost:5200
20:16:25 gateway.1          | header: Content-Type header: Content-Length header: Server header: Date send: b'GET /posts/?username=ProfAvery&sort=-timestamp HTTP/1.1\r\nHost: localhost:5200\r\nUser-Agent: python-requests/2.24.0\r\nAccept-Encoding: gzip, deflate\r\nAccept: */*\r\nConnection: keep-alive\r\n\r\n'
20:16:25 timelines.1        | 127.0.0.1 - - [25/May/2021 20:16:25] "GET /posts/?username=ProfAvery&sort=-timestamp HTTP/1.1" 200 -
20:16:25 gateway.1          | reply: 'HTTP/1.0 200 OK\r\n'
20:16:25 gateway.1          | DEBUG in root: New temp_servers: ['http://localhost:5201', 'http://localhost:5202', 'http://localhost:5200']
20:16:25 gateway.1          | DEBUG in root: user_reqs: 200
20:16:25 gateway.1          | DEBUG in root: temp_times_server: http://localhost:5201
20:16:25 gateway.1          | header: Content-Type header: Content-Length header: ETag header: Server header: Date send: b'GET /posts/?username=Beth_CSUF&sort=-timestamp HTTP/1.1\r\nHost: localhost:5201\r\nUser-Agent: python-requests/2.24.0\r\nAccept-Encoding: gzip, deflate\r\nAccept: */*\r\nConnection: keep-alive\r\n\r\n'
20:16:25 timelines.2        | 127.0.0.1 - - [25/May/2021 20:16:25] "GET /posts/?username=Beth_CSUF&sort=-timestamp HTTP/1.1" 200 -
20:16:25 gateway.1          | reply: 'HTTP/1.0 200 OK\r\n'
20:16:25 gateway.1          | DEBUG in root: New temp_servers: ['http://localhost:5202', 'http://localhost:5200', 'http://localhost:5201']
20:16:25 gateway.1          | DEBUG in root: user_reqs: 200
20:16:25 gateway.1          | DEBUG in root: temp_times_server: http://localhost:5202
20:16:25 gateway.1          | header: Content-Type header: Content-Length header: ETag header: Server header: Date send: b'GET /posts/?username=Ammania&sort=-timestamp HTTP/1.1\r\nHost: localhost:5202\r\nUser-Agent: python-requests/2.24.0\r\nAccept-Encoding: gzip, deflate\r\nAccept: */*\r\nConnection: keep-alive\r\n\r\n'
20:16:25 timelines.3        | 127.0.0.1 - - [25/May/2021 20:16:25] "GET /posts/?username=Ammania&sort=-timestamp HTTP/1.1" 200 -
20:16:25 gateway.1          | reply: 'HTTP/1.0 200 OK\r\n'
20:16:25 gateway.1          | DEBUG in root: New temp_servers: ['http://localhost:5200', 'http://localhost:5201', 'http://localhost:5202']
20:16:25 gateway.1          | DEBUG in root: user_reqs: 200
20:16:25 gateway.1          | DEBUG in root: temp_times_server: http://localhost:5200
20:16:25 gateway.1          | header: Content-Type header: Content-Length header: ETag header: Server header: Date send: b'GET /posts/?username=JohnLegend&sort=-timestamp HTTP/1.1\r\nHost: localhost:5200\r\nUser-Agent: python-requests/2.24.0\r\nAccept-Encoding: gzip, deflate\r\nAccept: */*\r\nConnection: keep-alive\r\n\r\n'
20:16:25 timelines.1        | 127.0.0.1 - - [25/May/2021 20:16:25] "GET /posts/?username=JohnLegend&sort=-timestamp HTTP/1.1" 200 -
20:16:25 gateway.1          | reply: 'HTTP/1.0 200 OK\r\n'
20:16:25 gateway.1          | DEBUG in root: New temp_servers: ['http://localhost:5201', 'http://localhost:5202', 'http://localhost:5200']
20:16:25 gateway.1          | DEBUG in root: user_reqs: 200
20:16:25 gateway.1          | 127.0.0.1 - - [25/May/2021 20:16:25] "GET /home/Ammania/ HTTP/1.1" 200 1024