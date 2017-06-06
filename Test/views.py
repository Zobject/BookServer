#coding=utf8
from django import forms
from DjangoUeditor.forms import UEditorField
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, render_to_response
from django.http import HttpResponse,JsonResponse
from rest_framework.parsers import JSONParser

import datetime
import pymongo
import json
from  bson import json_util , ObjectId
# Create your views here.
import  cgi

import os
import sys
import threading

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
    Description = UEditorField("描述", initial="abc", width=600, height=800)



@csrf_exempt
def addbook(request):
    if request.method=='POST':
        collection=db.Book
        Name=request.POST['name']
        content= request.POST['Description']
        f= request.FILES.get('File')
        print f
        destination = open('./media/bookcover/' + f.name, 'wb+')
        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()
        replacebefore=str(content)
        replaceafter=replacebefore.replace('img src=\"','img src=\"52.15.123.162:8000')
        cover= '52.15.123.162:8000/media/bookcover/'+f.name
        #print replaceafter
        doc={'Name':Name,'Cover':cover,'date':replaceafter}
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
        Probation = request.POST['Probation']
       # Cover = request.GET['Cover']
        Brief = request.POST['brief']
        Audio = request.POST['Audio']
        Suitable = request.POST['Suitable']

        print request.POST
        files= request.FILES.getlist('File')

        for f in files:
            destination = open('./upload/' + f.name, 'wb+')
            for chunk in f.chunks():
                destination.write(chunk)
                filename='/Users/zobject/Git/BookServer/upload/'+f.name
                #filename = '/home/ubuntu/BookServer/upload/'+f.name
                uploadname = f.name
                s3 = boto3.client('s3')
                bucket_name = 'bookmusic'
                s3.upload_file(filename, bucket_name, uploadname, Callback=ProgressPercentage(filename))
                if percentage == 100.0:
                    print 'success'
                else:
                    return HttpResponse('upload faile!')
            destination.close()
        path='https://s3.us-east-2.amazonaws.com/bookmusic/'
        doc = {'Name': Name, 'Musicurl': path+files[0].name, 'Author': Author, 'Press': Press, 'Column': Column,
               'Recommended': Recommended, 'Probation': Probation, 'Cover': path+files[1].name, 'Brief': Brief, 'Audio': Audio,
               'Suitable': Suitable, 'Upload': datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), 'Degree': 0,
               'Free': 0}
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
            if  booksum < 5  :
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
    collection = db.UserInfo
    if request.method == "POST":
        content = JSONParser().parse(request)
        Name = content.get('Name')
        Love=content.get('Love')
        collection.update({'Name': Name}, {'$addToSet': {'Love': Love}})
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
    collection.update({'Name':Name},{'$pull':{'Love':Love}})
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
            if  booksum < 5  :
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
    return HttpResponse(json.dumps(date,default=json_util.default),status=200,content_type='application/json')






