from .peeweext import Peeweext
from .mailgunext import Mailgunext
from .celeryext import Celeryext

pwx = Peeweext()
mailext = Mailgunext()
celeryapp = Celeryext()
