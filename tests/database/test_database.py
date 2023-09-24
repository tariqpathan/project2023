import pytest
from unittest.mock import MagicMock
# from your_module import function_to_test

def test_function_to_test(mocker):
    mocker.patch('your_module.your_db_call', return_value=MagicMock())
    # result = function_to_test()
    # ... your assertions here ...
