# coding: utf-8
import logging
from collections import OrderedDict
from contextlib import contextmanager

from sqlalchemy.orm import sessionmaker
from sqlalchemy import dialects, create_engine
from django.conf import settings
from django.db import transaction

from .compat import basestring

DIALECTS = {
    t: getattr(dialects, t).dialect
    for t in ['postgresql', 'mysql', 'oracle', 'mssql', 'sqlite', 'firebase']
    if hasattr(dialects, t)
}

logger = logging.getLogger(__name__)


def _detect_db_type(database='default'):
    return {
        'django.db.backends.postgresql': 'postgresql',
        'django.db.backends.postgresql_psycopg2': 'postgresql',
        'django.db.backends.mysql': 'mysql',
        'django.db.backends.oracle': 'oracle',
        # 'django.db.backends.sqlite3': 'sqlite3',
    }.get(settings.DATABASES[database]['ENGINE'])


def _execute_cursor(cursor, sql, params):
    try:
        cursor.execute(sql, params)
    except Exception:
        logger.exception('param:%s\nsql:%s', params, sql)


def _complement(conn, dialect=None):
    if not conn:
        conn = transaction.get_connection()
    if not dialect:
        dialect = AUTO_DETECTED_DB_TYPE
    if isinstance(dialect, basestring):
        dialect = DIALECTS[dialect]

    return conn, dialect


def query_expression(stmt, conn=None, dialect=None):
    conn, dialect = _complement(conn, dialect)
    with conn.cursor() as cursor:
        _execute_cursor(cursor, str(stmt), stmt.params)
        return [
            OrderedDict(zip([c.name for c in stmt.c], row))
            for row in cursor
        ]


def execute_expression(stmt, conn=None, dialect=None):
    conn, dialect = _complement(conn, dialect)
    stmt = stmt.compile(dialect=dialect())
    with conn.cursor() as cursor:
        _execute_cursor(cursor, str(stmt), stmt.params)
        return cursor.rowcount


def make_engine(db_type=None, database='default', encoding='utf', echo=False):
    ms_dsn = 'DRIVER={{SQL Server}}; SERVER={HOST}; DATABASE={NAME}; UID={USER}; PWD={PASSWORD}'
    uri = {
        'postgresql': 'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}',
        'postgresql+psycopg2': 'postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}', 
        'mysql': 'mysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}',
        'mysql+mysqldb': 'mysql+mysqldb://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}',
        'oracle': 'oracle://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}', 
        'oracle+cx_oracle': 'oracle+cx_oracle://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}',
        'mssql': 'mssql://{USER}:{PASSWORD}@' + ms_dsn,
        'mssql+pyodbc': 'mssql+pyodbc://{USER}:{PASSWORD}@' + ms_dsn,
        'mssql+adodbapi': 'mssql+adodbapi://{USER}:{PASSWORD}@' + ms_dsn,
        'mssql+pymssql': 'mssql+pymssql://{USER}:{PASSWORD}@' + ms_dsn,
        'sqlite': 'sqlite:///{NAME}',
        'sqlite+memory': 'sqlite://',
    }[db_type or _detect_db_type(database)]
    return create_engine(
        uri.format(**settings.DATABASES[database]),
        encoding=encoding, echo=echo)


@contextmanager
def make_session(engine=None):
    if not engine:
        engine = make_engine()
    Session = sessionmaker(engine)
    session = Session()
    try:
        yield session
    finally:
        session.close()


AUTO_DETECTED_DB_TYPE = _detect_db_type()
