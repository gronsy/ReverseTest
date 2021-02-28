import pytest
import city_info_creator
from os.path import exists
import os


def teardown_function():
    text_files_in_dir = os.listdir(".")

    for item in text_files_in_dir:
        if item.endswith(".txt"):
            os.remove(item)


def test_city_summary_request_raises_exception_test():
    url = "https://en.wikipedia.org/api/rest_v1/page/summary/fasdasdds"
    with pytest.raises(NameError):
        city_info_creator.create_request(url, "summary")


def test_city_weather_request_raises_exception_test():
    url = "http://api.openweathermap.org/data/2.5/weather?q=asdaasd&APPID=15bf51e94a29c728f34f933992b31cb2&units=metric"
    with pytest.raises(NameError):
        city_info_creator.create_request(url, "weather")


def test_return_ok_status_code_on_correct_request_weather():
    url = "http://api.openweathermap.org/data/2.5/weather?q=zagreb&APPID=15bf51e94a29c728f34f933992b31cb2&units=metric"
    response = city_info_creator.create_request(url, "weather")
    assert response.status_code == 200


def test_return_ok_status_code_on_correct_request_summary():
    url = "https://en.wikipedia.org/api/rest_v1/page/summary/zagreb"
    response = city_info_creator.create_request(url, "summary")
    assert response.status_code == 200


def test_make_api_calls_creates_output_file():
    city_info_creator.make_api_calls("Zagreb")
    assert exists("Zagreb.txt")
