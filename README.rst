.. image:: https://circleci.com/gh/righ/d2a.svg?style=svg
  :target: https://circleci.com/gh/righ/d2a

Requirements
============
- Python: 2.7.15 or later, 3.4 or later.

  - Tested with 2.7.15, 3.6

- Django: 1.9 or later.
  
  - Tested with 1.11, 2.0, 2.1

- SQLAlchemy: 0.9 or later.

  - Tested with 1.2

Installation
============

.. code:: bash

  $ pip install d2a

Usage
=====

Auto loading
------------
Just add `d2a` to ``settings.INSTALLED_APPS``.

.. code-block:: python

  INSTALLED_APPS = [
      'django.contrib.admin',
      'django.contrib.auth',
      'django.contrib.contenttypes',
      'django.contrib.sessions',
      'django.contrib.messages',
      'django.contrib.staticfiles',
  
      # top or here
      'd2a',

      # example apps
      'books',
      'sales',
  ]

.. warning::

  Put it before apps you made as much as possible.
  Because it wants to register alchemy model before the other ``apps.py``.

Then `models_sqla` (default) in all apps become possible to be imported as a module.

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

Also, it can extract model declared implicitly depending on m2m field.
(in this case, `BookCategory`)

.. note::

  You can set configrations to ``settings.py``.

  Example:

  .. code-block:: python

    # This variable can be omitted.
    D2A_CONFIG = {
        'AUTOLOAD': { # optional
            # module name: It can be used different module name from `models_sqla`.
            'module': 'modelsa',  # optional, default: 'models_sqla'
            # transfer function's args after 'exports' arg.
            'option': {  # optional
                'db_type': 'postgresql',  # default: 'default'
                'back_type': 'backref',  # default: 'backref'
                'as_table': True,  # default: False
                'name_formatter': str.upper,  # default: get_camelcase
            }
        },
        # converting rules for customized fields
        'ALIASES': {  # optional
            # Evaluates ExtendedImageField as ImageField
            ExtendedImageField: models.ImageField,
        },
    }


Per models module
-----------------
If you want to create a module manually, create a `models_sqla.py` in the apps.

Write like the following to it`:

.. code:: python

   from d2a import transfer
   from . import models
   transfer(models, globals())

`models_sqla.py` exists, auto module creation will be omitted.

And if you create every `models_sqla.py` manually,
it is unnecessary to set `d2a` to ``settings.INSTALLED_APPS``.

Example:

- `project_postgresql/books/models_sqla.py <https://github.com/righ/d2a/blob/master/project_postgresql/books/models_sqla.py>`_
- You can omit specifying `db_type`, then it automatically detects a database type from ``settings.DATABASES['default']``.

  - Now `postgresql`, `mysql` and `oracle` are allowed,
    the other types will be converted to the following types as ``default`` type: 
    `sqlalchemy/types.py <https://github.com/zzzeek/sqlalchemy/blob/master/lib/sqlalchemy/types.py>`_

Per model
---------
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
If you are using customized field not built-in,
you can register the field as the other field using `alias` or `alias_dict` method.

.. code:: python

  from django.db.models import ImageField
  
  class ExtendedImageField(ImageField):
      """something customizing"""
  
  from d2a import alias
  alias(ExtendedImageField, ImageField)

  # or
  alias_dict({
    ExtendedImageField: ImageField,
  })

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
:1.1.x:

  - (2019-02-17)
  - Added a function to load all models automatically.

:1.0.2:
  
  - (2018-07-10)
  - Improved a little.

:1.0.1:

  - (2018-07-06)
  - Fixed a bug, that it will be provided `None` even though it's not specified `default` argument.

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
