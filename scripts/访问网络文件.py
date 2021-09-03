import requests

res = requests.get('https://13267886101-1629860491-1306966168.cos.ap-chengdu.myqcloud.com/1629956049542_%E9%85%8D%E7%BD%AE%E5%9B%BE.png')

print(res.content)