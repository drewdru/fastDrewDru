import logging
import os
import sys

import pytest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
logger = logging.getLogger(__name__)

from fastDrewDru.db import get_db_service  # noqa


@pytest.fixture(autouse=True)
async def connect_db():
    """Connect to databse before tests."""
    # Setup : start db
    db_service = get_db_service()
    await db_service.db.connect()

    yield  # run tests

    # Teardown : stop db
    await db_service.db.disconnect()
