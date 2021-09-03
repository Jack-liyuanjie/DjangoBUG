from django.shortcuts import render, redirect
from django.http import HttpResponse
from utils.tencent.cos import delete_bucket
from web import models


def setting(request, project_id):
    return render(request, 'setting.html')


def delete(request, project_id):
    """删除项目"""
    if request.method == 'GET':
        return render(request, 'setting_delete.html')

    project_name = request.POST.get('project_name')
    if not project_name or project_name != request.tracer.project.name:
        return render(request, 'setting_delete.html', {'error': "项目名错误"})

    # 项目名写对了则删除(只有创建者可以删除)
    if request.tracer.user != request.tracer.project.creator:
        return render(request, 'setting_delete.html', {'error': "只有项目创建者可以删除项目"})

    # 1，删除桶
    #   -删除桶中的文件（找到桶中的所有文件和文件碎片+删除文件+删除文件碎片）
    #   -删除桶
    # 2，删除项目

    delete_bucket(request.tracer.project.bucket, request.tracer.project.region)
    models.Project.objects.filter(id=request.tracer.project.id).delete()

    return redirect("web:project_list")
