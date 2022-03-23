from . import extract_data
from . import data_handler
def test_one():
    data = {'a' : {'a' : 2, 'a' : [{'b' : 2}, {'q' : 3}, {'n' : 4}]}}
    path = 'test_data/fake_event'
    data_handler.log(data, path)
    other_data = data_handler.unlog(path)
    assert data == other_data
