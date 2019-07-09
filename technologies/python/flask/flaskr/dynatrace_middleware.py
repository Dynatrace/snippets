from wsgiref.util import request_uri
import oneagent.sdk
from oneagent import get_sdk
import socket

class DynatraceWSGIMiddleware(object):
    """An WSGI middleware that instruments the wrapped application (or
       middleware) with the OneAgent SDK for Python"""

    def __init__(self, app, app_id, virtual_host=None, context_root=None):
        """Creates a new DynatraceWSGIMiddleware.

        Args:
            app: The actual WSGI application to trace.
            app_id: The application_id, as passed to
                oneagent.sdk.SDK.create_web_application_info.
            virtual_host: The virtual_host to pass on to the SDK if none can be
                found in a request's WSGI environment.
            context_root: The context_root/prefix to pass on to the SDK if none
                can be found in a request's WSGI environment.
        """

        self.app = app
        self.app_id = app_id
        self.virtual_host = virtual_host
        self.context_root = context_root

    def __call__(self, environ, start_response):

        # Extract HTTP headers from the WSGI environment
        header_keys = []
        header_values = []
        for key in environ:
            if key.startswith(HTTP_PREFIX):
                header_keys.append(cgi_to_http_name(key))
                header_values.append(environ[key])

        # Trace the web request
        vhost = environ.get('SERVER_NAME') or \
                self.virtual_host or socket.gethostname() or 'localhost'
        ctxroot = environ.get('CONTEXT_PREFIX') or self.context_root or '/'
        with get_sdk().create_web_application_info(
                vhost, self.app_id, ctxroot) as wappinfo, \
            get_sdk().trace_incoming_web_request(
                wappinfo,
                get_request_uri(environ),
                environ['REQUEST_METHOD'],
                headers=(header_keys, header_values)) as tracer:

            # Storage for the response information received by start_response
            last_response_info = [(None, None, (None, None))]

            # start_response is the function that is passed as an argument to
            # the WSGI application to receive information about the respose,
            # like headers and status_code.
            # In case of exceptions, start_response may be called multiple
            # times and the last call overrides previous ones. See
            # https://www.python.org/dev/peps/pep-3333/#the-start-response-callable
            # for details.
            def wrapped_start_response(status, response_headers, exc_info=None):
                # Record relevant parameters into the outer variable
                last_exc_info = exc_info[:2] if exc_info else None
                last_response_info[0] = (
                    status, response_headers, last_exc_info)

                # Call original start_response
                return start_response(status, response_headers, exc_info)

            # Put the tracer in the environment, mainly so that the called app
            # can use add_parameter on it if it wants to.
            environ['dynatrace.webrequest_tracer'] = tracer

            # Execute the actual application (it probably calls
            # wrapped_start_response in turn)
            result = self.app(environ, wrapped_start_response)

            # last_response_info should now contain the information from
            # start_response. See the XXX below for cases where we cannot have
            # that information here.
            last_status, last_headers, last_exc_info = last_response_info[0]
            if last_headers:
                for name, value in last_headers: #pylint:disable=not-an-iterable
                    tracer.add_response_header(name, value)
            if last_status is not None:
                tracer.set_status_code(
                    http_status_code_from_phrase_string(last_status))
            if last_exc_info:
                tracer.mark_failed_exc(*last_exc_info)

            # XXX: Result is an iterable of bytestrings. This iterable could do the
            # actual heavy lifting in this webrequest, but we cannot instrument it
            # because the C SDK requires closing the handle on the same thread that
            # created it. However, it is nowhere guaranteed where the server
            # iterates over the result.
            # What is more, start_response may only be called in the first iteration
            # step of the iterable (e.g. if self.app is a generator function,
            # calling it does practically nothing), so in that worst case we get
            # basically ony the information about the incoming data but not
            # about the response (not even how long it really took to generate
            # the response.
            # In that cases, better tracing at risk of potentially reduced
            # performance and higher memory usage could be achieved by replacing
            # the line with `return list(result)`. Note that in the worst case,
            # that replacement may deadlock when the iterable waits for some
            # response before going on and the other side does the same.
            return result

#### Helper functions used internally: ###

def get_remote_address_string(wsgi_environ):
    remote_addr = wsgi_environ.get('REMOTE_ADDR')
    if remote_addr:
        remote_port = wsgi_environ.get('REMOTE_PORT')
        if remote_port:
            pos_colon = remote_addr.find(':')
            if pos_colon < 0: # IPv4
                remote_addr = '{}:{}'.format(remote_addr, remote_port)
            else: # IPv6
                remote_addr = '[{}]:{}'.format(remote_addr, remote_port)
    return remote_addr

def http_status_code_from_phrase_string(status_phrase):
    pos_space = status_phrase.index(' ')
    if pos_space <= 0:
        return int(status_phrase)
    return int(status_phrase[:pos_space])

def get_request_uri(environ):
    return environ.get('REQUEST_URI') or request_uri(environ)

HTTP_PREFIX = 'HTTP_'
HTTP_PREFIX_LEN = len(HTTP_PREFIX)

def cgi_to_http_name(name):
    return name[HTTP_PREFIX_LEN:].replace('_', '-').title()

