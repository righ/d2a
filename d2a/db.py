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

MS_DSN = 'DRIVER={{SQL Server}}; SERVER={HOST}; DATABASE={NAME}; UID={USER}; PWD={PASSWORD};'

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


def _complement(conn, dialect, database='default'):
    if not conn:
        conn = transaction.get_connection()
    if not dialect:
        dialect = _detect_db_type(database)
    if isinstance(dialect, basestring):
        dialect = DIALECTS[dialect]

    return conn, dialect


def query_expression(stmt, conn=None, dialect=None, database='default'):
    conn, dialect = _complement(conn, dialect, database)
    with conn.cursor() as cursor:
        _execute_cursor(cursor, str(stmt), stmt.params)
        return [
            OrderedDict(zip([c.name for c in stmt.c], row))
            for row in cursor
        ]


def execute_expression(stmt, conn=None, dialect=None, database='default'):
    conn, dialect = _complement(conn, dialect, database)
    stmt = stmt.compile(dialect=dialect())
    with conn.cursor() as cursor:
        _execute_cursor(cursor, str(stmt), stmt.params)
        return cursor.rowcount


def make_engine(db_type=None, database='default', encoding='utf8', echo=False):
    uri = {
        'postgresql': 'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}',
        'postgresql+psycopg2': 'postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}', 
        'mysql': 'mysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}',
        'mysql+mysqldb': 'mysql+mysqldb://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}',
        'oracle': 'oracle://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}',
        'oracle+cx_oracle': 'oracle+cx_oracle://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}',
        'mssql': 'mssql://{USER}:{PASSWORD}@' + MS_DSN,
        'mssql+pyodbc': 'mssql+pyodbc://{USER}:{PASSWORD}@' + MS_DSN,
        'mssql+adodbapi': 'mssql+adodbapi://{USER}:{PASSWORD}@' + MS_DSN,
        'mssql+pymssql': 'mssql+pymssql://{USER}:{PASSWORD}@' + MS_DSN,
        'sqlite': 'sqlite:///{NAME}',
        'sqlite3': 'sqlite:///{NAME}',
        'sqlite+memory': 'sqlite://',
    }[db_type or _detect_db_type(database)]
    return create_engine(
        uri.format(**settings.DATABASES[database]),
        encoding=encoding, echo=echo)


@contextmanager
def make_session(engine=None,
                 autoflush=True, autocommit=False,
                 expire_on_commit=True, info=None
):
    if not engine:
        engine = make_engine()
    Session = sessionmaker(engine,
                           autoflush=autoflush, autocommit=autocommit,
                           expire_on_commit=expire_on_commit, info=info)
    session = Session()
    try:
        yield session
    finally:
        if not autoflush:
            session.flush()
        if not autocommit:
            session.commit()
        session.close()


AUTO_DETECTED_DB_TYPE = _detect_db_type()
