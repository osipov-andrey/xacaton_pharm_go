import pytest

from repository.interface import MedsRepoProto
from repository.local_repo import MedsRepoLocal


@pytest.fixture
def repository() -> MedsRepoProto:
    yield MedsRepoLocal()
