# Wiki app in Django

## this makes basic works that the wiki app do!

### API links

-	/wiki/api/add/:title<br/>
	(Ex:  curl --data "content=First_Article" -X POST http://localhost:8000/wiki/api/add/welcome/)<br/>
	POST request<br/>
	Should contain a key("content") with value as the article content in POST request.<br/>
	Will return a json with key("status")<br/>
	{"status" : "200 OK"} -> The article is edited succesfully.(If :title is already available)<br/>
	{"status" : "201 Empty"} -> The article is created succesfully.<br/>
	{"status" : "202 Invalid"} -> Not a proper POST request.<br/>

-	/wiki/api/all<br/>
	GET request<br/>
	Will return a json with a key("title").<br/>
	The value to the key is a list that contains all the article titles.<br/>

-	/wiki/api/:title<br/>
	GET request<br/>
	(Ex: wiki/api/welcome, where 'welcome' is an article title)<br/>
	Will return a json with a key("content").<br/>
	The value to the key is the content of the corresponding article.<br/>

-	/wiki/:title/delete<br/>
	GET request<br/>
	(Ex: wiki/welcome/delete, where 'welcome' is an article title)<br/>
	Will return a json with key("status")<br/>
	{"status" : "200 OK"} -> Will delete the entire article if exists.<br/>
	{"status" : "404 Error"} -> If the article doesn't exist.<br/>