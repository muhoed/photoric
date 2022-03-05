from photoric import create_app

def test_test_config():
    """
    GIVEN Photoric application create by app factory function
    WHEN test environment type is submitted
    THEN check that environment is 'development' and testing is on
    """
    assert create_app("test").testing
    assert create_app("test").env == 'development'