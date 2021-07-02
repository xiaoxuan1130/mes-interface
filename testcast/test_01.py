import allure
import pytest

@pytest.fixture(scope="session")
def login():
    print("用例先登录")

@allure.step("步骤1")
def step_1():
    print("111")

@allure.step("步骤2")
def step_2():
    print("222")

@allure.feature("编辑页面")
class TestEditPage():
    '''编辑页面'''

    @allure.story("这是一个xxxx用例")
    def test_1(self,login):
        step_1()
        step_2()
        print("xxxxx")

    @allure.story("这是一个yyy用例")
    def test_2(self,login):
        print("yyy")