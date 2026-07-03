import quikrun

def test_has_version():
    assert isinstance(quikrun.__version__, str)
    assert quikrun.__version__