import pytest

from repository.interface import MedsRepoProto


@pytest.fixture
def repository() -> MedsRepoProto:
    yield MedsRepoProto()
