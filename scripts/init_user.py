import os
import sys
import django

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DjangoBUG.settings")
django.setup()

from web import models
# 往数据库插入
# models.UserInfo.objects.create(username='李元杰', email='liyuanjie@live.com', mobile_phone='11957476091', password=123456789)
