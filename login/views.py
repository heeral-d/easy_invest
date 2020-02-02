from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
#from bs4 import BeautifulSoup as soup
import time



from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.sessions.models import Session

global username

# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            request.session['username']=username
            return redirect('/home')
        else:
            messages.info(request,'Invalid credentials')
            return redirect('login')
    else:
        return render(request,'login.html')


def dashboard(request):
    return render(request, 'dashboard.html')

#def home(request):
#   return render(request, 'index.html',{'username':'root'})


def register(request):
    print(request.method)
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('/register')
            else:        
                user = User.objects.create_user(username=username, password=password1, first_name=first_name, last_name=last_name)
                user.save()
                print('user added')
                return redirect('login')
        else:
            messages.info(request, 'Passwords not matching')
            return redirect('/register')
        return redirect('/')
          
    else:    
        return render(request, 'register.html')


def home(request):
    chrome_options=webdriver.ChromeOptions()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--proxy-server='direct://'")
    chrome_options.add_argument("--proxy-bypass-list=*")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--ignore-certificate-errors')
    browser=webdriver.Chrome(executable_path=r"C:\Users\Admin\projects\hackit\chromedriver.exe",options=chrome_options)
    browser.get("https://www.wishberry.in/success-stories")
    b=[]
    p=0
    project_name=[]
    categories=[]
    amount=[]
    backers=[]
    requiredAmount=[]
    description=[]
    tasks=[]
    link=[]

    for i in range(18):
        if i%6==5:
            p+=1
        if i>5:
            for j in range(p):
                load_more=WebDriverWait(browser,20).until(EC.presence_of_element_located((By.CSS_SELECTOR,".cursor.fw-sb.pr15.mt20.block-display.text-center.tc-primary")))
                load_more.click()
        WebDriverWait(browser,20).until(EC.presence_of_element_located((By.CSS_SELECTOR,".f18.bw-b.f-pts.h45.block-display.lh-12.mb5")))
        category=browser.find_elements_by_css_selector('.inblock.f14.bdr-rad.bdr.pt5.pb5.pl15.pr15.mr20')
        categories.append(category[i].get_attribute('innerText'))
        #print(category[i].get_attribute('innerText'))
        links=browser.find_elements_by_css_selector(".f18.bw-b.f-pts.h45.block-display.lh-12.mb5")
        links[i].click()
        WebDriverWait(browser,20).until(EC.presence_of_element_located((By.CSS_SELECTOR,".campaign-info-data.f16.fw-l.grey.mb10")))
        required_amount=browser.find_element_by_css_selector('.campaign-info-data.f16.fw-l.grey.mb10')
        ra=required_amount.get_attribute('innerText').split()
        num_req_amt=int(ra[5].replace(',',''))
        #print(num_req_amt)
        amount.append(num_req_amt)
        required_amount=''.join(ra[4:])
        requiredAmount.append(required_amount)
        #print(required_amount)
        backer=browser.find_elements_by_css_selector('.f42.f-pts.text')
        backers.append(backer[1].get_attribute('innerText'))
        #print(backers[1].get_attribute('innerText'))
        projectname=browser.find_element_by_css_selector('.f-pts.f28.m10').get_attribute('innerText')
        project_name.append(projectname)
        #print(projectname)
        project_desc=browser.find_element_by_css_selector('p').get_attribute('innerText')
        description.append(project_desc)
        #print(project_desc)
        amount_to_be_spend=browser.find_elements_by_css_selector('text')
        project_expend=[]
        temp=[]

        for am in amount_to_be_spend:
            amt=am.get_attribute('innerHTML')
            temp.append(amt)
            c=(amt.split())[0]
            project_expend.append(int(c.replace(',','')))
            #print(amt)
        tasks.append(temp)
        #print(project_expend)
        b.append(project_expend)
        project_links=browser.find_elements_by_css_selector('.campaign-share')
        temp2 = []
        for l in project_links:
            #print(l.get_attribute("href"))
            temp2.append(l.get_attribute("href"))
        link.append(temp2)
        browser.execute_script("window.history.go(-1)")
        #print()

    browser.quit()

    '''print('\n\npn ====== ',project_name)
    print('\n\ncat =====',categories)
    print('\n\namt ====',amount)
    print('\n\nback ===',backers)
    print('\n\nra ====',requiredAmount)
    print('\n\nt =====',tasks)
    print('\n\nta ====',b)
    print('\n\nlinks ==',link)
    print(description)'''

    mlist = zip(project_name,description,categories,backers, requiredAmount, amount, tasks, b, link)
    context = {'mylist':mlist,}
    return render(request, 'index.html', context)
    #{'pname':project_name, 'categories':categories, 'backers':backers, 'namount':amt ,'total_amount':requiredAmount, 'tasks':tasks, 'tamount':b, 'links':links, 'description':description}