import requests
import datetime
import os

# 从 GitHub Secrets 读取 Webhook
WEBHOOK = os.environ["DINGTALK_WEBHOOK"]

# 值班人员列表（自定义展示名 + 手机号）
duty_list = [
    {"name": "文佳老师", "at": "13642054556"},
    {"name": "雨芃老师", "at": "13811112222"},
    {"name": "楷祥老师", "at": "13822223333"},
]

today = datetime.date.today()

# 周末不发送
if today.weekday() >= 5:
    print("周末，不发送值班提醒。")
    exit(0)

# 计算从某个起点以来的工作日数（避免周末占用顺序）
start_date = datetime.date(2025, 1, 1)  # 你可以改成实际开始日期
workdays = 0
day = start_date
while day <= today:
    if day.weekday() < 5:  # 只算工作日
        workdays += 1
    day += datetime.timedelta(days=1)

# 轮到谁值班
index = (workdays - 1) % len(duty_list)
person = duty_list[index]

# 消息正文里写“自定义名字”，@ 部分由手机号触发钉钉真实名字
msg_text = f"值班提醒：今天由 {person['name']} 值班！"

data = {
    "msgtype": "text",
    "text": {"content": msg_text},
    "at": {
        "atMobiles": [person["at"]],  # 这里会在群里高亮真实钉钉名
        "isAtAll": False
    },
}

res = requests.post(WEBHOOK, json=data)
print(res.text)
