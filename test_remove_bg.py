# Requires "requests" to be installed (see python-requests.org)
import requests

response = requests.post(
    'https://api.remove.bg/v1.0/removebg',
    data={
        'image_url': 'https://wlf-upload-file.oss-cn-hangzhou.aliyuncs.com/wlfpanda.jpg?Expires=1701336977&OSSAccessKeyId=TMP.3KkRprBaL5ZFe6JfpHzY3VuUCQvPhLPzZ8pAxpyt4h1A24QfT48keqpNNjqsehaQRJeGK2BijKFrKhgtkyf9gpivEorqKF&Signature=vQVE9gYwu4E7kKIsFrDDX7DEIkI%3D',
        'size': 'auto'
    },
    headers={'X-Api-Key': 'dgpggvKUkdU2sS9XPcns3EQE'},
)
if response.status_code == requests.codes.ok:
    with open('no-bg.png', 'wb') as out:
        out.write(response.content)
else:
    print("Error:", response.status_code, response.text)