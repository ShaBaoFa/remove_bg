# Import necessary libraries
from dotenv import dotenv_values
from aliyunsdkcore import client
from aliyunsdkcore.request import CommonRequest
import json
import oss2


class CloudService:
    def __init__(self):
        self.endpoint = dotenv_values(".env")['ALIYUN_ENDPOINT']
        self.sts_access_key_id = dotenv_values(".env")['STS_ACCESS_KEY_ID']
        self.sts_access_key_secret = dotenv_values(".env")['STS_ACCESS_KEY_SECRET']
        self.oss_access_key_id = dotenv_values(".env")['OSS_ACCESS_KEY_ID']
        self.oss_access_key_secret = dotenv_values(".env")['OSS_ACCESS_KEY_SECRET']
        self.bucket_name = dotenv_values(".env")['ALIYUN_BUCKET']
        self.role_arn = dotenv_values(".env")['ALIYUN_ROLE_ARN']
        self.last_uploaded_file_name = None

    def get_sts_token(self) -> dict:
        # Implementation to get STS token using STS credentials
        clt = client.AcsClient(self.sts_access_key_id, self.sts_access_key_secret, 'cn-hangzhou')
        request = CommonRequest(product="Sts", version='2015-04-01', action_name='AssumeRole')
        request.set_method('POST')
        request.set_protocol_type('https')
        request.add_query_param('RoleArn', self.role_arn)
        # 指定自定义角色会话名称，用来区分不同的令牌，例如填写为sessiontest。
        request.add_query_param('RoleSessionName', 'removebg')
        # 指定临时访问凭证有效时间单位为秒，最小值为900，最大值为3600。
        request.add_query_param('DurationSeconds', '3000')
        # 如果policy为空，则RAM用户默认获得该角色下所有权限。如果有特殊权限控制要求，请参考上述policy_text设置。
        # request.add_query_param('Policy', policy_text)
        request.set_accept_format('JSON')
        # ... rest of the implementation ...
        response = clt.do_action_with_exception(request)
        return json.loads(oss2.to_unicode(response))

    def upload_file(self, file_path):
        """
        Uploads a file to Aliyun OSS using the obtained STS token.

        :param file_path: Path of the file to be uploaded.
        :return: URL of the uploaded file.
        """
        sts_token = self.get_sts_token()
        auth = oss2.StsAuth(
            sts_token['Credentials']['AccessKeyId'],
            sts_token['Credentials']['AccessKeySecret'],
            sts_token['Credentials']['SecurityToken']
        )
        bucket = oss2.Bucket(auth, self.endpoint, self.bucket_name)
        # ... upload logic ...
        """上传文件到阿里云OSS"""
        with open(file_path, 'rb') as file_obj:
            try:
                print(f"正在上传: {file_path}")
                # 从file_path中获取文件名
                file_name = file_path.split('/')[-1]
                bucket.put_object(file_name, file_obj)
                self.last_uploaded_file_name = file_name
                return True
            except Exception as e:
                raise Exception(e)

    def get_signed_url(self, object_name, expiration=3600):
        """
        Generates a signed URL for an object in OSS using OSS credentials.

        :param object_name: Name of the object in the bucket.
        :param expiration: Expiration time in seconds.
        :return: Signed URL.
        """
        auth = oss2.Auth(self.oss_access_key_id, self.oss_access_key_secret)
        bucket = oss2.Bucket(auth, self.endpoint, self.bucket_name)
        # ... signed URL generation logic ...
        return bucket.sign_url('GET', object_name, expiration)

    # Additional methods related to cloud service interactions
