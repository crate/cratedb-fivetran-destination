import logging
import shlex
import subprocess
from pathlib import Path

import click

from cratedb_fivetran_destination.util import setup_logging

logger = logging.getLogger()


SDK_TESTER_OCI = (
    "us-docker.pkg.dev/build-286712/public-docker-us/sdktesters-v2/sdk-tester:2.25.1118.001"
)


@click.command()
@click.option(
    "--directory",
    "-h",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True, path_type=Path),
    required=True,
    help="Directory containing test data",
)
def cli(directory: Path) -> None:
    setup_logging()
    logger.info(f"Starting Fivetran SDK tester on directory: {directory}")
    command = f"""
    docker run --rm
        --mount type=bind,source="{directory}",target=/data
        -a STDIN -a STDOUT -a STDERR
        -e WORKING_DIR="{directory}"
        -e GRPC_HOSTNAME=host.docker.internal
        --network=host
        --add-host=host.docker.internal:host-gateway
        {SDK_TESTER_OCI}
        --tester-type destination
        --port 50052
    """
    subprocess.check_call(shlex.split(command.strip()))  # noqa: S603
