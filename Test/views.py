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
                date.append({"sum": sumindatabase})
            if  booksum < 5  :
                 date = list(collection.find())
            else:
                if booksum-5*(int(page))<=0:
                    date = list(collection.find().limit((booksum-5*(int(page)))%5))
                else:
                    date=list(collection.find().skip(booksum-5*(int(page))).limit(5))
        if int(target)==0:
            if int(sum) < booksum:
                date=list(collection.find().skip(sum-1))
                date.append({"sum": booksum})
        for i in  date:
            i['Upload'] = str(i.get('Upload'))

        c=list(reversed(date))
        print str(c)
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


