# fb.com
This is a software replicating a subset of features of facebook.

Usage and GUI:
1. git clone https://github.com/warahul/fb.com
2. cd djangotest
3. python manage.py runserver
4. In browser, open http://127.0.0.1:8000/messenger/
5. There are a few users in the db, username="warahul", password="warahul"
6. If try to login using wrong username/password, it will show error.
7. On successful login, it takes you to home page, and asks you the name of the user to whom you want to send a message.
8. If it is first time that you are messaging that person, you should use the lower part to add the user (or users), as the lower GUI part is for creating new chats.
9. The upper part searches all existing chats with the searched user and you, bringing up the requisite list of options.
10. If there are unseen messages that came in when the user was loggen off or is inactive on the main page, a list of such chats open up at the top of the page.

Underlying implementation:
We have separate databases for Users, for holding which user has seen upto which messages in every chat and Messages, which stores the messages exchanged between a set of users, and who sent which message. We allow searching for users for every prefix of their name. For example, "wa" will give us all the messages that have "warahul" and "wadbude" as users.