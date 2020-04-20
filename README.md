# ordinary-portal

I really like the general idea behind magic-wormhole, and it's great for many things.

This is a work in progress attempt at imitating it's core functionality with smaller, pure Python dependencies.

Ideally it would install faster, and have a quick setup guide with a public message broker server like Wormhole does.

That's still TODO, this is just a little code done over the weekend.

I based a 'Portal Creator', and a 'Downloader' around a message broker - a shared websocket server, that relays messages to all clients.


- The Portal Creator generates a pass phrase to be shared.
- The pass phrase is turned into an encryption key that costs CPU cycles.
- After the 'Downloader' enters the pass phrase, it generates a key pair.
- The 'Downloader' then responds to the Portal creator by sharing it's public encryption key.
- The 'Portal Creator' then encrypts a string or a binary file, so that only the 'Downloader' can read it.
- That's it, the data is securely received by only one party and both parties disconnect from the message broker, happily going about their lives without a Covid laced USB stick or emails needing be passed around.


That's the idea anywhere, no warranty is expressed or implied :D

I would like something I could use for quickly sharing SSH public keys.
It doesn't do this super well yet and is more of a toy at the moment but it is quite lightweight and readable.

Currently the Pipfile records the dependencies for the 'Portal Creator' and the 'Downloader', but not the 'server'.
This is because I haven't refined a lightweight server yet.

That said, for me on Ubuntu, this works to get a Websocket message broker going on localhost:9999:

sudo pip install autobahn[twisted]

python server.py

I'm running that on a publicly accessible VPS until it is abused.

Then clients would connect to it. Currently config.py has the websocket message broker's server and port specified.

With Pipenv dependencies installed you could run to "open a portal":

pipenv run python portal_uploader.py


Then get the data passed through the portal using:
pipenv run python downloader.py
(after entering the key).

Most of the time, it should be possible to reuse a shared websocket server as a message broker.
That's the idea anyhow!

WIP!