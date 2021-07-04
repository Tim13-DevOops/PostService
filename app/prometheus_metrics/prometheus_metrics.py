from flask import request

from prometheus_client import Counter
import logging

logger = logging.getLogger()

counter_404 = Counter(
    "flask_404_counter",
    "Counts number of requests with status code 404 for each endpoint",
    ["service", "endpoint"],
)

counter_ingress = Counter(
    "flask_ingress_counter",
    "Counts the amount of inbound data in the app",
    ["service"],
)


counter_egress = Counter(
    "flask_egress_counter",
    "Counts the amount of outbound data in the app",
    ["service"],
)


def count_size_ingress():
    if request.content_length:
        counter_ingress.labels(service="agent_backend").inc(
            request.content_length / 1024 / 1024
        )


def count_size_egress(response):
    if response.content_length:
        counter_egress.labels(service="agent_backend").inc(
            response.content_length / 1024 / 1024
        )
    return response


def init_metrics():
    from app.app import metrics, app

    metrics.register_default(
        metrics.counter(
            "flask_user_counter",
            "Number of visits by unique users",
            labels={
                "service": lambda: "agent_backend",
                "ip_address": lambda: request.remote_addr,
                "browser": lambda: request.user_agent.browser,
            },
        )
    )

    metrics.register_default(
        metrics.counter(
            "flask_by_endpoint_counter",
            "Number of requests per endpoint",
            labels={
                "service": lambda: "agent_backend",
                "path": lambda: request.path,
                "status_code": lambda response: response.status_code,
            },
        )
    )

    @app.errorhandler(404)
    def page_not_found(e):
        counter_404.labels(service="agent_backend", endpoint=request.path).inc()
        return e, 404

    app.before_request(count_size_ingress)
    app.after_request(count_size_egress)
