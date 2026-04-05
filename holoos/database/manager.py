"""
HoloOS Database Layer
=====================
Persistence layer with SQL and NoSQL abstractions.
"""

from __future__ import annotations

import logging
import time
import json
from typing import Any, Optional, list
from dataclasses import dataclass, field
from enum import Enum, auto

logger = logging.getLogger(__name__)


class DatabaseType(Enum):
    SQL = auto()
    NOSQL = auto()
    GRAPH = auto()
    TIME_SERIES = auto()


@dataclass
class DatabaseConfig:
    db_type: DatabaseType
    host: str = "localhost"
    port: int = 5432
    database: str = "holoos"
    username: str = ""
    password: str = ""


@dataclass
class TableSchema:
    name: str
    columns: list[dict]
    primary_key: str
    indexes: list[str] = field(default_factory=list)


class SQLDatabase:
    """SQL database abstraction."""

    def __init__(self, config: DatabaseConfig = None) -> None:
        self.config = config or DatabaseConfig(DatabaseType.SQL)
        self._tables: dict[str, TableSchema] = {}
        self._data: dict[str, list[dict]] = {}
        logger.info(f"[SQLDatabase] Initialized: {self.config.database}")

    def create_table(self, schema: TableSchema) -> bool:
        self._tables[schema.name] = schema
        self._data[schema.name] = []
        logger.info(f"[SQLDatabase] Table created: {schema.name}")
        return True

    def insert(self, table: str, data: dict) -> bool:
        if table not in self._data:
            return False
        data["_id"] = len(self._data[table])
        data["_created_at"] = time.time()
        self._data[table].append(data)
        return True

    def select(self, table: str, where: dict = None, limit: int = 100) -> list[dict]:
        if table not in self._data:
            return []
        
        results = self._data[table]
        
        if where:
            results = [r for r in results if all(r.get(k) == v for k, v in where.items())]
        
        return results[:limit]

    def update(self, table: str, where: dict, data: dict) -> int:
        if table not in self._data:
            return 0
        
        count = 0
        for row in self._data[table]:
            if all(row.get(k) == v for k, v in where.items()):
                row.update(data)
                row["_updated_at"] = time.time()
                count += 1
        
        return count

    def delete(self, table: str, where: dict) -> int:
        if table not in self._data:
            return 0
        
        original_len = len(self._data[table])
        self._data[table] = [r for r in self._data[table] if not all(r.get(k) == v for k, v in where.items())]
        return original_len - len(self._data[table])


class NoSQLDatabase:
    """NoSQL document database abstraction."""

    def __init__(self) -> None:
        self._collections: dict[str, dict] = {}
        logger.info("[NoSQLDatabase] Initialized")

    def insert(self, collection: str, document: dict) -> str:
        if collection not in self._collections:
            self._collections[collection] = {}
        
        doc_id = str(time.time()) + "_" + str(len(self._collections[collection]))
        document["_id"] = doc_id
        document["_created_at"] = time.time()
        
        self._collections[collection][doc_id] = document
        return doc_id

    def get(self, collection: str, doc_id: str) -> Optional[dict]:
        if collection in self._collections:
            return self._collections[collection].get(doc_id)
        return None

    def find(self, collection: str, query: dict = None, limit: int = 100) -> list[dict]:
        if collection not in self._collections:
            return []
        
        docs = list(self._collections[collection].values())
        
        if query:
            docs = [d for d in docs if all(d.get(k) == v for k, v in query.items())]
        
        return docs[:limit]

    def update(self, collection: str, doc_id: str, data: dict) -> bool:
        if collection in self._collections and doc_id in self._collections[collection]:
            self._collections[collection][doc_id].update(data)
            self._collections[collection][doc_id]["_updated_at"] = time.time()
            return True
        return False

    def delete(self, collection: str, doc_id: str) -> bool:
        if collection in self._collections and doc_id in self._collections[collection]:
            del self._collections[collection][doc_id]
            return True
        return False


class KeyValueStore:
    """Key-value store (Redis-style)."""

    def __init__(self) -> None:
        self._store: dict[str, tuple[Any, float]] = {}
        logger.info("[KeyValueStore] Initialized")

    def set(self, key: str, value: Any, ttl: int = None) -> None:
        expiry = time.time() + ttl if ttl else None
        self._store[key] = (value, expiry)

    def get(self, key: str) -> Optional[Any]:
        if key in self._store:
            value, expiry = self._store[key]
            if expiry is None or time.time() < expiry:
                return value
            del self._store[key]
        return None

    def delete(self, key: str) -> bool:
        if key in self._store:
            del self._store[key]
            return True
        return False

    def exists(self, key: str) -> bool:
        return self.get(key) is not None

    def keys(self, pattern: str = "*") -> list[str]:
        return list(self._store.keys())

    def increment(self, key: str, amount: int = 1) -> int:
        current = int(self.get(key) or 0)
        new_value = current + amount
        self.set(key, new_value)
        return new_value


class DatabaseManager:
    """Unified database manager."""

    def __init__(self) -> None:
        self.sql = SQLDatabase()
        self.nosql = NoSQLDatabase()
        self.kv = KeyValueStore()
        
        self._init_default_tables()
        
        logger.info("[DatabaseManager] Initialized")

    def _init_default_tables(self) -> None:
        self.sql.create_table(TableSchema(
            name="users",
            columns=[{"name": "username", "type": "string"}, {"name": "email", "type": "string"}],
            primary_key="id",
        ))
        
        self.sql.create_table(TableSchema(
            name="sessions",
            columns=[{"name": "user_id", "type": "int"}, {"name": "token", "type": "string"}],
            primary_key="id",
        ))

    def get_stats(self) -> dict:
        return {
            "sql_tables": len(self.sql._tables),
            "sql_records": sum(len(v) for v in self.sql._data.values()),
            "nosql_collections": len(self.nosql._collections),
            "kv_keys": len(self.kv._store),
        }


_db_manager: Optional[DatabaseManager] = None


def get_database() -> DatabaseManager:
    global _db_manager
    if _db_manager is None:
        _db_manager = DatabaseManager()
    return _db_manager


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