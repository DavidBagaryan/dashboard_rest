this project is driven by python ^3.5 and pip ^19 

1. git clone https://gitlab.com/DavidBagaryan/dashboard_rest.git your/project/dir 
2. cd your/project/dir
3. virtualenv venv (install virtenv or analog) 
4. source venv/bin/activate(or analog activation)
5. pip install -r requirements.txt

then you can run migrations
6. cd dashboard_rest/
7. python manage.py makemigrations
8. python manage.py migrate

also, you can create superadmin
9. python manage.py createsuperuser and follow the instruction below

available possibility:
- articles list 
- create the article with associated tags
- edit article
- read article
- delete article

10. python manage.ry runserver (port number - optional)
11. copy URL below to test app (http://url:port)
11. to get articles list to emulate GET request to http://url:port/articles/list/
12. to create article emulate POST request (Content-Type: application/json) 
    to http://url:port/articles/create/ with params:
    article: {
      "title":"test title",
      "description":"test description",
      "author_name":"Test Author"
    }
    tags(optional, with any amount): [
      {
        "name":"test name 1"
      },
      {
        "name":"test name 2"
      },
      ...
    ]
13. to edit article emulate POST request (Content-Type: application/json) 
    to http://url:port/articles/edit/<article title>/ with the same params as create
14. to read article emulate get the request to 
    http://url:port/articles/read/<article title>/    
14. to delete article emulate DELETE request (Content-Type: application/json) 
    to http://url:port/articles/delete/<article title>/ witout params    
          
so, this is it
sorry for some shitty constructions in create/update actions
actually, this is my first REST API plus first practice with DRF
          
          
          
          
          
          
          