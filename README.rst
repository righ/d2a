it converts a django model to a sqlalchemy declaration.

Requirements
============
- Python 3.6 (not tested)
- Django 1.4 ~ 1.11 (not tested)

Install
=======

.. code:: bash

  $ pip install d2a

Usage
=====
- For example you make `models_sqla.py` at a directory which `models.py` has been placed on.
- And write like the following to the `models_sqla.py`:

  .. code:: python

     from d2a import copy
     from . import models
     copy(models, globals())

- That's all, you can import sqlalchemy declaration made from django model.

  - Example: `demo/models.py` and `demo/models_sqla.py` exist.

  .. code:: python

    >>> from demo import models
    <module 'demo.models' from 'djangomodel2alchemymap/sample/demo/models.py'>
    >>> models.  # tab tab tab -> Test is declared.
    models.Test(   models.models  models.uuid
    >>> from demo import models_sqla
    >>> models_sqla.Test  # Test is declared as sqlalchemy declaration !
    <class 'd2a.alchemy.test_table'>
    >>> models_sqla.Test.__table__  # and got Table ! yatta!
    Table('test_table', MetaData(bind=None), Column('id', CHAR(length=32), table=<test_table>, primary_key=True, nullable=False), Column('no', INTEGER(), table=<test_table>, nullable=False), Column('created', DateTime(), table=<test_table>, nullable=False), Column('updated', DateTime(), table=<test_table>, nullable=False), Column('type', VARCHAR(length=20), table=<test_table>, nullable=False), Column('description', Text(), table=<test_table>), Column('status', VARCHAR(length=10), table=<test_table>), Column('category', VARCHAR(length=255), table=<test_table>), schema=None)

Links
=====
- https://github.com/righ/d2a
