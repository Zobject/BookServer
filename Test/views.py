from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from rest_framework.parsers import JSONParser
import datetime
import pymongo
import json
from  bson import json_util
# Create your views here.

try:
    conn=pymongo.MongoClient()
    print 'success'
except:
    print 'false'
db=conn['BookServer']
collection=db.Book

def index(request):
    return render(request, 'addbook.html')


def insert(request):
    Name=request.GET['name']
    Musicurl=request.GET['musicurl']
    Author =request.GET['author']
    Press =request.GET['Press']
    Column =request.GET['Column']
    Recommended = request.GET['Recommended']
    Probation =request.GET['Probation']
    Cover =request.GET['Cover']
    Brief =request.GET['brief']
    Audio = request.GET['Audio']
    Suitable =request.GET['Suitable']
    if(collection.find({"Name":Name}).count()>0):
        return  render(request,'success.html')
    doc={'Name':Name,'Musicurl':Musicurl,'Author':Author,'Press':Press,'Column':Column,'Recommended':Recommended,'Probation':Probation,'Cover':Cover,'Brief':Brief,'Audio':Audio,'Suitable':Suitable,'Upload':datetime.datetime.now(),'Degree':0,'Free':0}
    print doc
    collection.insert(doc)
    return  render(request,'success.html')


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
        #print request
        content=JSONParser().parse(request)
        Name=content.get('Name')
        print None
        date=collection.find({'Name':Name}).next()
        date['Upload']=str(date.get('Upload'))
        print date
    return HttpResponse(json.dumps(date,default=json_util.default),status=200,content_type='application/json')


@csrf_exempt
def userInfo(request):
    collection=db.UserInfo
    if request.method =="POST":
        content = JSONParser().parse(request)
        Name=content.get('Name')
        Heard=content.get('Heard')
        Love=content.get('Love')
        print Love
        if Heard== None and Love==None:
            if collection.find({'Name':Name}).count()==0:
                doc={'Name':Name,'Heard':[],'Love':[]}
                collection.insert(doc)
        if Heard!= None:
            collection.update({'Name':Name},{'$addToSet':{'Heard':Heard}})
        if Love!= None or Love!='':
            collection.update({'Name': Name}, {'$addToSet': {'Love': Love}})
        date = list(collection.find({'Name': Name}))
        returndate = {'result': date}
        return  HttpResponse(json.dumps(returndate,default=json_util.default),status=200,content_type='application/json')



@csrf_exempt
def listenlist(request):

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
    collection = db.Listener
    if request.method =="POST":
        #print request
        content=JSONParser().parse(request)
        Name=content.get('Name')
        print None
        date=collection.find({'Name':Name}).next()
        date['Upload']=str(date.get('Upload'))
        print date
    return HttpResponse(json.dumps(date,default=json_util.default),status=200,content_type='application/json')






