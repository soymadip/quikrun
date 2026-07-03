import importlib
import pytest

@pytest.mark.parametrize(
    "module",
    [
        "quikrun",
        "quikrun.__main__",
        "quikrun.main",
    ],
)
def test_import(module):
    assert importlib.import_module(module) is not None