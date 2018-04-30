#coding=utf-8
from django.views import View
from django.shortcuts import render,redirect

from django.http.response import HttpResponse,HttpResponseRedirect
class BaseView(View):
    template_name=None

    def get(self,request,*args,**kwargs):
        if hasattr(self,'prepare'):
            getattr(self,'prepare')(request,*args,**kwargs)

        # 获得cookie使用的
        if hasattr(self, 'handle_request_cookie'):
            getattr(self, 'handle_request_cookie')(request, *args, **kwargs)

        response=render(request,self.template_name,self.get_context(request))

        # 添加cookie使用的
        if hasattr(self, 'handle_response_cookie'):
            getattr(self, 'handle_response_cookie')(response, *args, **kwargs)
        return response

    def get_context(self, request):
        context = {}
        context.update(self.get_extra_context(request))
        return context

    def get_extra_context(self, request):
        return {}


class MuitlObjectReturned():
    per_page=12
    objects=None
    objects_name='objects'
    def get_objects(self,page_num='1'):
        from django.core.paginator import Paginator
        paginator=Paginator(self.objects,self.per_page)
        page_num=int(page_num)
        if page_num < 1 : page_num = 1
        if page_num > paginator.num_pages : page_num = paginator.num_pages
        page = paginator.page(page_num)
        #xrange
        return {'page':page,'page_range':paginator.page_range,self.objects_name:page.object_list}


# 需要处理一些业务逻辑
class BaseRedirctView(View):
    redirect_url=None
    def dispatch(self, request, *args, **kwargs):
        if hasattr(self,'handle'):
            getattr(self,'handle')(request,*args,**kwargs)
        return HttpResponseRedirect(self.redirect_url)

from django.http.response import JsonResponse,HttpResponseBadRequest
# 处理的都是Post请求,这个里面用不用渲染数据
# 一般来说，是不用渲染模板的，只需要返回json即可
class OperateView(View):
    form_cls = None
    def  post(self,request,*args,**kwargs):
        form = self.form_cls(request.POST.dict())
        if form.is_valid():
            handler = request.POST.get('type', '')
            if hasattr(self,handler):
                return JsonResponse(getattr(self,handler)(request,**form.cleaned_data),safe=False)
            else:
                return HttpResponseBadRequest('type没有传递')
        else:
            return JsonResponse({'errorcode':-300,'errormsg':form.errors})


from django import forms
class MyForm(forms.Form):
    goodsid = forms.IntegerField()
    colorid = forms.IntegerField()
    sizeid  = forms.IntegerField()
    count = forms.IntegerField(required=False)
    def clean(self):
        super(MyForm,self).clean()
        data = self.cleaned_data
        count = data['count']
        # if count<0:
        #     self.errors['count']=['商品数量不能小于0']

import hashlib


import  os
def fileToObj(filename):
    with open(filename) as fr:
        return eval(fr.read())
from clothesshop.settings import BASE_DIR
provinces = fileToObj(os.path.join(BASE_DIR,'assets/province.json'))
citys = fileToObj(os.path.join(BASE_DIR,'assets/city.json'))
areas = fileToObj(os.path.join(BASE_DIR,'assets/area.json'))
def md(text):
    md5 = hashlib.md5()
    md5.update(text)
    return md5.hexdigest()
def get_citys_by_id(provice_id):
    return citys[provice_id]
def get_areas_by_id(city_id):
    return areas[city_id]
def get_province_by_id(provinceid):
    for item in provinces:
        if item['id']== str(provinceid):
            return item['name']
def get_area_by_id(cityid,areaid):
    for item in areas[str(cityid)]:
        if item['id']== str(areaid):
            return item['name']
def get_city_by_id(provinceid,cityid):
    for item in citys[str(provinceid)]:
        if item['id'] == str(cityid):
            return item['name']


