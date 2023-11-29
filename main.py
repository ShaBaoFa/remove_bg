import os
import io
from PIL import Image, ImageTk
import requests
from aliyunsdkcore import client
from aliyunsdkcore.request import CommonRequest
from oss2.credentials import EnvironmentVariableCredentialsProvider
import json
import oss2
from dotenv import load_dotenv, dotenv_values
import tkinter as tk
from tkinter import filedialog


def get_sts_token() -> list:
    # yourEndpoint填写Bucket所在地域对应的Endpoint。以华东1（杭州）为例，Endpoint填写为https://oss-cn-hangzhou.aliyuncs.com。
    endpoint = dotenv_values(".env")['ALIYUN_ENDPOINT']
    # 填写步骤1创建的RAM用户AccessKey。
    access_key_id = dotenv_values(".env")['STS_ACCESS_KEY_ID']
    access_key_secret = dotenv_values(".env")['STS_ACCESS_KEY_SECRET']
    # role_Arn填写步骤3获取的角色ARN，例如acs:ram::175708322470****:role/ramtest。
    role_arn = dotenv_values(".env")['ALIYUN_ROLE_ARN']

    # 创建权限策略。
    # 仅允许对examplebucket执行上传（PutObject）和下载（GetObject）操作。
    # policy_text = '{"Version": "1", "Statement": [{"Action": ["oss:PutObject","oss:GetObject"], "Effect": "Allow", "Resource": ["acs:oss:*:*:examplebucket/*"]}]}'

    clt = client.AcsClient(access_key_id, access_key_secret, 'cn-hangzhou')
    request = CommonRequest(product="Sts", version='2015-04-01', action_name='AssumeRole')
    request.set_method('POST')
    request.set_protocol_type('https')
    request.add_query_param('RoleArn', role_arn)
    # 指定自定义角色会话名称，用来区分不同的令牌，例如填写为sessiontest。
    request.add_query_param('RoleSessionName', 'removebg')
    # 指定临时访问凭证有效时间单位为秒，最小值为900，最大值为3600。
    request.add_query_param('DurationSeconds', '3000')
    # 如果policy为空，则RAM用户默认获得该角色下所有权限。如果有特殊权限控制要求，请参考上述policy_text设置。
    # request.add_query_param('Policy', policy_text)
    request.set_accept_format('JSON')

    body = clt.do_action_with_exception(request)

    # 使用RAM用户的AccessKey ID和AccessKey Secret向STS申请临时访问凭证。
    token = json.loads(oss2.to_unicode(body))
    # 打印STS返回的临时访问密钥（AccessKey ID和AccessKey Secret）、安全令牌（SecurityToken）以及临时访问凭证过期时间（Expiration）。
    return [
        token['Credentials']['AccessKeyId'],
        token['Credentials']['AccessKeySecret'],
        token['Credentials']['SecurityToken']
    ]


def oss_uploader(oss_token: list, file_path: str) -> str:
    auth = oss2.StsAuth(oss_token[0], oss_token[1], oss_token[2])
    bucket = oss2.Bucket(auth, dotenv_values(".env")['ALIYUN_ENDPOINT'], dotenv_values(".env")['ALIYUN_BUCKET'])
    """上传文件到阿里云OSS"""
    with open(file_path, 'rb') as file_obj:
        try:
            print(f"正在上传: {file_path}")
            # 从file_path中获取文件名
            file_name = file_path.split('/')[-1]
            os.environ['current_file_name'] = file_name
            bucket.put_object(file_name, file_obj)
            return get_view_url()
        except Exception as e:
            raise Exception(e)

def select_file():
    """选择文件并上传"""
    file_path = filedialog.askopenfilename()
    # 限制只能上传图片
    if file_path.split('.')[-1] not in ['jpg', 'png', 'jpeg']:
        label.config(text=f"只能上传图片")
        return
    if file_path:
        """获取sts_token"""
        try:
            oss_token = get_sts_token()
        except Exception as e:
            label.config(text=f"获取token失败: {e}")
            return
        # 上传到阿里云OSS
        try:
            url = oss_uploader(oss_token, file_path)
        except Exception as e:
            label.config(text=f"上传失败: {e}")
            return
        label.config(text=f"已上传: {file_path}")
        show_image(url)

def show_image(url):
    """在UI中显示图片"""
    response = requests.get(url)
    image_data = response.content
    image = Image.open(io.BytesIO(image_data))
    photo = ImageTk.PhotoImage(image)

    image_label.config(image=photo)
    image_label.image = photo  # 保持对图像的引用

def get_view_url() -> str:
    auth = oss2.ProviderAuth(EnvironmentVariableCredentialsProvider())
    bucket = oss2.Bucket(auth, dotenv_values(".env")['ALIYUN_ENDPOINT'], dotenv_values(".env")['ALIYUN_BUCKET'])
    file_name = os.getenv('current_file_name')
    url = bucket.sign_url('GET', file_name, 60 * 60 * 24 * 365)
    # 在label根据url显示图片
    return url

# 创建UI
os.environ['OSS_ACCESS_KEY_ID'] = dotenv_values(".env")['OSS_ACCESS_KEY_ID']
os.environ['OSS_ACCESS_KEY_SECRET'] = dotenv_values(".env")['OSS_ACCESS_KEY_SECRET']
root = tk.Tk()
root.title("文件上传到阿里云OSS")
root.geometry("600x400")

button = tk.Button(root, text="选择文件并上传", command=select_file)
button.pack(pady=20)
label = tk.Label(root, text="")
label.pack()
image_label = tk.Label(root)
image_label.pack()
root.mainloop()
