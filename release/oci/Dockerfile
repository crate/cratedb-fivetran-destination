# Stage 1: Build wheel package
FROM python:3.14-slim-bookworm AS build

ARG BUILD=/usr/src

# Enable concurrent multi-arch builds.
# https://github.com/docker/buildx/issues/549#issuecomment-1788297892
ARG TARGETPLATFORM
ARG TARGETOS
ARG TARGETARCH
ARG TARGETVARIANT

# Configure operating system.
ENV DEBIAN_FRONTEND=noninteractive
ENV TERM=linux

# Install the `uv` package manager.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Configure build environment.
ENV PIP_ROOT_USER_ACTION=ignore
ENV UV_COMPILE_BYTECODE=true
ENV UV_LINK_MODE=copy
ENV UV_PYTHON_DOWNLOADS=never
ENV UV_SYSTEM_PYTHON=true

# Install package builder.
RUN \
    --mount=type=cache,id=pip-${TARGETARCH}${TARGETVARIANT},target=/root/.cache/pip \
    --mount=type=cache,id=uv-${TARGETARCH}${TARGETVARIANT},target=/root/.cache/uv \
    true \
    && uv pip install build
RUN python -m build --version

# Build wheel package.
COPY . ${BUILD}
RUN python -m build --wheel ${BUILD}


FROM python:3.14-slim-bookworm AS package

ARG BUILD=/usr/src

# Enable concurrent multi-arch builds.
# https://github.com/docker/buildx/issues/549#issuecomment-1788297892
ARG TARGETPLATFORM
ARG TARGETOS
ARG TARGETARCH
ARG TARGETVARIANT

# Configure operating system.
ENV DEBIAN_FRONTEND=noninteractive
ENV TERM=linux

# Install the `uv` package manager.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

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
    --mount=type=cache,id=pip-${TARGETARCH}${TARGETVARIANT},target=/root/.cache/pip \
    --mount=type=cache,id=uv-${TARGETARCH}${TARGETVARIANT},target=/root/.cache/uv \
    true \
    && uv tool install --upgrade /tmp/*.whl

# Copy `selftest.sh` to the image.
COPY release/oci/selftest.sh /usr/local/bin

# Run the program by default.
ENTRYPOINT ["cratedb-fivetran-destination"]
