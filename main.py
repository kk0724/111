import random
from time import localtime
from requests import get, post
from datetime import datetime, date
from zhdate import ZhDate
import sys
import os

def get_color():
    # 获取随机颜色
    def get_colors(n):
        return ["#" + "%06x" % random.randint(0, 0xFFFFFF) for _ in range(n)]
    color_list = get_colors(100)
    return random.choice(color_list)

def get_access_token():
    app_id = config["app_id"]
    app_secret = config["app_secret"]
    post_url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={app_id}&secret={app_secret}"
    try:
        response = get(post_url).json()
        access_token = response['access_token']
    except KeyError:
        print("获取access_token失败，请检查app_id和app_secret是否正确")
        sys.exit(1)
    return access_token

def get_weather(region):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    key = config["weather_key"]
    region_url = f"https://geoapi.qweather.com/v2/city/lookup?location={region}&key={key}"
    response = get(region_url, headers=headers).json()
    if response["code"] != "200":
        print(f"地区信息请求失败，错误码：{response['code']}")
        sys.exit(1)
    location_id = response["location"][0]["id"]
    weather_url = f"https://devapi.qweather.com/v7/weather/now?location={location_id}&key={key}"
    response = get(weather_url, headers=headers).json()

    if "now" not in response:
        print("天气信息API返回的数据中缺少 'now' 字段")
        input("Press enter to continue")
        sys.exit(1)

    weather = response["now"]["text"]
    temp = response["now"]["temp"] + u"\N{DEGREE SIGN}" + "C"
    wind_dir = response["now"]["windDir"]
    return weather, temp, wind_dir

# 此处省略其他函数定义 ...

if __name__ == "__main__":
    try:
        with open("config.txt", encoding="utf-8") as f:
            config = eval(f.read())
    except FileNotFoundError:
        print("请检查config.txt文件是否与程序位于同一路径")
        sys.exit(1)
    except SyntaxError:
        print("请检查配置文件格式是否正确")
        sys.exit(1)

    accessToken = get_access_token()
    users = config["user"]
    region = config["region"]
    weather, temp, wind_dir = get_weather(region)
    # 此处省略其他变量赋值 ...

    for user in users:
        send_message(user, accessToken, region, weather, temp, wind_dir, note_ch, note_en)
    input("Press enter to continue")
