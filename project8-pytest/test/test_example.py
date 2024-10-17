# validating some type of data
# validate numbers
def test_equal_or_not_equal():
    assert  3 == 3
    assert  3 != 1

# validate instances
def test_instance():
    assert  isinstance('this is a string', str)
    assert  isinstance(10, int)

# validate booleans
def test_boolean():
    validate = True
    assert validate is True
    assert  ('Hello'== 'world') is False

# validate Types
def test_type():
    assert type('hello' is str)
    assert type('world' is not int)

# validate greater than and less than
def test_greater_and_less_than():
    assert 7 > 3
    assert 4 < 10
# validate again types
def test_list():
    num_list = [1,2,3,4,5,6,8,9]
    any_list = [False, False]
    assert 1 in num_list
    assert 7 not in num_list
    assert all(num_list)
    assert  not any(any_list)

