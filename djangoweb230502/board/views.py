from django.shortcuts import render,redirect
from board.models import Board, Comment
from django.views.decorators.csrf import csrf_exempt
import chunk
import os
from django.http.response import HttpResponse, HttpResponseRedirect
import urllib
from django.db.models import Q
import math
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from board import bigdataPro

UPLOAD_DIR='c:/pyj/upload/'

# Create your views here.

def home(request):
    return render(request,'main.html')

def wordcloud(request):
    bigdataPro.wordcloud()
    return render(request,'bigdata/wordcloud.html')

def cctv(request):
    bigdataPro.cctv_map()
    return render(request,'map/map01.html')

def login_form(request):
    return render(request,'user/login.html')

@csrf_exempt
def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(request,username=username,password=password)
        
        if user is not None:
            auth.login(request,user)
            return redirect('/list/')
        else:
            return render(request,'user/login.html',{'error':'username or password is incorrect'})
    else:
        return render(request,'user/login.html')

def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return redirect('/list/')
    return render(request,'user/login.html')

def signup_form(request):
    return render(request,'user/signup.html')

@csrf_exempt
def signup(request):
    if request.method=='POST':
        if request.POST['password']==request.POST['password2']:
            username=request.POST['username']
            password=request.POST['password']
            email=request.POST['email']
            user=User.objects.create_user(username, email, password)
            return redirect('/login_form/')
    return render(request, '/user/signup.html')


def list2(request):
    boardCount=Board.objects.all().count()
    boardList=Board.objects.all().order_by("-idx")
    return render(request,'board/list.html',{'boardCount':boardCount,'boardList':boardList})

@csrf_exempt
def list(request):
    try:
        search_option=request.POST['search_option']
    except:
        search_option=''
        
    try:
        search=request.POST['search']
    except:
        search=''
        
    if search_option == 'all':
        boardCount=Board.objects.filter(Q(writer__contains=search)
                                        | Q(title__contains=search)
                                        | Q(content__contains=search)).count()
    elif search_option == 'title':
        boardCount=Board.objects.filter(Q(title__contains=search)).count()
        
    elif search_option == 'writer':
        boardCount=Board.objects.filter(Q(writer__contains=search)).count()
        
    elif search_option == 'content':
        boardCount=Board.objects.filter(Q(content__contains=search)).count()
    else:
        boardCount=Board.objects.all().count()
        
    try:
        start=int(request.GET['start'])
    except:
        start=0
        
    page_size=3
    block_size=3
    
    end=start+page_size
        
    total_page=math.ceil(boardCount/page_size) # math.ceil 소숫점 올림처리
    current_page=math.ceil((start+1)/page_size)
    start_page=math.floor((current_page-1)/block_size)*block_size+1 # math.floor 소숫점 버림처리
    end_page=start_page+block_size-1
    
    if end_page > total_page:
        end_page=total_page
    
    if start_page >= block_size:
        prev_list=(start_page-2)*page_size
    else:
        prev_list=0
        
    if end_page < total_page:
        next_list=end_page*page_size
    else:
        next_list=0
    
        
    if search_option == 'all':
        boardList=Board.objects.filter(Q(writer__contains=search)
                                        | Q(title__contains=search)
                                        | Q(content__contains=search)).order_by('-idx')[start:end] # 한페이지 내용만 가져오기
    elif search_option == 'title':
        boardList=Board.objects.filter(Q(title__contains=search)).order_by('-idx')[start:end]
        
    elif search_option == 'writer':
        boardList=Board.objects.filter(Q(writer__contains=search)).order_by('-idx')[start:end]
        
    elif search_option == 'content':
        boardList=Board.objects.filter(Q(content__contains=search)).order_by('-idx')[start:end]
    else:
        boardList=Board.objects.all().order_by('-idx')[start:end]
        
    links=[]
    for i in range(start_page,end_page+1):
        page_start=(i-1)*page_size
        link="<a href='/list/?start="+str(page_start)+"'>"+str(i)+"</a>"
        links.append(link)
        
    return render(request,'board/list.html',
                  {
                      'boardList':boardList,
                   'boardCount':boardCount,
                   'search_option':search_option,
                   'search':search,
                   'start_page':start_page,
                   'end_page':end_page,
                   'total_page':total_page,
                   'block_size':block_size,
                   "prev_list":prev_list, 
                   'next_list':next_list,
                   'links':links
                   }
                  )
                                        
def detail(request):
    id=request.GET['idx']
    dto=Board.objects.get(idx=id)
    dto.hit_up()
    dto.save()
    
    commentList=Comment.objects.filter(board_idx=id).order_by("-idx")
    # print("commentList : ",commentList)
    
    filesize="%.2f"%(dto.filesize/1024)
    return render(request, 'board/detail.html', 
                  {'dto':dto, 'filesize':filesize, 'commentList':commentList})

def reply_insert(request):
    id=request.POST['idx']
    dto=Comment(board_idx=id,
                writer=request.POST['writer'],
                content=request.POST['content']
                )
    dto.save()
    return HttpResponseRedirect("/detail?idx="+id)
    

def download(request):
    id=request.GET['idx']
    dto=Board.objects.get(idx=id)
    path=UPLOAD_DIR+dto.filename
    filename=os.path.basename(path)
    filename=urllib.parse.quote(filename)
    
    with open(path,'rb') as file:
        response=HttpResponse(file.read(),content_type='application/octet-stream')
        response['Content-Disposition']="attachment;filename*=UTF-8''{0}".format(filename)
        dto.down_up()
        dto.save()
    return response

@csrf_exempt
def update(request):
    id=request.POST['idx']
    
    dto_src=Board.objects.get(idx=id)
    fname=dto_src.filename
    fsize=dto_src.filesize
    
    if 'file' in request.FILES:
        file=request.FILES['file']
        fname=file.name
        fp=open("%s%s"%(UPLOAD_DIR, fname),'wb')
        
        for chunk in file.chunks(): #파일을 청크 데이터 단위로 쪼개줌
            fp.write(chunk) #  청크 단위로 기록
        fp.close()
            
        fsize=os.path.getsize(UPLOAD_DIR+fname)
        
    dto_new=Board(idx=id,
                   writer=request.POST['writer'],
                   title=request.POST['title'],
                   content=request.POST['content'],
                   filename=fname,
                   filesize=fsize
                   )
    
    dto_new.save()
    
    return redirect("/list/")
    
@csrf_exempt
def delete(request):
    id=request.POST['idx']
    Board.objects.get(idx=id).delete()
    return redirect("/list/")

@login_required
def write(request):
    return render(request,'board/write.html')

@csrf_exempt
def insert(request):
    fname=''
    fsize=0
    
    if 'file' in request.FILES:
        file=request.FILES['file']
        fname=file.name
        fsize=file.size
        # print('fsize : ',fsize)
        
        fp=open("%s%s"%(UPLOAD_DIR, fname),'wb')
        for chunk in file.chunks():
            fp.write(chunk)
    
        fp.close()
        
    w=request.POST['writer']
    t=request.POST['title']
    c=request.POST['content']
    
    dto=Board(writer=w, title=t, content=c, filename=fname, filesize=fsize)
    dto.save()
    return redirect("/list/")




