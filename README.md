# resin-home-automator
Example Python Flask web app deployable via resin.io for periodic Celery tasks
Deployed as a Flask web app that works on any of the `ARMv7` devices supported
by [resin.io][resin-link].

## Deployment

To get this project up and running, once you are set up with resin.io,
you need to add your resin.io application's remote (the exact url will vary for
different users, so consult the [Resin docs](http://docs.resin.io/) to get
started with a new app):

    git remote add resin gh_kermit666@git.resin.io:gh_kermit666/homeautomator.git

and push the code to the newly added remote:

    git push resin master

It should take a few minutes for the code to push. While you wait,
enable device URLs so the server can be accessed outside of its local network.
This option can be found in the `Actions` tab in your device dashboard.

![Actions Tab](/img/enable-public-URLs.png)

Once the device is updated, you should see this in your logs:
![log output](/img/log-output.png)

Then in your browser you should be able to open the device URL and see web app.

## Development

Install & configure [Docker-machine](https://www.docker.com/docker-machine).
Build the image:

    docker build -f Dockerfile.dev.base -t resin/armv7hf-debian . # only once
    docker build -t homeautomator .

You can now run it:

    docker run -i -p 8080:80 homeautomator

And open it on the Docker-machine url (`docker-machine ip default`)
and port 8080, e.g. <http://192.168.99.100:8080/>.

### No Docker?

If you just want to run the Flask web app, install requirements in a venv:

    python3 -m venv venv # only once
    source venv/bin/activate
    pip install -r src/requirements.txt # only after updates

and run it:

    honcho -f Procfile.dev start

### Cleanup

You clean all the stopped Docker containers with:

    docker rm $(docker ps -a -q -f status=exited)

and the Docker images with:

    docker rmi -f $(docker images -a | grep "<none>" | awk "{print \$3}")

[resin-link]:https://resin.io/
[signup-page]:https://dashboard.resin.io/signup
[gettingStarted-link]:http://docs.resin.io/#/pages/installing/gettingStarted.md
