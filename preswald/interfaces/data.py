import logging
from typing import Optional

import pandas as pd

from preswald.engine.service import PreswaldService

from .components import table


# Configure logging
logger = logging.getLogger(__name__)


def connect():
    """
    Connect to all listed data sources in preswald.toml
    """
    try:
        service = PreswaldService.get_instance()
        source_names, duckdb_conn = service.data_manager.connect()
        logger.info(f"Successfully connected to data sources: {source_names}")
        # TODO: bug - getting duplicated if there are multiple clients
        return duckdb_conn
    except Exception as e:
        logger.error(f"Error connecting to datasources: {e}")


def query(sql: str, source_name: str) -> pd.DataFrame:
    """
    Query a data source using sql from preswald.toml by name
    """
    try:
        service = PreswaldService.get_instance()
        df_result = service.data_manager.query(sql, source_name)
        logger.info(f"Successfully queried data source: {source_name}")
        return df_result
    except Exception as e:
        logger.error(f"Error querying data source: {e}")


def get_df(source_name: str, table_name: Optional[str] = None) -> pd.DataFrame:
    """
    Get a dataframe from the named data source from preswald.toml
    If the source is a database/has multiple tables, you must specify a table_name
    """
    try:
        service = PreswaldService.get_instance()
        df_result = service.data_manager.get_df(source_name, table_name)
        logger.info(f"Successfully got a dataframe from data source: {source_name}")
        return df_result
    except Exception as e:
        logger.error(f"Error getting a dataframe from data source: {e}")


def view(df: pd.DataFrame, limit: int = 100):
    """
    Render a preview of the data using the table component.

    Args:
        data_or_connection_name: Either a pandas DataFrame or a connection name string.
        limit (int): Maximum number of rows to display in the table.
    """
    return table(df.head(limit))
