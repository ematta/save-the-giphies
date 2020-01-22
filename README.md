# CLOSING OUT

A lot of lessons were learned here and I am moving the effort over to [my main site's codebase](https://github.com/ematta/matta.dev). Thank you for following this short journey.

## Save the giphies

Documentation in progress, but here is how we can get you up and running for now.

### Env vars

You need the following environment variables for the server:

```
GIPHY_API_KEY=xxxxx # The API key generate by Giphy
POSTGRES_URL=localhost # You will be running PG locally via docker
POSTGRES_PORT=5432 # You cannot customize this for now
POSTGRES_USER=thegiphies # Create any user you want
POSTGRES_PASSWORD=xxxxx # Create any password you want
POSTGRES_DB=save_the_giphies # Create any db name you want
SECRET_KEY=xxxxx # any random text, I would suggest you use openssl rand -base64 32 
```

### Contributing to server

_Python version: 3.8.x_

There are a couple of steps you need to do before you can properly call the server. First, you need postgres libraries. If you are on linux, you are in luck. Just install `libpq-dev` through your favorite package manager. Unfortunately, for Mac, you need to go through the hassle of running `brew install postgres openssl` and setting these env vars:

```
export LDFLAGS="-L/usr/local/opt/openssl/lib"
export CPPFLAGS="-I/usr/local/opt/openssl/include"
```

This is for `psychopg` which requires pg headers.

The next part is fairly straight forward. Running `make` will serve a development version of the api server. It creates your virtualenv and installs your libraries. You can also run `make tests` to verify tests and `make check-code` to make sure your code is up to snuff.

Finally, we need to provision the database. To do this run `python db.py` in the server folder. ***WARNING: THIS WILL DROP AND CREATE, SO IF YOU ARE ALREADY PROVISIONED DONT RE-RUN!***. We are currently working on improving the data migraiton experience.

### Contributing to client

_Node.js: 12.14_

We are using [`vue.js`](https://vuejs.org/) to serve our UI needs. As long as you have a node environment set up you should just run `npm run serve` to run a local development version. ***Before doing this, please make sure you run `npm i`***. Check your code with `npm run lint` and if you want to auto-fix, run `npm run lint -- --fix`. Also, check any new libraries you install with `npm audit fix`. Look in `client/env` for the current environmental variables we pass to Vue. 

### Running everything

At this point, since we are still working on dockerization, we have to awkwardly run two terminals.

- Terminal 1: In the root folder run `make run-api`
- Terminal 2: In the root folder run `make run-ui`

Navigate to `localhost:8080` and try it out!

## TODO

- Dockerize the app
- Push to a live environment
- Work on CSS
