# ordinary_portal

I really like the general idea behind magic-wormhole, and it's great for many things.

This is a work in progress attempt at imitating it's core functionality with smaller, pure Python dependencies.

Though it's less featured, I have made it to install faster.
It has this README serving as a quick setup guide with a public message broker server like Wormhole does.
Though I could take down the connecting server at any point, it is easy to host another using server.py on a public IP.

This was mostly coded over the weekend.

I based a 'Portal Creator', and a 'Downloader' around a message broker - a shared websocket server, that relays messages to all clients.


- The Portal Creator ('ordinary_portal send') generates a pass phrase to be shared.
- The pass phrase is turned into an encryption key that costs CPU cycles (to reduce the chance of abuse).
- After the 'Downloader' enters the pass phrase, it generates a key pair.
- The 'Downloader' then responds to the Portal creator by sharing it's public encryption key.
- The 'Portal Creator' then encrypts a string or a binary file, so that only the 'Downloader' can read it.
- That's it, the data is securely received by only one party and both parties disconnect from the message broker, happily going about their lives without a Covid laced USB stick or emails needing be passed around.


That's the idea anywhere. I might well adjust the protocol above.
No warranty is expressed or implied, this was written with little sleep, for fun and to satisfy my own needs and curiosity.
It's not been audited or anything, but it's pretty small and easy to read.
Constructive pointers and PR's are welcome!


I would like something I could use for quickly sharing SSH public keys, little scripts, and such.

### Experimental pip installation:

pip3 install --user --upgrade https://github.com/lukestanley/ordinary-portal/archive/master.zip

### Upload the super secret message by running this and following prompts:

ordinary_portal send

### Receive the message by running this:
ordinary_portal download

####This is a work in progress!

**Websocket server dependencies**
Currently the Pipfile records the dependencies for the 'Portal Creator' and the 'Downloader', but not the 'server'.
This is because I haven't refined a lightweight server yet.

That said, for me on Ubuntu, this works to get a Websocket message broker going on localhost:9999:

sudo pip install autobahn[twisted]

python server.py

I'm running that on a publicly accessible VPS until it is abused.

Then clients would connect to it. Currently config.py has the websocket message broker's server and port specified.

