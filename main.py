import requests
import pytest
from datetime import datetime
from datetime import timedelta

######################### API response ##########################
get_api_url = "https://samples.openweathermap.org/data/2.5/forecast/hourly?q=London,us&appid=b6907d289e10d714a6e88b30761fae22"
response = requests.get(get_api_url)
content = response.json()     # response output in form of dictionary

########################### common lists and dictionary #####################
try:
    if content.get("list"):
        content_list = content["list"]   # list containing response details

    dt_text = []    # list for date time info
    for item in content_list:
        if item.get("dt_txt"):
            dt_text.append(item["dt_txt"])
    time_dic = {}  # dictionary for date time info
    for dt in dt_text:
        temp = dt.split(" ")
        if time_dic.get(temp[0]):
            time_dic[temp[0]].append(dt)
        else:
            time_dic[temp[0]] = [dt]
except Exception as e:
    print("The required values were not fetched from the API response",e)

####################### testcases ############################
def test_number_of_days():
    date_lis = []
    for dt in dt_text:
        temp = dt.split(" ")
        if temp[0] in date_lis:
            pass
        else:
            date_lis.append(temp[0])
    msg = "The data collected is for more than 4 days.It is collected for {} days".format(len(date_lis))
    assert len(date_lis)==4,msg

@pytest.mark.parametrize("key",[key for key in time_dic.keys()])
def test_check_time_difference(key):
    lis = time_dic[key]
    time_start = datetime.strptime(lis[0],'%Y-%m-%d %H:%M:%S')
    time_diff = timedelta(hours=1)
    print(time_diff)
    flag = True
    for i in range(1,len(lis)):
        temp = datetime.strptime(lis[i], '%Y-%m-%d %H:%M:%S')
        if (temp - time_start) == time_diff:
            time_start = temp
        else:
            flag = False
    assert flag == True


def test_verify_temperature():
    temperature_not_in_range_list = []
    for item in content_list:
        if item.get("dt_txt"):
            date = item["dt_txt"]
        if item.get("main"):
            temp = item["main"]["temp"]
            min_temp = item["main"]["temp_min"]
            max_temp = item["main"]["temp_max"]
            if not (temp>=min_temp and temp<=max_temp):
                temperature_not_in_range_list.append(date)
    msg = "The temperature at this date and time was not in range" , temperature_not_in_range_list
    assert len(temperature_not_in_range_list)==0,msg


def test_verify_description_for_weatherid_500():
    for item in content_list:
        if item["weather"][0]["id"]==500:
            assert item["weather"][0]["description"] == "light rain"


def test_verify_description_for_weatherid_800():
    for item in content_list:
        if item["weather"][0]["id"]==800:
            assert item["weather"][0]["description"] == "clear sky"
