from django import forms

from web import models
from web.forms.bootstrap import BootStrapForm


class WiKiModelForm(BootStrapForm, forms.ModelForm):
    class Meta:
        model = models.WiKi
        exclude = ['project', 'depth']

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 找到想要的字段,把他绑定显示的数据重置
        # 数据 = 去数据库中获取当前项目的所以wiki标题
        total_data_list = [("", '---请选择---'),]
        data_list = models.WiKi.objects.filter(project=request.tracer.project).values_list('id', 'title')
        total_data_list.extend(data_list)
        self.fields['parent'].choices = total_data_list
