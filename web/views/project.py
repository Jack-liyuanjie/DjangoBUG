import time

from django.shortcuts import render, redirect
from web.forms.project import ProjectModelForm
from django.http import JsonResponse
from web import models
from django.http import HttpResponse
from utils.tencent.cos import create_bucket


def project_list(request):
    """项目列表"""
    if request.method == 'GET':
        # GET请求查看项目列表
        """
        1.从数据库中获取2部分数据
            我创建的所以项目：已星标，未星标
            我参与的所有项目：已星标，未星标
        2.提取已星标
            列表 = 循环 [我创建的所有项目] + [我参与的所有项目] 把已星标的数据提取
            
        得到3个列表：星标，创建，参与
        """
        project_dict = {'star': [], 'my': [], 'join': []}
        my_project_list = models.Project.objects.filter(creator=request.tracer.user)
        for row in my_project_list:
            if row.star:
                project_dict['star'].append({'value': row, 'type': 'my'})
            else:
                project_dict['my'].append(row)

        join_project_list = models.ProjectUser.objects.filter(user=request.tracer.user)
        for item in join_project_list:
            if item.star:
                project_dict['star'].append({'value': item.projetc, 'type': 'join'})
            else:
                project_dict['join'].append(item.projetc)

        form = ProjectModelForm(request)
        return render(request, 'project_list.html', {'form': form, 'project_dict': project_dict})

    # POST请求ajax提交数据
    form = ProjectModelForm(request, data=request.POST)
    if form.is_valid():
        # 为项目创建一个桶
        bucket = "{}-{}-1306966168".format(request.tracer.user.mobile_phone, str(int(time.time())))
        region = 'ap-chengdu'
        create_bucket(bucket, region)
        # 把桶和区域写入数据库

        # 验证通过：提交的数据有：项目名，描述，颜色 + creator谁创建的？
        form.instance.bucket = bucket
        form.instance.region = region
        form.instance.creator = request.tracer.user

        # 创建项目
        form.save()

        # 项目初始化问题类型
        issues_type_object_list = []
        for item in models.IssuesType.PROJECT_INIT_LIST:  # ["任务", '功能', 'Bug']
            issues_type_object_list.append(models.IssuesType(project=form.instance, title=item))
        models.IssuesType.objects.bulk_create(issues_type_object_list)

        return JsonResponse({'status': True})

    return JsonResponse({'status': False, 'error': form.errors})


def project_star(request, project_type, project_id):
    """星标项目"""
    if project_type == 'my':
        models.Project.objects.filter(id=project_id, creator=request.tracer.user).update(star=True)
        return redirect('web:project_list')

    if project_type == 'join':
        models.ProjectUser.objects.filter(project_id=project_id, user=request.tracer.user).update(star=True)
        return redirect('web:project_list')

    return HttpResponse('请求错误')


def project_unstar(request, project_type, project_id):
    if project_type == 'my':
        models.Project.objects.filter(id=project_id, creator=request.tracer.user).update(star=False)
        return redirect('web:project_list')

    if project_type == 'join':
        models.ProjectUser.objects.filter(project_id=project_id, user=request.tracer.user).update(star=False)
        return redirect('web:project_list')

    return HttpResponse('请求错误')


