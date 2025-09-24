import requests
import datetime
import os
import sys

# 读取环境变量
WEBHOOK = os.environ.get("DINGTALK_WEBHOOK")
DUTY1_PHONE = os.environ.get("DUTY1_PHONE")
DUTY2_PHONE = os.environ.get("DUTY2_PHONE")
DUTY3_PHONE = os.environ.get("DUTY3_PHONE")

# 检查必要环境变量是否存在
if not WEBHOOK:
    print("错误：未配置 DINGTALK_WEBHOOK")
    sys.exit(1)
if not all([DUTY1_PHONE, DUTY2_PHONE, DUTY3_PHONE]):
    print("错误：未配置全部 DUTY_PHONE 环境变量")
    sys.exit(1)

# 值班人员列表（自定义名字 + 手机号来自 Secrets）
duty_list = [
    {"name": "文佳", "at": DUTY1_PHONE},
    {"name": "雨芃", "at": DUTY2_PHONE},
    {"name": "楷祥", "at": DUTY3_PHONE},
]

today = datetime.date.today()

# 周末不发送
if today.weekday() >= 5:
    print("周末，不发送值班提醒。")
    sys.exit(0)

# 计算从某个起点以来的工作日数（周末不占用顺序）
start_date = datetime.date(2025, 1, 1)
workdays = 0
day = start_date
while day <= today:
    if day.weekday() < 5:
        workdays += 1
    day += datetime.timedelta(days=1)

# 轮到谁值班
index = (workdays - 1) % len(duty_list)
person = duty_list[index]

# 构造消息
# msg_text = f"值班提醒：今天由 {person['name']} 老师值班！\n需求链接https://alidocs.dingtalk.com/i/nodes/QG53mjyd80RjzmmdfQdwzwmwV6zbX04v?corpId=ding5b97e5f7d1c55821ee0f45d8e4f7c288&utm_medium=im_card&iframeQuery=viewId%3Dlw0u8qogyn1y35l3ebvo2%26utm_medium%3Dim_card%26sheetId%3Dqvrb8hhpw4v8n5wvuwito%26entrance%3Ddata%26utm_source%3Dim&utm_scene=person_space&utm_source=im"

#data = {
#    "msgtype": "text",
#    "text": {"content": msg_text},
#    "at": {
#        "atMobiles": [person["at"]],
#        "isAtAll": False
#    },
#}

# 消息1 
full_url = "https://alidocs.dingtalk.com/i/nodes/QG53mjyd80RjzmmdfQdwzwmwV6zbX04v?corpId=ding5b97e5f7d1c55821ee0f45d8e4f7c288&utm_medium=im_card&iframeQuery=viewId%3Dlw0u8qogyn1y35l3ebvo2%26utm_medium%3Dim_card%26sheetId%3Dqvrb8hhpw4v8n5wvuwito%26entrance%3Ddata%26utm_source%3Dim&utm_scene=person_space&utm_source=im"

data_link = {
    "msgtype": "link",
    "link": {
        "title": f"值班提醒：今天由 {person['name']} 老师值班！",  # 卡片标题
        "text": "【新需求】点击查看 AI 表格数据需求。",  # 卡片摘要
        "messageUrl": full_url  # 点击卡片后的跳转链接
    },
}


# 发送消息 1 (Link Card)
res_link = requests.post(WEBHOOK, json=data_link)
print(f"Link 消息发送结果: {res_link.text}")


# 消息 2: Text 消息体，内容简洁，只为触发 @人 提醒
at_text = f"@{person['name']} 请查看上方链接中的今日值班新需求！"

data_at = {
    "msgtype": "text",
    "text": {"content": at_text},
    "at": {
        "atMobiles": [person["at"]],
        "isAtAll": False
    },
}

# 发送消息 2 (Text Message with @)
res_at = requests.post(WEBHOOK, json=data_at)
print(f"Text 消息发送结果: {res_at.text}")
