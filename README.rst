.. image:: https://circleci.com/gh/righ/d2a.svg?style=svg
  :target: https://circleci.com/gh/righ/d2a

Requirements
============
- Python: 2.7, 3.3, 3.4, 3.5, 3.6 (Tested with 2.7, 3.6)
- Django: 1.9 ~ 2.0 (Tested with 1.11, 2.0)
- SQLAlchemy: 0.9 ~ 1.2 (Tested with 1.2)

Installation
============

.. code:: bash

  $ pip install d2a

Usage
=====

altogether
----------
Example: you make `models_sqla.py` at the same directory which `models.py` has been placed on.

- And write like the following to the `models_sqla.py`

  .. code:: python

     from d2a import transfer
     from . import models
     transfer(models, globals())

  - Example:
    
    - `project_postgresql/books/models_sqla.py <https://github.com/righ/d2a/blob/master/project_postgresql/books/models_sqla.py>`_
    - `project_postgresql/sales/models_sqla.py <https://github.com/righ/d2a/blob/master/project_postgresql/sales/models_sqla.py>`_
    - You can omit specifying `db_type`, then it automatically detects database type from ``settings.DATABASES['default']``.

      - Allowed `db_type` is now `postgresql`, `mysql` and `oracle`,
        the other types will be converted to the following types as ``default`` type: 
        `sqlalchemy/types.py <https://github.com/zzzeek/sqlalchemy/blob/master/lib/sqlalchemy/types.py>`_

That's all, you can import sqlalchemy declaration made from django model.

.. code:: python

  >>> from books import models_sqla
  >>> models_sqla.  # tab completion
  models_sqla.Author(            models_sqla.BookCategory(      models_sqla.CategoryRelation(  models_sqla.transfer(
  models_sqla.Book(              models_sqla.Category(          models_sqla.models
  
  >>> models_sqla.Book
  <class 'd2a.book'>
  
  >>> models_sqla.Book.  # tab completion
  models_sqla.Book.author       models_sqla.Book.content      models_sqla.Book.metadata     models_sqla.Book.tags
  models_sqla.Book.author_id    models_sqla.Book.description  models_sqla.Book.mro(         models_sqla.Book.title
  models_sqla.Book.category     models_sqla.Book.id           models_sqla.Book.price
  # SQL Expression schema
  >>> models_sqla.Book.__table__
  Table(
    'book', MetaData(bind=None), 
    Column('id', UUID(), table=<book>, primary_key=True, nullable=False, default=ColumnDefault(<function uuid4 at 0x7f3cebe7e598>)), 
    Column('price', JSON(astext_type=Text()), table=<book>, nullable=False), 
    Column('title', VARCHAR(length=255), table=<book>, nullable=False), 
    Column('description', TEXT(), table=<book>),
    Column('author_id', INTEGER(), ForeignKey('author.id'), table=<book>), 
    Column('content', BYTEA(), table=<book>, nullable=False), 
    Column('tags', ARRAY(VARCHAR()), table=<book>, nullable=False), 
    schema=None
  )

Also, it can extract model declared implicitly depending on m2m field. (in this case, `BookCategory`)

single
------
If you just want to convert one model, you should use `declare` function.

.. code:: python

  >>> from d2a import declare
  >>> from sales.models import Sales
  >>> sales = declare(Sales)
  >>> sales
  <class 'd2a.sales'>
  
  >>> sales.__table__
  Table(
    'sales', MetaData(bind=None), 
    Column('id', BIGINT(), table=<sales>, primary_key=True, nullable=False), 
    Column('book_id', UUID(), ForeignKey('book.id'), table=<sales>, nullable=False), 
    Column('sold', TIMESTAMP(), table=<sales>, nullable=False), 
    Column('reservation', INTERVAL(), table=<sales>), 
    Column('source', INET(), table=<sales>), 
    schema=None
  )
  
  >>> sales.
  sales.book         sales.id           sales.mro(         sales.sold
  sales.book_id      sales.metadata     sales.reservation  sales.source

Custom fields
-------------
If you are using customized field which is not built-in, you can register the field as the other field using `alias` method.

.. code:: python

  from django.db.models import ImageField
  
  class ExtendedImageField(ImageField):
      """something customizing"""
  
  from d2a import alias
  alias(ExtendedImageField, ImageField)

Demo
============

start up environment
--------------------

.. code-block:: shell

  $ git clone git@github.com:righ/d2a.git
  $ cd d2a
  $ docker-compose up

preparation
--------------------

.. code-block:: shell 

  $ docker exec -it d2a_app_1 /bin/bash
  # python -m venv venv # only first time
  # source venv/bin/activate
  (venv) # cd project_postgresql/ # (or mysql)
  (venv) project_postgresql # ./manage.py migrate

execute
------------

.. code-block:: shell

  (venv) project_postgresql # ./manage.py shell

.. code-block:: python

  >>> from books import models_sqla
  >>> book = models_sqla.Book()
  >>> author = models_sqla.Author()
  >>> book.author = author
  >>> author.books
  [<d2a.book object at 0x7f3cec539358>]
  # And do something you want do ;)

Links
=====
- https://github.com/righ/d2a/
- https://pypi.org/project/d2a/

History
=======
:1.0.2:
  
  - (2018-07-10)
  - Improved a little.

:1.0.1:

  - (2018-07-06)
  - Fixed a bug, that it will be provided `None` even though it does not be specified `default` argument.

:1.0.0:

  - (2018-07-05)
  - Fixed bugs.
  - Added unit tests.

:0.0.6:

  - Fixed a bug that abstract models become the targets.
  - Deleted `install_requires`.

:0.0.5:

  - added alias method.

:0.0.4:

  - fixed bugs.

:0.0.3:

  - it got easy to declare custom field.
  - transfer method can define secondary table.

:0.0.2:

  - it supported m2m field.
  - it limited django version less than `1.9`.

:0.0.1: first release (2017-12-27)
