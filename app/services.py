import random
import json
import string
from dao import database
import time
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import asyncio
# 用于存储验证码信息的全局字典
verification_codes = {}

def load_config():
    with open("config.json","r") as file:
        config = json.load(file)

        email_config=config.get("email",{})

        my_account = email_config.get("my_account")
        my_pass = email_config.get("my_pass")

        if not my_account or not my_pass:
            raise ValueError("Missing email account or password in config file.")

    return my_account,my_pass

my_account,my_pass=load_config()

def create_verification_code(email: str) -> str:
    # 生成6位随机验证码
    code = str(random.randint(100000, 999999))

    # 当前时间戳
    current_timestamp = time.time()

    # 设置验证码有效期为300秒
    expiry_timestamp = current_timestamp + 300

    # 拼接邮箱和验证码形成唯一的键
    verification_string = f"{email}_{code}"

    # 将验证码信息存储到字典
    verification_codes[verification_string] = {
        "code": code,
        "timestamp": current_timestamp,
        "expiry": expiry_timestamp
    }

    # 返回生成的验证码
    return code

def send_verification_code(code:str ,email:str):
    ret = True
    try:
        msg = MIMEText(f'验证码，请勿泄露：\n{code}','plain','utf-8')
        msg['From'] = formataddr(["天气网站",my_account])
        msg['To'] = formataddr(["尊敬的用户",email])
        msg['Subject'] = "天气网站注册验证码"

        server=smtplib.SMTP_SSL("smtp.qq.com",456)
        server.login(my_account,my_pass)
        server.sendmail(my_account,[email],msg.as_string())
        server.quit()
    except Exception:
        ret = False
    return ret

async def delete_expired_codes():
    while True:
        # 获取当前时间戳
        current_timestamp = time.time()
        # 创建一个待删除的验证码列表
        expired_keys = []
        
        # 检查每个验证码的过期时间
        for key, value in list(verification_codes.items()):
            if current_timestamp > value["expiry"]:
                expired_keys.append(key)
        
        # 删除过期验证码
        for key in expired_keys:
            del verification_codes[key]
            print(f"Deleted expired code: {key}")
        
        # 每隔60秒检查一次过期的验证码
        await asyncio.sleep(60)

def verify_verification_code(code:str,email:str):
    verify_string = f"{email}_{code}"
    if verify_string in verification_codes :
        stored_info = verification_codes[verify_string]
        del verification_codes[verify_string]
        return True


    