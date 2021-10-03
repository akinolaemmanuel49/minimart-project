import os
import tempfile

import pytest

from minimart import create_app
from minimart.models import *

@pytest.fixture
def app():
    app = create_app()
    app.config.from_object('minimart.config.TestingConfig')
    return app