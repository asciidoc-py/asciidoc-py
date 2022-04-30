from asciidoc import set_future_compat, set_legacy_compat
import pytest

@pytest.fixture
def enable_future_compat() -> None:
    set_future_compat()
    yield
    set_legacy_compat()
