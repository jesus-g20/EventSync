EvenSync

EventSync solves the problem of managing and attending social events by providing an easy-touse platform where users can discover events, chat with attendees, and manage payments. Users can log in or sign up using secure authentication, search for events by location or category, and see a list of attendees.

A built-in chat system allows event participants to interact with each other, either one-on-one or
in group chats, helping people connect before the event. Event organizers can use the platform to
manage ticket sales, with a secure payment system powered by Stripe to handle transactions. The
app also offers a map view feature to help users easily find nearby events.

By integrating all these features into one app, EventSync makes it easier for people to organize,
find, and attend events, while promotion social connections

Steps to view the website and manage the administrative part:

1 - Create a virtual environment:

python3 -m venv virtualenv

2 - Activate the virtual environment:

source virtualenv/bin/activate

3 - Install dependencies (requirements.txt):

pip install -r requirements.txt

4 - Run the migrations:

python manage.py migrate

5 - Create the superuser:

python manage.py createsuperuser

6 - Run the server:

python manage.py runserver