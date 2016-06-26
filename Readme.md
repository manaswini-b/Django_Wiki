# Wiki app in Django

## this makes basic works that the wiki app do!

### Api links

-	/wiki/api/add/:title
	(Ex:  curl --data "content=First_Article" -X POST http://localhost:8000/wiki/api/add/welcome/)
	POST request
	Should contain a key("content") with value as the article content in POST request.
	Will return a json with key("status")
	{"status" : "200 OK"} -> The article is edited succesfully.(If :title is already available)
	{"status" : "201 Empty"} -> The article is created succesfully.
	{"status" : "202 Invalid"} -> Not a proper POST request.

-	/wiki/api/all
	GET request
	Will return a json with a key("title").
	The value to the key is a list that contains all the article titles.

-	/wiki/api/:title
	GET request
	(Ex: wiki/api/welcome, where 'welcome' is an article title)
	Will return a json with a key("content").
	The value to the key is the content of the corresponding article.

-	/wiki/:title/delete
	DELETE request
	(Ex: wiki/welcome/delete, where 'welcome' is an article title)
	Will return a json with key("status")
	{"status" : "200 OK"} -> Will delete the entire article if exists.
	{"status" : "404 Error"} -> If the article doesn't exist.