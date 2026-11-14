# Messenger

A small web messenger built with Django. It supports personal chats and group chats, and new messages appear instantly for everyone in the chat without reloading the page.

I built it as a learning project to get hands-on with a custom user model, relationships between models, and real-time features through Django Channels and WebSockets.

## Features

- Sign up, log in and log out, using a custom user model with a display name, avatar field and short bio
- Personal chats: start a conversation with someone by their username, and the existing chat is reused if you already have one
- Group chats: create a group with a name and pick its members; the creator becomes the group admin
- Real-time messaging over WebSockets, with messages saved to the database so the history stays after a reload
- A plain form fallback: if the WebSocket connection is down, messages are still sent with a normal POST request and broadcast to the other members
- Access control on both pages and WebSocket connections, so you can only open and connect to chats you are a member of

## Tech stack

- Python 3.14, Django 6.1
- Django Channels with Daphne as the ASGI server
- Redis as the channel layer, through `channels-redis`
- PostgreSQL 17 and Redis 7, both running in Docker
- Bootstrap for styling and a little plain JavaScript on the chat page

## Getting started

You need Python 3, Docker Desktop and Git.

```bash
git clone https://github.com/IAmBeli/messenger.git
cd messenger

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

docker compose up -d
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Then open http://127.0.0.1:8000/. To try real-time messaging, sign up a second user in a private window and open the same chat in both windows.

PostgreSQL is exposed on port 5435 and Redis on port 6380, so they do not clash with other local projects that use the default ports.

## How it works

Regular pages such as the chat list, the chat page and the sign-up form are ordinary Django views served over HTTP.

When a chat page opens, its JavaScript connects to `/ws/chats/<id>/`. The `ChatConsumer` checks that the user is logged in and is a member of that chat, then adds the connection to a channel layer group named after the chat. When someone sends a message, the consumer validates it with the same form the HTTP fallback uses, saves it to PostgreSQL and sends it to the group. Redis delivers it to every open connection in that group, and each browser adds the new message to the page.

The code that broadcasts a message lives in `chats/broadcast.py`, so the WebSocket consumer and the fallback view share it.

## Project layout

```
accounts/    custom user model, sign-up form and view
chats/       chat models, views, forms, WebSocket consumer and routing
config/      settings, URL configuration and the ASGI entry point
templates/   base layout, auth pages and chat pages
```

## Not done yet

I wrapped up the project with a deliberately limited scope. These parts are left out:

- Managing a group after it is created: renaming it, adding or removing members, and leaving a group
- A profile page and avatar uploads (the fields exist on the user model, but media file handling is not set up)
- Unread message counters, and sorting the chat list by the latest message instead of creation time
- Production settings: `DEBUG` is on and the database credentials are hard-coded for local development

## A note on dependencies

`redis` is pinned below version 8. Version 8 of the Python client changed its default socket timeout to five seconds, which breaks the blocking reads that `channels-redis` uses to wait for new messages, and WebSocket connections dropped a few seconds after opening.