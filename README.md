### adapted from https://github.com/ProfAvery/cpsc449/tree/master/mockroblog/separate-dbs



# Sample API calls

**`createUser(username, email, password)`**

> ```shell-session
> $ http -a Ammania:easy POST localhost:5000/users/ username=Ammania email=Ammania@gmail.com password=easy
> ```

**`authenticateUser(username, password)`**

> ```shell-session
> $ http GET 'localhost:5000/users/ProfAvery/password/'
> ```

**`addFollower(username, usernameToFollow)`**

> ```shell-session
> $ http -a Ammania:easy POST localhost:5000/followers/ follower_id=4 following_id=2
> ```

**`removeFollower(username, usernameToRemove)`**

for mac OSX:
> ```shell-session
> $ id=$(http -a Ammania:easy GET 'localhost:5000/followers/?follower_id=4&following_id=2' | jq '.resources[0].id')
> $ http -a Ammania:easy DELETE localhost:5000/followers/$id
> ```

for Ubuntu/Tuffix:
> ```shell-session
> $ id=$(http -a Ammania:easy GET 'localhost:5000/followers/?follower_id=4&following_id=2' | jq .resources[0].id)
> $ http -a Ammania:easy DELETE localhost:5000/followers/$id
> ```

**`getUserTimeline(username)`**

> ```shell-session
> $ http -a ProfAvery:password GET 'localhost:5000/posts/?username=ProfAvery&sort=-timestamp'
> ```

**`getPublicTimeline()`**

> ```shell-session
> $ http -a ProfAvery:password GET 'http://localhost:5000/posts/?sort=-timestamp'
> ```

**`getHomeTimeline(username)`**

> ```shell-session
> $ http -a KevinAWortman:qwerty localhost:5000/home/KevinAWortman/
> ```

**`postTweet(username, text)`**

> ```shell-session
> $ http -a Ammania:easy POST localhost:5000/posts/ username=Ammania text='Let buy some Tesla stock'
> ```