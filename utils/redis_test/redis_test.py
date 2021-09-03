import redis

conn = redis.Redis(host='116.62.193.152', port=6379, password='123456', encoding='utf-8', db=1)

conn.set('13267886101', 9999, ex=60)

value = conn.get('13267886101')
print(value)