"""
Logging configuration.
"""

import logging
import os

from hyperdx.opentelemetry import configure_opentelemetry
from hyperdx.opentelemetry.options import HyperDXOptions
from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import (
    OTLPLogExporter as GRPCOTLPLogExporter,
)
from opentelemetry.exporter.otlp.proto.http._log_exporter import (
    OTLPLogExporter as HTTPOTLPLogExporter,
)
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import ConsoleLogExporter, SimpleLogRecordProcessor


def _configure_hyperdx_logs(options: HyperDXOptions) -> None:
    logger_provider = LoggerProvider()

    if options.logs_exporter_protocol == "grpc":
        exporter = GRPCOTLPLogExporter(
            endpoint=options.get_logs_endpoint(),
            credentials=options.get_logs_endpoint_credentials(),
            headers=options.get_logs_headers(),
        )
    else:
        exporter = HTTPOTLPLogExporter(
            endpoint=options.get_logs_endpoint(),
            headers=options.get_logs_headers(),
        )

    set_logger_provider(logger_provider)
    logger_provider.add_log_record_processor(SimpleLogRecordProcessor(exporter))
    # Console exporter helps verify that logs are emitted at all.
    logger_provider.add_log_record_processor(
        SimpleLogRecordProcessor(ConsoleLogExporter())
    )

    handler = LoggingHandler(level=logging.NOTSET, logger_provider=logger_provider)
    logging.getLogger().addHandler(handler)


def setup_logging():
    # TODO 1: Set up basic logging with level INFO using logging.basicConfig()
    api_key = os.getenv("HYPERDX_API_KEY")

    options = HyperDXOptions(
        service_name="churn-prediction-api",
        apikey=api_key,
    )

    # Configure trace/metrics with HyperDX defaults.
    configure_opentelemetry(options)

    # Override log pipeline to use SimpleLogRecordProcessor.
    _configure_hyperdx_logs(options)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # TODO 2: Create a named logger using logging.getLogger() and return it
    logger = logging.getLogger(__name__)
    logger.info("HyperDX logging configured")
    return logger
