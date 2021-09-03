from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client

secret_id = 'AKIDdGm8QXR8iAXjpwwlO1Xqwqb7OTKzQddO'  # 替换为用户的 secretId(登录访问管理控制台获取)
secret_key = 'f8RXP4WghW9aowuhHgsseCVaR9euvhHi'  # 替换为用户的 secretKey(登录访问管理控制台获取)
region = 'ap-chengdu'  # 替换为用户的 Region
# token = None                # 使用临时密钥需要传入 Token，默认为空，可不填
# scheme = 'https'            # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)
# 2. 获取客户端对象
client = CosS3Client(config)

response = client.upload_file(
    Bucket='liyuanjie-1306966168',
    LocalFilePath='p1.jpg',
    Key='p3.jpg',
)
print(response['ETag'])
