## Docker

This Dockerfile provides a building block to serve as a base layer to instrument Varnish.
After forking this repo you can choose to add the required layers to the Dockerfile or
simply build this Dockerfile with the appropriate build arguments, save it to your private
docker registry and start using that as your base-layer of your Varnish docker image build.

Example command for building this from the `../technologies/varnish/monitor-varnish-cache/` directory:
```
$ docker build -t varnish-metrics -f ./docker/Dockerfile --build-arg APP_NAME=myapp --build-arg BASE_URL=<your.api.url> --build-arg API_TOKEN=<token> .
```
Now your Varnish image can start using this layer:
```
FROM varnish-metrics:latest AS varnish

RUN apk add varnish
... ## and so on in your Varnish image

```