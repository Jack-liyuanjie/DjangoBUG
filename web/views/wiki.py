from django.shortcuts import render, redirect, reverse, HttpResponse
from django.views.decorators.clickjacking import xframe_options_sameorigin

from utils.password_utils.encrypt import uid
from utils.tencent.cos import upload_file
from web.forms.wiki import WiKiModelForm
from web import models
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def wiki(request, project_id):
    """wiki首页展示"""
    wiki_id = request.GET.get('wiki_id')
    if not wiki_id or not wiki_id.isdecimal():
        return render(request, 'wiki.html')

    wiki_object = models.WiKi.objects.filter(id=wiki_id, project_id=project_id).first()

    return render(request, 'wiki.html', {'wiki_object': wiki_object})


def wiki_add(request, project_id):
    """wiki添加"""
    if request.method == 'GET':
        form = WiKiModelForm(request)
        return render(request, 'wiki_form.html', {'form': form})
    form = WiKiModelForm(request, data=request.POST)
    if form.is_valid():
        # 判断用户是否选择父节点
        if form.instance.parent:
            form.instance.depth = form.instance.parent.depth + 1
        else:
            form.instance.depth = 1

        form.instance.project = request.tracer.project
        form.save()

        return redirect(reverse('web:wiki', kwargs={'project_id': project_id}))
    return render(request, 'wiki_form.html', {'form': form})


def wiki_catalog(request, project_id):
    """wiki目录"""
    # 获取当前项目所以的目录: data = QuerySet类型
    # data = models.WiKi.objects.filter(project=request.tracer.project).values_list('id', 'title', 'parent_id')
    data = models.WiKi.objects.filter(project=request.tracer.project).values('id', 'title', 'parent_id').order_by(
        'depth', 'id')

    return JsonResponse({'status': True, 'data': list(data)})


def wiki_delete(request, project_id, wiki_id):
    """删除文章"""

    models.WiKi.objects.filter(project_id=project_id, id=wiki_id).delete()
    return redirect(reverse('web:wiki', kwargs={'project_id': project_id}))


def wiki_edit(request, project_id, wiki_id):
    """编辑文章"""
    wiki_object = models.WiKi.objects.filter(project_id=project_id, id=wiki_id).first()
    if not wiki_object:
        return redirect(reverse('web:wiki', kwargs={'project_id': project_id}))

    if request.method == 'GET':
        form = WiKiModelForm(request, instance=wiki_object)
        return render(request, 'wiki_form.html', {'form': form})

    form = WiKiModelForm(request, data=request.POST, instance=wiki_object)
    if form.is_valid():
        if form.instance.parent:
            form.instance.depth = form.instance.parent.depth + 1
        else:
            form.instance.depth = 1

        form.instance.project = request.tracer.project
        form.save()
        url = reverse('web:wiki', kwargs={'project_id': project_id})
        preview_url = "{0}?wiki_id={1}".format(url, wiki_id)
        return redirect(preview_url)

    return render(request, 'wiki_form.html', {'form': form})


@csrf_exempt
def wiki_upload(request, project_id):
    """ markdown插件上传图片 """
    result = {
        'success': 0,
        'message': None,
        'url': None
    }

    image_object = request.FILES.get('editormd-image-file')
    if not image_object:
        result['message'] = "文件不存在"
        return JsonResponse(result)

    ext = image_object.name.rsplit('.')[-1]
    key = "{}.{}".format(uid(request.tracer.user.mobile_phone), ext)
    image_url = upload_file(
        request.tracer.project.bucket,
        request.tracer.project.region,
        image_object,
        key
    )
    result['success'] = 1
    result['url'] = image_url
    return JsonResponse(result)






