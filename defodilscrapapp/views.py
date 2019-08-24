from django.shortcuts import render
from django.shortcuts import render, HttpResponse
# Create your views here.

from django.shortcuts import render, redirect
from django.contrib import auth, messages


import os
import urllib
import urllib.request
from urllib.request import urlopen
from bs4 import BeautifulSoup
# from urlparse import urlsplit
from os.path import basename

from bs4 import BeautifulSoup
import requests

import requests
from bs4 import BeautifulSoup
import xlwt 
from xlwt import Workbook

from django.contrib.auth.decorators import login_required

def login(request):

    if request.user.is_authenticated:
        return redirect('home')
 
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(password)
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            # correct username and password login the user
            auth.login(request, user)
            return redirect('home')
 
        else:
            messages.error(request, 'Error wrong username/password')
 
    return render(request, 'login.html')
 

@login_required(login_url='login')
def home(request):
    return render(request, "home.html")



 
def logout(request):
    auth.logout(request)
    return redirect('login')  
  
@login_required(login_url='login')
def scrap_data(request):
    e_links = request.POST['e_links']
    e_tag = request.POST['e_tag']
    print(e_links)
    print(e_tag)
    if e_tag == 'heading':
        try:

            url = e_links
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            tb = soup.find_all("h2", class_="title")

            f= open("result/headlines.txt", "w+")

            for i in tb:
                    try:
                            ss = i.find("a").contents
                            # print(ss)
                            k = ss[0]   
                            # # print(str(k))
                            # # print()
                            k = str(k)
                            print(k)
                            f.write(k + "\n")
                            
                    except:
                            pass
                            # print("No")
            f.close() 
        except:
            pass
    elif e_tag == 'paragraph':
        try:
            url = e_links
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            # tb = soup.find('tr')
            tb = soup.find_all("p")

            # wb = Workbook()
            # sheet1 = wb.add_sheet('Sheet 1') 
            #     # add_sheet is used to create sheet.
            f= open("result/paragraph.txt", "w+")

            for i in tb:
                    try:
                            ss = i.contents
                            # print(ss[0])
                            k = ss[0]   
                            # print(str(k))
                            # print()
                            k = str(k)
                            print(k)
                            f.write(k + "\n")
                            print(1)
                    except:
                            pass
                            # print("No")
            f.close()  

        except:
            pass       
    elif e_tag == 'telephone':
        try:
            url = e_links
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            # tb = soup.find('tr')
            tb = soup.find_all("td", colspan="2")

            wb = Workbook() 
                # add_sheet is used to create sheet. 
            sheet1 = wb.add_sheet('Sheet 1') 
            sheet1.write(0, 0, 'TelePhone Number')
            count = 0
            for i in tb:
                
                j = i.contents
                ss = j[0]
                # print(ss)
                try:
                    if ss[:3] == '+88' or ss[:2]=='01' :
                        count += 1       
                        print(ss)      
                        sheet1.write(count, 0, ss)   
                    
                except:
                    print("no")
                wb.save('result/telephone.xls')
        except:
            pass        

    elif e_tag == 'image':
        try:
            url = e_links
            html = urlopen(url)
            soup = BeautifulSoup(html, "lxml")

            imgs = soup.findAll('img')
            print("aa")
            # user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
            # headers={'User-Agent':user_agent,} 

            for img in imgs:
                print("VV")
                # print(img)
                jf = img.get('src')
                
                print(jf)
                # j = img.get('src').read()
                # fileName = basename(urlsplit(jf)[2])
                # output = open(fileName,'wb')
                # output.write(j)
                # output.close()
                # print(img.get('src'))

#'/home/asus/Desktop/defodilscrap/result/imagefile' 

                try:
                    my_path = '/home/asus/Desktop/defodilscrap/result/imagefile'    #'/home/asus/Desktop/amarfile'
                    urllib.request.urlretrieve(jf, os.path.join(my_path, os.path.basename(jf)))
                    #   with open(basename(jf), "wb") as f:
                    #     f.write(requests.get(jf).content)  
                #     uopen = urlopen(jf)
                #     stream = uopen.read()
                #     file = open('myfile.jpg','w')
                #     file.write(stream)
                #     file.close()
                except:
                    print('not found')  
        except:
            pass              

    return HttpResponse("check your Folder") 


