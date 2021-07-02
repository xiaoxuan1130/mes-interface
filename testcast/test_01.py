import pytest

def test_one():
    print("正在执行----test_one")
    x = "this111"
    assert 'h' in x

def test_two():
    print("正在执行----test_two")
    x = "hello"
    assert x

def test_three():
    print("正在执行----test_three")
    a = "hello"
    b = "hello world"
    assert a in b

if __name__ == "__main__":
    pytest.main(["-s", "test_01.py"])