it converts a django model to a sqlalchemy declaration.

Requirements
============
- Python: ? (not tested)
- Django: 1.9 ~ 2.0 (not tested)
- SQLAlchemy: 0.9 ~ 1.2 (not tested)

Installation
============

.. code:: bash

  $ pip install d2a

Usage
=====

altogether
----------
Example: you make `models_sqla.py` at a directory which `models.py` has been placed on.

- And write like the following to the `models_sqla.py`:

  .. code:: python

     from d2a import transfer
     from . import models
     transfer(models, globals())

- That's all, you can import sqlalchemy declaration made from django model.

  - Example: `demo/models.py <https://github.com/righ/d2a/blob/master/sample/demo/models.py>`_ and `demo/models_sqla.py <https://github.com/righ/d2a/blob/master/sample/demo/models_sqla.py>`_ exist.

  .. code:: python

    >>> from demo import models
    >>> models.  # tab completion
    models.Author(            models.Category(          models.Sales(             models.uuid
    models.Book(              models.CategoryRelation(  models.models

    >>> models.Book
    <class 'demo.models.Book'>
    >>> models.Book.  # tab completion
    models.Book.DoesNotExist(             models.Book.delete(                   models.Book.price
    models.Book.MultipleObjectsReturned(  models.Book.description               models.Book.refresh_from_db(
    models.Book.add_to_class(             models.Book.from_db(                  models.Book.sales
    models.Book.author                    models.Book.full_clean(               models.Book.save(
    models.Book.author_id                 models.Book.get_deferred_fields(      models.Book.save_base(
    models.Book.category                  models.Book.id                        models.Book.serializable_value(
    models.Book.check(                    models.Book.mro(                      models.Book.title
    models.Book.clean(                    models.Book.objects                   models.Book.unique_error_message(
    models.Book.clean_fields(             models.Book.pk                        models.Book.validate_unique(

    >>> from demo import models_sqla
    >>> models_sqla.  # tab completion
    models_sqla.Author(            models_sqla.BookCategory(      models_sqla.CategoryRelation(  models_sqla.models
    models_sqla.Book(              models_sqla.Category(          models_sqla.Sales(             models_sqla.transfer(   models_sqla.Book(              models_sqla.CategoryRelation(  models_sqla.models

    >>> models_sqla.Book
    <class 'd2a.alchemy.book'>
    >>> models_sqla.Book.  # tab completion
    models_sqla.Book.author_id    models_sqla.Book.description  models_sqla.Book.metadata     models_sqla.Book.price
    models_sqla.Book.category     models_sqla.Book.id           models_sqla.Book.mro(         models_sqla.Book.title
    
single
------
You should write like the following:

  .. code:: python

    >>> from d2a import declare
    >>> from demo.models import Sales
    >>> sales = declare(Sales)
    >>> sales
    <class 'd2a.alchemy.sales'>
    >>> sales.__table__
    Table('sales', MetaData(bind=None), Column('id', BIGINT(), table=<sales>, primary_key=True, nullable=False), Column('book_id', CHAR(length=32), ForeignKey('book.id'), table=<sales>), Column('sold', DateTime(), table=<sales>), schema=None)

Custom fields
-------------
If you are using customized field which is not built-in, you can register the field as the other field using `alias` method.

.. code:: python

  from django.db.models import ImageField
  
  class ExtendedImageField(ImageField):
      """something customizing"""
  
  from d2a import alias
  alias(ExtendedImageField, ImageField)


Links
=====
- https://github.com/righ/d2a

History
=======
:0.0.1: first release (2017-12-27)
:0.0.2:

  - it supported m2m field.
  - it limited django version less than `1.9`.

:0.0.3:

  - it got easy to declare custom field.
  - transfer method can define secondary table.

:0.0.4:

  - fixed bugs.

:0.0.5:

  - added alias method.

:0.0.6:

  - Fixed a bug that abstract model become the target.
  - Deleted `install_requires`.
