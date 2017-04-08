# fb.com
This is a software replicating a subset of features of facebook.

Usage:
1. git clone https://github.com/warahul/fb.com
2. cd djangotest
3. python manage.py runserver
4. In browser, open http://127.0.0.1:8000/messenger/
5. Only one user exists in db, username="warahul", password="warahul"
6. If try to login using wrong username/password, it will show error.
7. On successful login, it takes you to home page, and ask you name and messege to send.
8. If it is first time that you are messeging that person, then it creates a 
    new Messege object and  add the yourself and the other person as the users of this object.
    If not then, it appends the messege sent to the previous ones, separted with "," and stores in database.
    Test: messege object is printed on the console, everytime you send messege,
