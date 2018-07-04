from d2a import transfer
from . import models

transfer(models, globals(), db_type='postgresql')

