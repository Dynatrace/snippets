Enrich PurePath with OpenTelemetry instrumentation
===================================================

This blog post demo app leverage Go OpenTelemetry to enrich PurePath with data from TCP protocol.
The blog post `Leverage automated and intelligent observability for OpenTelemetry for Go with Dynatrace PurePath 4 <https://www.dynatrace.com/news/blog/leverage-automated-and-intelligent-observability-for-opentelemetry-for-go-with-dynatrace-purepath-4/>`_ describes this sample.

Disclaimer
-----------

The contained code is considered educational and NOT SUPPORTED by Dynatrace.
Please use at your own risk. You can contact the author via Github issues.

Deploy Dynatrace OneAgent
--------------------------

see `Dynatrace OneAgent documentation <https://www.dynatrace.com/support/help/setup-and-configuration/dynatrace-oneagent/>`_

Install Go SDK 1.13 or higher
------------------------------

see https://golang.org/doc/install

Compile Client app and define Custom service
---------------------------------------------

Compile Client app::

    > cd ./client/
    > go build

Run Client app and select *main.processTCPRequest* function as an entry point for a `custom service <https://www.dynatrace.com/news/blog/introducing-custom-services-for-go-applications/>`_.


Compile Server app
-------------------

Compile Server app::

    > cd ./server/
    > go build


Run compiled apps
------------------

1. Run Client app
2. Run Server app
3. Make TCP request to TCP server which is running on port *1234* by using *telnet* utility, e.g.

    telnet localhost 1234
