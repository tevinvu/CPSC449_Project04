1. File gateway.ini information:
- [routes]
'/users/' = ["http://localhost:5100"]  --> users services
'/users/following.json' = ["http://localhost:5300"] --> users services
'/followers/' = ["http://localhost:5100"] --> users services
'/posts/' = ["http://localhost:5200", "http://localhost:5201", "http://localhost:5202"] --> timelines services
'/timelines/posts.json' = ["http://localhost:5400"] --> timelines services 





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

 http --verbose -a ProfGofman:secur GET 'localhost:5000/users/?username=ProfGofman&password=secur'
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
➜  gateway http -a ProfGofman:secur DELETE localhost:5000/followers/$id
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
http -a Ammania:easy GET localhost:5000/home/Ammania/
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

