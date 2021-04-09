## Designed to be a base layer to inherit from with the monitoring script and python 3 pre-installed.
## The API_TOKEN and BASE_URL already injected in the build
## --- TAKE CARE IN USING THIS APPROACH ---
## The token will be visible on the image upon inspection
## and therefore doesn't follow Docker's Best Practices
## --- Internal/private Use Only ---
ARG DISTRO_TAG=latest

FROM alpine:${DISTRO_TAG} AS packages

RUN apk update && apk upgrade \
  && apk add python3 \
  && pip3 install --upgrade pip \
  && pip3 install requests

FROM packages AS baseLayer

COPY ./docker/entrypoint.sh /entrypoint.sh
COPY varnish_metrics.py /opt/dynatrace/varnish_metrics.py
RUN chmod -R 755 /opt/dynatrace && chmod -R 755 /entrypoint.sh

ARG API_TOKEN
ARG BASE_URL
ARG APP_NAME

ENV API_TOKEN=${API_TOKEN:-"No token provided"}
ENV BASE_URL=${BASE_URL:-"No url provided"}
ENV APP_NAME=${APP_NAME:-"localhost"}

ENTRYPOINT [ "sh", "-c", "/entrypoint.sh" ]