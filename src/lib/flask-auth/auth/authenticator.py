from functools import wraps
from logging import setLoggerClass
from typing import Union
from flask import Flask, request, jsonify, _request_ctx_stack
from urllib.error import URLError
from jwt import decode, PyJWKClient
import jwt.exceptions as jwt_error
from auth.exceptions import *
from auth.utils import get_access_token
from werkzeug.local import LocalProxy


# allows flask applications to access the auth token
auth_token: dict = LocalProxy(lambda:
    getattr(_request_ctx_stack.top, 'auth_token', None)
)


class Authenticator(object):
    '''
    An authenticator for Oauth 2.0 access tokens.

    Attributes:
        issuer: The URL of the openid connect issuer
        audience: The audience of the service
        jwks_client: the JSON Web Key Set client.
        _app_initialized: whether or not the authenticator has been initialized
            with a flask app.
    '''
    issuer: Union[str, None] = None
    audience: Union[str, None] = None
    jwks_client: Union[PyJWKClient, None] = None
    _app_initialized = False


    def __init__(self, app: Flask = None):
        '''
        Creates an access token authenticator for the given flask application.
        If a flask app is provided as a parameter, the authenticator is
        initialized with the app; otherwise, the app is required to be
        initialized later using `Authenticator.init_app()`.

        Args:
            app: A flask application
        '''
        if app is not None:
            self.init_app(app)


    def init_app(self, app: Flask) -> None:
        '''
        Initializes a given flask application for the authenticator.

        Args:
            app: A flask application

        Pre-conditions:
            app != None
            AUTH_ISSUER in app.config
            AUTH_AUDIENCE in app.config
            AUTH_JWKS_URI in app.config

        Post-conditions:
            Registers error handler with app that catches authentication errors
            and returns the appropriate response.
        '''
        assert app != None
        assert 'AUTH_ISSUER' in app.config
        assert 'AUTH_AUDIENCE' in app.config
        assert 'AUTH_JWKS_URI' in app.config

        self.issuer = app.config['AUTH_ISSUER']
        self.audience = app.config['AUTH_AUDIENCE']
        self.jwks_client = PyJWKClient(app.config['AUTH_JWKS_URI'])

        @app.errorhandler(AuthError)
        def handle_pyjwt_error(e: AuthError):
            '''
            Returns a response based on an AuthError that has been raised. This
            function is called when AuthError is raised inside of `app`.
            '''
            body = None
            www_auth = f'Bearer realm="{self.issuer}"'
            if e.error and e.error_description:
                body = {
                    'error': e.error,
                    'error_description': e.error_description
                }
                www_auth += f', error="{e.error}"'
                www_auth += f', error_description="{e.error_description}"'

            return jsonify(body), e.status_code, {'WWW-Authenticate': www_auth}

        @app.errorhandler(URLError)
        def handle_connection_error(e: URLError):
            return {
                'error': 'connection_error',
                'error_description': 'cannot connect to auth provider'
            }, HTTPStatus.INTERNAL_SERVER_ERROR

        self._app_initialized = True


    def require_token(self, func):
        '''
        Decorator that requires that requests to the decorated route provide
        authentication via an access token passed in the Authentication header.

        Args:
            func: the function that require_token decorates

        Pre-conditions:
            flask app is initialized for the authenticator

        Example:
            @app.route('/hello', methods=['POST','GET'])
            @auth.require_auth
            def hello():
            return 'Hello World!'
        '''
        @wraps(func)
        def wrapped_route(*args, **kwargs):
            '''
            The route function that wrapped by require_auth
            '''
            assert self._app_initialized is True
            token = get_access_token(request)
            try:
                signing_key = self.jwks_client.get_signing_key_from_jwt(token)
                data: dict = decode(token,
                    signing_key.key,
                    algorithms=['RS256'],
                    issuer=self.issuer,
                    audience=self.audience,
                )
            except jwt_error.InvalidTokenError as error:
                raise InvalidTokenError(str(error))

            except jwt_error.PyJWKClientError as error:
                raise InvalidTokenError('Key does not match provider')

            except jwt_error.PyJWTError as error:
                raise AuthError()

            _request_ctx_stack.top.auth_token = data
            return func(*args, **kwargs)
        return wrapped_route
