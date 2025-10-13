# Stage 1: Build wheel package
FROM python:3.14-slim-bookworm AS build

ARG BUILD=/usr/src

# Configure operating system.
ENV DEBIAN_FRONTEND=noninteractive
ENV TERM=linux

# Install prerequisites.
RUN apt-get update
RUN apt-get --yes install --no-install-recommends --no-install-suggests git wget

# Install package builder.
ENV PIP_ROOT_USER_ACTION=ignore
RUN pip install build
RUN python -m build --version

# Build wheel package.
COPY . ${BUILD}
RUN python -m build --wheel ${BUILD}


FROM python:3.14-slim-bookworm AS package

ARG BUILD=/usr/src

# Configure operating system.
ENV DEBIAN_FRONTEND=noninteractive
ENV TERM=linux

# Configure build environment.
ENV PIP_ROOT_USER_ACTION=ignore
ENV UV_COMPILE_BYTECODE=true
ENV UV_LINK_MODE=copy
ENV UV_PYTHON_DOWNLOADS=never
ENV UV_SYSTEM_PYTHON=true

# Configure runtime environment.
ENV PATH=/root/.local/bin:$PATH

# Provide wheel package.
COPY --from=build ${BUILD}/dist/*.whl /tmp

# Install package.
RUN \
    --mount=type=cache,id=pip,target=/root/.cache/pip \
    --mount=type=cache,id=uv,target=/root/.cache/uv \
    true \
    && pip install uv \
    && uv tool install --upgrade "$(ls /tmp/*.whl)"

# Copy `selftest.sh` to the image.
COPY release/oci/selftest.sh /usr/local/bin

# Run the program by default.
ENTRYPOINT ["cratedb-fivetran-destination"]
