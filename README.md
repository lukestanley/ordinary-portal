# ordinary-portal

I really like the general idea behind magic-wormhole, and it's great for many things.
This is a work in progress attempt at imitating it's core functionality with smaller, pure Python dependencies.
Ideally it would install faster.
I based a 'Portal Creator', and a 'Downloader' around a shared websocket server, that relays messages to all clients.
The Portal Creator generates a pass phrase to be shared.
The pass phrase is turned into an encryption key that costs CPU cycles.
After the 'Downloader' enters the pass phrase, it responds to the Portal creator by sharing a public encryption key.
The 'Portal Creator' then encrypts a string or a binary file, so that only the 'Downloader' can read it.
That's the idea anywhere, no warranty is expressed or implied :D
I would like something I could use for quickly sharing SSH public keys.
It doesn't do this super well yet and is more of a toy at the moment but it is quite lightweight and readable.

Currently the Pipfile records the dependencies for the 'Portal Creator' and the 'Downloader', but not the 'server'.
This is because I haven't refined a lightweight server yet.
Most of the time, it should be possible to reuse a shared websocket server as a message broker.
That's the idea anyhow!