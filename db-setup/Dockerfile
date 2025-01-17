# Use the official Postgres image as a base image
FROM postgres:17.2

# Set environment variables for Postgres
ENV POSTGRES_USER=demouser
ENV POSTGRES_PASSWORD=secret
ENV POSTGRES_DB=demodb

# Install the build dependencies
USER root
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    postgresql-server-dev-all \
    && rm -rf /var/lib/apt/lists/*

# Clone, build, and install the pgvector extension
RUN cd /tmp \
    && git clone --branch v0.8.0 https://github.com/pgvector/pgvector.git \
    && cd pgvector \
    && make \
    && make install
