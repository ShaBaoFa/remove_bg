# remove_bg
解决突然需要证件照的问题）
目前进行到上传至oss，预览的部分
```shell
cp .env.sample .env
```
修改.env文件中的配置
```shell
REMOVE_BG_API_KEY=remove.bg api key
ALIYUN_ENDPOINT= oss endpoint
STS_ACCESS_KEY_ID= 
STS_ACCESS_KEY_SECRET=
OSS_ACCESS_KEY_ID=
OSS_ACCESS_KEY_SECRET=
ALIYUN_BUCKET=
ALIYUN_ROLE_ARN=
```
目前需要配置的是你sts角色的key和id，以及oss的key和id，以及bucket的名字，以及endpoint


