from flask import request
from flask_restful import Api
from werkzeug.exceptions import HTTPException
from app.prometheus_metrics.prometheus_metrics import counter_404
from flask.wrappers import Response
import json
import logging

logger = logging.getLogger()


def handle_generic_exception(error):

    response = Response()
    response.data = json.dumps(
        {"code": 500, "name": "Internal server error", "message": f"{error}"}
    )
    response.status_code = 500
    response.content_type = "application/json"
    return response


class CustomApi(Api):
    def __init__(self, *args, **kwargs):
        super(CustomApi, self).__init__(*args, **kwargs)

    def handle_error(self, e):
        if isinstance(e, HTTPException):
            if e.code == 404:
                counter_404.labels(
                    service="agent_backend", endpoint=request.path
                ).inc()

            return super(CustomApi, self).handle_error(e)
        else:
            return handle_generic_exception(e)
