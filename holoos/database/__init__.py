"""
HoloOS Database Module
=======================
Persistence layer with SQL and NoSQL.
"""

from .manager import (
    DatabaseType,
    DatabaseConfig,
    TableSchema,
    SQLDatabase,
    NoSQLDatabase,
    KeyValueStore,
    DatabaseManager,
    get_database,
)

__all__ = [
    "DatabaseType",
    "DatabaseConfig",
    "TableSchema",
    "SQLDatabase",
    "NoSQLDatabase",
    "KeyValueStore",
    "DatabaseManager",
    "get_database",
]