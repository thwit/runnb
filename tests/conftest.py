import pytest
from IPython.core.interactiveshell import InteractiveShell


@pytest.fixture(autouse=True)
def _reset_ipython_singleton():
    InteractiveShell.clear_instance()
    yield
    InteractiveShell.clear_instance()
