import time
from uuid import uuid4 as uuid


def generate_unique():

    return '{0}_{1}'.format(str(int(time.time())), uuid().hex[:6])
