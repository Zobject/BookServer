#coding=utf-8
from django import forms
from DjangoUeditor.forms import UEditorField
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, render_to_response
from django.http import HttpResponse,JsonResponse
from rest_framework.parsers import JSONParser
import random
import datetime
import pymongo
import json
from  bson import json_util , ObjectId
# Create your views here.
import  cgi

import os
import sys
import threading











import sys

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

    
import boto3

try:
    conn=pymongo.MongoClient()
    print 'success'
except:
    print 'false'
db=conn['BookServer']
collection=db.Book


class UserForm(forms.Form):
    File = forms.FileField()





#UEditor
class TestUEditorForm(forms.Form):
    Description = UEditorField("描述", initial="abc", width=400, height=600)



@csrf_exempt
def addbook(request):
    if request.method=='POST':
        collection=db.Book
        Name=request.POST['name']
        Brief=request.POST['name1']
        content= request.POST['Description']
        f= request.FILES.get('File')
        print f
        destination = open('./media/bookcover/' + f.name, 'wb+')
        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()
        print content
        replacebefore=str(content)
        replaceafter=replacebefore.replace('img src=\"','img src=\"http://52.15.123.162:8000')
        cover= 'http://52.15.123.162:8000/media/bookcover/'+f.name
        #print replaceafter
        doc={'Name':Name,'Brief':Brief,'Cover':cover,'date':replaceafter}
        print doc
        collection.insert(doc)

        return HttpResponse('success!')
    else:
        url = UserForm()
        print url
        form=TestUEditorForm()
        ls=[url,form]
        return  render(request,'addbook.html',{'form':ls})


class ProgressPercentage(object):
    percentage = 0
    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()
    def __call__(self, bytes_amount):

        # To simplify we'll assume this is hooked up
        # to a single filename.
        with self._lock:
            self._seen_so_far += bytes_amount
            global percentage
            percentage = (self._seen_so_far / self._size) * 100


@csrf_exempt
def addlisten(request):
    if request.method=='POST':
        #url=UserForm(request.POST,request.FILES)
        collection=db.Listen
        Name = request.POST['name']
        #Musicurl = request.GET['musicurl']
        Author = request.POST['author']
        Press = request.POST['Press']
        Column = request.POST['Column']
        Recommended = request.POST['Recommended']
        # Probation = request.POST['Probation']
       # Cover = request.GET['Cover']
        Brief = request.POST['brief']
        # Audio = request.POST['Audio']
        Suitable = request.POST['Suitable']


        musicurl=request.POST['musicurl']
        # print request.POST
        files= request.FILES.getlist('File')
        print files
        for f in files:
            destination = open('./media/listen/' + f.name, 'wb+')
            for chunk in f.chunks():
                destination.write(chunk)
                #filename='/Users/zobject/Git/BookServer/media/listen/'+f.name
                # filename = '/home/ubuntu/BookServer/media/listen/'+f.name
                # uploadname = f.name
                # s3 = boto3.client('s3')
                # bucket_name = 'bookmusic'
                # s3.upload_file(filename, bucket_name, uploadname, Callback=ProgressPercentage(filename))
                # if percentage == 100.0:
                #     print 'success'
                # else:
                #     return HttpResponse('upload faile!')
            destination.close()
        #path='https://s3.us-east-2.amazonaws.com/bookmusic/'
        cover = 'http://52.15.123.162:8000/media/listen/'
        doc = {'Name': Name, 'Musicurl': musicurl, 'Author': Author, 'Press': Press, 'Column': Column,
               'Recommended': Recommended,  'BookCover':cover+files[0].name, 'Brief': Brief, 'Musiccover': cover+files[1].name,
               'Suitable': Suitable, 'Upload': datetime.datetime.now().strftime("%Y.%m.%d"), 'Degree': random.randint(10000,100000)}
        print doc
        if (collection.find({"Name": Name}).count() > 0):
            return HttpResponse('already exist!')
        collection.insert(doc)
        return  HttpResponse('upload ok!')
    else:
        url=UserForm()
        print url
    return render_to_response('upload.html', {'uf': url})


@csrf_exempt
def booklist(request):
    if request.method=="POST":
        date=[]
        c={}
        content=JSONParser().parse(request)
        page=content.get('page')
        target=content.get('target')
        sum=content.get('sum')
       # page=request.GET['page']
        booksum = collection.find().count()
        if int(target)==1:
            #sum=collection.find().count()
            if int(page)==1:
                sumindatabase = collection.find().count()
                c = {"sum": str(sumindatabase)}
            if  booksum < 5 and  int(page)== 1  :
                   date = list(collection.find())
            else:
                if int(page)==booksum/5+1:
                    date = list(collection.find().limit((booksum-5*(int(page)))%5))
                elif int(page)>booksum/5+1:
                    date=[]
                else:
                    date=list(collection.find().skip(booksum-5*(int(page))).limit(5))
        if int(target)==0:
            if int(sum) < booksum:
                date=list(collection.find().skip(int(sum)))
                c={"sum": str(booksum)}
            else:
                date=[]
        for i in  date:
            i['Upload'] = str(i.get('Upload'))
        if date!=None:
            c['result']=list(reversed(date))
    return HttpResponse(json.dumps(c,default=json_util.default),status=200,content_type='application/json')



@csrf_exempt
def bookdetails(request):
    if request.method =="POST":
        collection = db.Book
        #print request
        content=JSONParser().parse(request)
        Name=content.get('Name')
        date=collection.find_one({'Name':Name})
        print date
    return HttpResponse(json.dumps(date,default=json_util.default),status=200,content_type='application/json')


@csrf_exempt
def createuserinfo(request):
    collection=db.UserInfo
    if request.method =="POST":

        content = JSONParser().parse(request)
        Name=content.get('Name')
        if collection.find({'Name': Name}).count() == 0:
            doc={'Name':Name,'Love':[]}
            collection.insert(doc)
        return JsonResponse({'target':'success'})

@csrf_exempt
def createuserlove(request):
    collection=db.Book
    if request.method == "POST":
        content = JSONParser().parse(request)
        Name = content.get('Name')
        Love=content.get('Love')
        Taregt=content.get('Target')
        if Taregt=='0':
            date=collection.find_one({'Name': Love})
            print str(date)
            collection = db.UserInfo
            collection.update({'Name': Name}, {'$addToSet': {'Love': date}})
        else:
            collection = db.UserInfo
            collection.update({'Name': Name}, {'$pull': {'Love': {'Name': Love}}})
        return JsonResponse({'target': 'success'})





@csrf_exempt
def getuserlove(request):
  collection = db.UserInfo
  if request.method == "POST":

    content = JSONParser().parse(request)
    Name = content.get('Name')
    date=list(collection.find({'Name':Name}))

    return HttpResponse(json.dumps(date,default=json_util.default),status=200,content_type='application/json')
        # if  target==None:
        #     if collection.find({'Name':Name}).count()==0:
        #         doc={'Name':Name,'Love':[]}
        #         collection.insert(doc)
        #         return  JsonResponse({'target':'success'})
        #     else:
        #         collection.update({'Name': Name}, {'$addToSet': {'Love': Love}})
        # date = list(collection.find({'Name': Name}))
        # returndate = {'result': date}
        # return  HttpResponse(json.dumps(returndate,default=json_util.default),status=200,content_type='application/json')

@csrf_exempt
def removeuserlove(request):
  collection = db.UserInfo
  if request.method == "POST":

    content = JSONParser().parse(request)
    Name = content.get('Name')
    Love = content.get('Love')
    collection.update({'Name':Name},{'$pull':{'Love':{'Name':Love}}})
    return JsonResponse({'target':'success'})



@csrf_exempt
def listenlist(request):
    collection=db.Listen
    if request.method=="POST":
        date=[]
        c={}
        content=JSONParser().parse(request)
        page=content.get('page')
        target=content.get('target')
        sum=content.get('sum')
       # page=request.GET['page']
        booksum = collection.find().count()
        if int(target)==1:
            #sum=collection.find().count()
            if int(page)==1:
                sumindatabase = collection.find().count()
                c = {"sum": str(sumindatabase)}
            if  booksum < 5 and int(page)== 1 :
                 date = list(collection.find())
            else:
                if int(page)==booksum/5+1:
                    date = list(collection.find().limit((booksum-5*(int(page)))%5))
                elif int(page)>booksum/5+1:
                    date=[]
                else:
                    date=list(collection.find().skip(booksum-5*(int(page))).limit(5))
        if int(target)==0:
            if int(sum) < booksum:
                date=list(collection.find().skip(int(sum)))
                c={"sum": str(booksum)}
            else:
                date=[]
        for i in  date:
            i['Upload'] = str(i.get('Upload'))
        if date!=None:
            c['result']=list(reversed(date))
    return HttpResponse(json.dumps(c,default=json_util.default),status=200,content_type='application/json')



@csrf_exempt
def listendetails(request):
    collection = db.Listen
    if request.method =="POST":
        #print request
        content=JSONParser().parse(request)
        Name=content.get('Name')
        print None
        date=collection.find({'Name':Name}).next()
        date['Upload']=str(date.get('Upload'))
        #print date
        collection.update({'Name':Name},{'$inc':{'Degree':random.randint(1,10)}})
    return HttpResponse(json.dumps(date,default=json_util.default),status=200,content_type='application/json')




def test(request):



    if request.method=='GET':
        name=request.GET['Name']
        print name
        content=collection.find_one({'Name':name})
        data=content.get('date')
    return  HttpResponse(data,content_type='text/html')


#添加音乐接口
@csrf_exempt
def addmusic(request):
    db=conn['FreeMusic']
    collection=db.Music
    if request.method=='POST':
        title = request.POST['title']
        musicurl=request.POST['musicurl']
        imgurl=request.POST['imgurl']
        uid = request.POST['uid']
        if request.POST['uid']!='':
            print 'xxxxxxx'
            uid=request.POST['uid']
            doc = {'url': musicurl, 'title': title, 'img': imgurl, 'id': int(uid)}

        else:
            print 'aaaaa'
            top = request.POST['top']
            doc = {'url': musicurl, 'title': title, 'img': imgurl,'top':int(top),'time':datetime.datetime.now()}
        collection.insert(doc)
        return  HttpResponse('success')
    else:
        return render(request,'addmusic.html')



#删除音乐接口
def freedelet(request):
    if request.method=='GET':
        db = conn['FreeMusic']
        collection = db.Music
        id=request.GET['top']
        collection.remove({'top':int(id)})
        return render(request, 'success.html')

#单条更改更改数据接口
def freechange(request):

    if request.method=='GET':
        db = conn['FreeMusic']
        collection = db.Music
        if request.GET['top']!=None:
            top=request.GET['top']
            data = collection.find_one({'top': int(top)})
        else:
            uid = request.GET['uid']
            data=collection.find_one({'id':int(uid)})
        # data.update(id=data.pop("id"))
        return render(request, 'change.html', {'data': data})

#更新成功接口
@csrf_exempt
def changesome(request):
    if request.method=='POST':
        db = conn['FreeMusic']
        collection = db.Music
        title = request.POST['title']
        musicurl = request.POST['musicurl']
        imgurl = request.POST['imgurl']
        if request.POST.has_key('top'):
            top=request.POST['top']
            collection.update({'top': int(top)}, {'$set': {'url': musicurl, 'title': title, 'img': imgurl,'time':datetime.datetime.now()}})
            return render(request,'success.html')
        else:
            uid = request.POST['uid']
            collection.update({'id': int(uid)}, {'$set': {'url': musicurl, 'title': title, 'img': imgurl}})
            return render(request, 'success.html')



#数据更改主界面
def changesomething(request):
    db=conn['FreeMusic']
    collection=db.Music
    if request.method=='GET':
            data=list(collection.find())

    return render(request,'test.html',{'data':data})

    # elif request.method=='POST':
    #     # uid=request.POST['uid']
    #     # cao=request.POST['caozuo']
    #     if int(cao)==1:
    #         collection.remove({'_id':uid})
    #         return HttpResponse('success')
    #     elif int(cao)==0:
    #         collection.find({"_id":uid})

#返回数据接口
@csrf_exempt
def freemusic(request):
    result={}
    db=conn['FreeMusic']
    collection=db.Music
    result=[]
    top=[]
    other=[]
    if request.method=='POST':
        coetent=JSONParser().parse(request)
        page=int(coetent.get('page'))
        print page
        for i in range(1,collection.find().count()+1):
            if collection.find({'top':i}).count()>1:
                data=collection.find({'top':i}).sort([('time',pymongo.DESCENDING)])
                top.append(data.next())
            else:
                data = collection.find_one({'top': i})
                if data!=None:
                 top.append(data)
        # other=list(collection.find({'id':{'$exists':'true'}}).sort('id'))
        result={'top':top,}
    return HttpResponse(json.dumps(result,default=json_util.default),status=200,content_type='application/json')


def showbooklist(request):
    if request.method=='GET':
        db=conn['BookServer']
        collection=db.Book
        data=list(collection.find())
        return render(request,'showbooklist.html',{'data':data})

def bookdele(request):
    if request.method=='GET':
        db=conn['BookServer']
        name=request.GET['name']
        collection=db.Book
        data=collection.find_one({'Name':name})
        return  render(request,'')