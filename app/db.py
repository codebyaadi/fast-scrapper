import logging
from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster, Session
from cassandra.cqlengine.connection import register_connection, set_default_connection
from astrapy import DataAPIClient, Database
from .core.config import get_settings

settings = get_settings()


def get_cluster() -> Cluster:
    """
    Create and return a Cassandra Cluster object using credentials from environment variables.
    """
    try:
        cloud_config = {"secure_connect_bundle": settings.ASTRA_DB_BUNDLE_PATH}
        if not cloud_config["secure_connect_bundle"]:
            raise ValueError("ASTRA_DB_BUNDLE_PATH environment variable is missing.")

        auth_provider = PlainTextAuthProvider("token", settings.ASTRA_DB_TOKEN)

        # Create and return a cluster
        cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
        logging.info("Successfully created a cluster connection.")
        return cluster
    except Exception as e:
        logging.error(f"Error creating cluster: {e}")
        raise


def get_session() -> Session:
    """
    Establish and return a Cassandra session.
    """
    try:
        cluster = get_cluster()
        session = cluster.connect()
        register_connection(str(session), session=session)
        set_default_connection(str(session))
        logging.info("Session created successfully.")
        return session
    except Exception as e:
        logging.error(f"Error creating session: {e}")
        raise


def get_database() -> Database:
    """
    Connects to a DataStax Astra database.
    This function retrieves the database endpoint and application token from the
    environment variables `ASTRA_DB_API_ENDPOINT` and `ASTRA_DB_APPLICATION_TOKEN`.

    Returns:
        Database: An instance of the connected database.

    Raises:
        RuntimeError: If the environment variables `ASTRA_DB_API_ENDPOINT` or
        `ASTRA_DB_TOKEN` are not defined.
    """
    endpoint = settings.ASTRA_DB_API_ENDPOINT
    token = settings.ASTRA_DB_TOKEN

    if not token or not endpoint:
        raise RuntimeError(
            "ASTRA_DB_API_ENDPOINT and ASTRA_DB_TOKEN environment variable is missing."
        )

    client = DataAPIClient(token)

    database = client.get_database(endpoint)

    logging.info(f"Connected to database {database.info().name}")

    return database
