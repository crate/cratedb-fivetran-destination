import subprocess
import threading
from textwrap import dedent
from time import sleep

import pytest


def run(command: str, background: bool = False):
    if background:
        return subprocess.Popen(command, shell=True)  # noqa: S602
    subprocess.check_call(command, stderr=subprocess.STDOUT, shell=True)  # noqa: S602
    return None


@pytest.fixture
def services():
    """
    Invoke the CrateDB Fivetran destination gRPC adapter and the Fivetran destination tester.
    """
    processes = []

    oci_image = (
        "us-docker.pkg.dev/build-286712/public-docker-us/sdktesters-v2/sdk-tester:2.25.0131.001"
    )
    run("gcloud auth configure-docker us-docker.pkg.dev")
    run(f"docker pull {oci_image}")

    # Start gRPC server.
    from cratedb_fivetran_destination.main import start_server

    server = None

    def starter():
        nonlocal server
        server = start_server()

    t = threading.Thread(target=starter)
    t.start()

    cmd = dedent(f"""
    docker run --rm \
      --mount type=bind,source=./tests/data,target=/data \
      -a STDIN -a STDOUT -a STDERR \
      -e WORKING_DIR=./tests/data \
      -e GRPC_HOSTNAME=host.docker.internal \
      --network=host \
      --add-host=host.docker.internal:host-gateway \
      {oci_image} \
      --tester-type destination --port 50052
    """)
    processes.append(run(cmd, background=True))
    sleep(6)

    yield

    # Terminate gRPC server.
    server.stop(grace=3.0)

    # Terminate processes again.
    for proc in processes:
        proc.terminate()
        proc.wait(3)


def test_integration(capfd, services):
    """
    Verify the Fivetran destination tester runs to completion.
    """

    # Read out stdout and stderr.
    out, err = capfd.readouterr()

    # "Truncate" is the last software test invoked by the Fivetran destination tester.
    # If the test case receives corresponding log output, it is considered to be complete.
    assert "Create Table succeeded" in err
    assert "Alter Table succeeded" in err
    assert "WriteBatch succeeded" in err
    assert "Truncate succeeded: transaction" in err
