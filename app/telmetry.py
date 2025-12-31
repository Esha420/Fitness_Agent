# app/telemetry.py
from contextlib import contextmanager
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource

_tracer = None


def init_otel():
    global _tracer
    if _tracer:
        return _tracer

    resource = Resource(attributes={
        SERVICE_NAME: "fitness-ai-tool",
        "deployment.environment": "demo"
    })

    provider = TracerProvider(resource=resource)
    processor = BatchSpanProcessor(
        OTLPSpanExporter(
            endpoint="http://localhost:4317",
            insecure=True
        )
    )
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)

    _tracer = trace.get_tracer("fitness-ai-tool")
    return _tracer


def get_current_trace_id() -> str:
    span = trace.get_current_span()
    ctx = span.get_span_context()
    return format(ctx.trace_id, "032x") if ctx.trace_id else ""


@contextmanager
def trace_span(span: str, user_id: str, metadata: dict | None = None):
    tracer = init_otel()

    with tracer.start_as_current_span(span) as s:
        s.set_attribute("user.id", user_id)
        s.set_attribute("app.layer", "application")

        if metadata:
            for k, v in metadata.items():
                s.set_attribute(f"custom.{k}", str(v))

        try:
            yield s
        except Exception as e:
            s.record_exception(e)
            s.set_status(Status(StatusCode.ERROR, str(e)))
            raise
