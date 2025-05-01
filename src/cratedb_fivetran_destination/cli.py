import logging

import click

from cratedb_fivetran_destination.main import start_server
from cratedb_fivetran_destination.util import setup_logging

logger = logging.getLogger()


@click.command()
@click.version_option()
@click.pass_context
@click.option("--port", "-p", type=int, default=50052, help="Port to listen on. Default: 50052")
@click.option(
    "--max-workers",
    "-w",
    type=int,
    default=1,
    help="The maximum number of threads that can be used. Default: 1",
)
def main(ctx: click.Context, port: int, max_workers: int) -> None:
    """
    Start Fivetran CrateDB Destination gRPC server.

    The executable needs to do the following:

    - Accept a --port argument that takes an integer as a port number to listen to.
    - Listen on both IPV4 (i.e. 0.0.0.0) and IPV6 (i.e ::0), but if only one is possible,
      it should listen on IPV4.

    -- https://github.com/fivetran/fivetran_sdk/blob/main/development-guide.md#command-line-arguments
    """
    setup_logging()
    server = start_server(port=port, max_workers=max_workers)
    logger.info(f"Fivetran CrateDB Destination gRPC server started on port {port}")
    server.wait_for_termination()
    logger.info("Fivetran CrateDB Destination gRPC server terminated")
