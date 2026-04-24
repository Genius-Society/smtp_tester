import os

EN_US = os.getenv("LANG") != "zh_CN.UTF-8"

API_SMTP = os.getenv("smtpi")

if not API_SMTP:
    print("请检查环境变量")
    exit()
