from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.contrib import messages 
from .models import *
from .forms import *
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings
import re
from django.db.models import Q

from django.http import JsonResponse,HttpResponse
import random


import razorpay
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


# ------------------- SIGNUP/LOGIN/LOGOUT FUNCTIONS STARTS ---------------------

# User Login

def login(l1):
    if l1.method=='POST':
        u = l1.POST.get('username')
        p =  l1.POST.get('password')
        if u=='admin'and p=='123':
            return redirect(adminindex)

        elif usersignup.objects.filter(username=u).exists():
            usr = usersignup.objects.filter(username=u).first()
            if usr.password == p:
                l1.session['id'] = [usr.id]
                return redirect(index)
            else:
                messages.info(l1,'Incorrect Password',extra_tags="login")
                return redirect(login)

        else:
            messages.info(l1,'Username not found',extra_tags="login")
            return redirect(login)
        
    return render(l1,'login.html')

# Logout page

def logout(l3):
    if 'id' in l3.session:
        l3.session.flush()
        return redirect(index)
    return redirect(index)


# User Signup

def signup(l2):
    if l2.method == 'POST':
        n = l2.POST.get('name')
        e = l2.POST.get('email')
        ph = l2.POST.get('phone')
        u = l2.POST.get('username')
        p = l2.POST.get('password')
        p2 = l2.POST.get('repassword')
        if p == p2:
            if usersignup.objects.filter(username=u).exists():
                messages.info(l2,"Username already exists",extra_tags="signup")
                return redirect(signup) 
            elif usersignup.objects.filter(email=e).exists():
                messages.info(l2,"Email already exists",extra_tags="signup")
                return redirect(signup)  
            else:
                try:
                    y=re.search("(?=.{8,})(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[~!@#$%^&*?])",p)
                    x=re.findall(r'^[6-9][0-9]{9}',ph)
                    if x==[ph]:
                        if y==None:
                            messages.info(l2,"Password is not strong",extra_tags="signup")
                            return redirect(signup)
                        else:
                            val=usersignup.objects.create(name=n,email=e,phone=ph,username=u,password=p)
                            val.save()  
                            return redirect(login) 
                    else:
                        messages.info(l2,"Not a valid phone number",extra_tags="signup")
                        return redirect(signup)
                except:
                    messages.info(l2,"Invalid input",extra_tags="signup")
        else:
            messages.info(l2,"Password doesn't match",extra_tags="signup")
            return redirect(signup) 

    return render(l2,'login.html')

# ------------------- SIGNUP/LOGIN/LOGOUT FUNCTIONS ENDS ---------------------
##########################



# ------------------- HOME FUNCTIONS STARTS ---------------------

# Main pages

def base(r11):
    if 'id' in r11.session:
        se = r11.session.get('id')
        val = se[0]
        usr = usersignup.objects.filter(id=val).first()
        c = mycart.objects.filter(usr=val).all()
        pro = profilepic.objects.filter(user=usr).first()
        cnt = c.count()
        return render(r11,'base.html',{'cnt':cnt,'usr':usr,'pro':pro})
    return render(r11,'base.html')

def index(r1):
    if 'id' in r1.session:
        se = r1.session.get('id')
        val = se[0]
        usr = usersignup.objects.filter(id=val).first()
        c = mycart.objects.filter(usr=val).all()
        pro = profilepic.objects.filter(user=usr).first()
        cnt = c.count()
        obj=products.objects.all()
        l=[]
        for i in obj:
            if len(l) < 3:
                l.append(i)
            else:
                pass
        k=[]
        n=[]
        for i in obj:
            k.append(i)
        k.reverse()
        for j in k:
            if len(n) < 6:
                n.append(j)
            else:
                pass
        return render(r1,'index.html',{'l':l,'n':n,'cnt':cnt,'usr':usr,'pro':pro})
    else:
        obj=products.objects.all()
        l=[]
        for i in obj:
            if len(l) < 3:
                l.append(i)
            else:
                pass
        k=[]
        n=[]
        for i in obj:
            k.append(i)
        k.reverse()
        for j in k:
            if len(n) < 6:
                n.append(j)
            else:
                pass
        print(n)
        print(k)
        return render(r1,'index.html',{'l':l,'n':n})

    

# ------------------- HOME FUNCTIONS ENDS ---------------------
##########################



# ------------------- CART FUNCTIONS STARTS ---------------------

# Cart function

def cartt(c1):
    if 'id' in c1.session:
        se = c1.session.get('id')
        val = se[0]
        c = mycart.objects.filter(usr=val).all()
        cnt = c.count()
        cl = {}
        t=0
        for i in c:
            cl[i.products]=[i.quantity,i.id,i.products.discount*i.quantity]
            t=t+(i.products.discount*i.quantity)
        print(cl)

        usr = usersignup.objects.filter(id=val).first()
        return render(c1,'cart.html',{"usr":usr,"cl":cl,'cnt':cnt,'t':t})
    return redirect(login)

# Add to Cart function

def addcart(r3,wal=0):
    if 'id' in r3.session:
        se = r3.session.get('id')
        val = se[0]
        c = mycart.objects.filter(usr=val).all()
        if r3.method == 'POST':
            p = products.objects.filter(id=wal).first()
            usr = usersignup.objects.get(id = val)
            if c:
                f=0
                for i in c:
                    if i.products == p:
                        f=1
                        i.quantity = i.quantity + 1
                        i.save()
                        return redirect(cartt)
                if f==0:
                    val = mycart.objects.create(usr = usr,products = p,quantity = 1,delivered = False)
                    val.save()
                    return redirect(cartt)   
            else:
                val = mycart.objects.create(usr = usr,products = p,quantity = 1,delivered = False)
                val.save()  
                return redirect(cartt)
    return redirect(login)


# Deleting cart items

def deletecart(d1,de):
    if 'id' in d1.session:
        c=mycart.objects.get(id=de)
        c.delete()
        return redirect(cartt)

# Decreasing cart items

def minuscart(d2,de):
    if 'id' in d2.session:
        c=mycart.objects.get(id=de)
        if c.quantity>1:
            c.quantity = c.quantity - 1
            c.save()
        else:
            c.delete()
        return redirect(cartt)

# Increasing cart items

def pluscart(d3,de):
    if 'id' in d3.session:
        c=mycart.objects.get(id=de)
        c.quantity = c.quantity + 1
        c.save()
        return redirect(cartt)


# ------------------- CART FUNCTIONS ENDS ---------------------
##########################



# ------------------- SEARCH FUNCTIONS STARTS ---------------------

# Search page
def searchfn(s):
    if 'id' in s.session:
        se = s.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id = val)
        c = mycart.objects.filter(usr=val).all()
        cnt = c.count()
        if s.method == 'POST':
            sr = s.POST.get('sr')
            l = products.objects.filter(name__icontains = sr)
            return render(s,'shop-list.html',{'l':l,'cnt':cnt,"usr":usr})
        return render(s,'shop-single.html',{'cnt':cnt,"usr":usr})
    else:
        if s.method == 'POST':
            sr = s.POST.get('sr')
            l = products.objects.filter(name__icontains = sr)
            return render(s,'shop-list.html',{'l':l})
        return render(s,'shop-single.html')



    # if s.method == 'POST':
    #     sr = s.POST.get('sr')
    #     l = products.objects.filter(name__icontains = sr)
    #     return render(s,'shop-list.html',{'l':l})
    # return render(s,'shop-list.html')


# ------------------- SEARCH FUNCTIONS ENDS ---------------------
##########################



# ------------------- CHECKOUT FUNCTIONS STARTS ---------------------

# Checkout page

def checkout(r4):
    if 'id' in r4.session:
        se = r4.session.get('id')
        val = se[0]
        c = mycart.objects.filter(usr=val).all()
        if c:
            cnt = c.count()
            cl = {}
            t=0
            for i in c:
                cl[i.products]=[i.quantity,i.id,i.products.discount*i.quantity]
                t=t+(i.products.discount*i.quantity)

            usr = usersignup.objects.filter(id=val).first()
            det = profile.objects.filter(user=usr).first()

            return render(r4,'checkout.html',{"usr":usr,"cl":cl,'cnt':cnt,'t':t,"det":det})
    return redirect(cartt)
# Thankyou page

def thanku(r8):
    if 'id' in r8.session:
        se = r8.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id = val)
        return render(r8,'thankyou.html',{"usr":usr})
    else:
        return render(r8,'thankyou.html')

# ------------------- CHECKOUT FUNCTIONS ENDS ---------------------
##########################



# ------------------- ABOUT AND CONTACT FUNCTIONS STARTS ---------------------

def about(r2):
    if 'id' in r2.session:
        se = r2.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id = val)
        c = mycart.objects.filter(usr=val).all()
        cnt = c.count()
        return render(r2,'about.html',{'cnt':cnt,"usr":usr})
    else:
        return render(r2,'about.html')


def contact(r5):
    if 'id' in r5.session:
        se = r5.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id = val)
        c = mycart.objects.filter(usr=val).all()
        dtls=[]
        print("HELLO",c)
    
        print("HELLO HI")
        cnt = c.count()
        if r5.method=='POST':
            n=r5.POST.get('name')
            m=r5.POST.get('mobile')
            e=r5.POST.get('email')
            me=r5.POST.get('message')
            l=msg.objects.create(name=n,mobile=m,email=e,message=me)
            l.save()
            return redirect(contact)
        return render(r5,'contact.html',{'cnt':cnt,"usr":usr})
    else:
        return redirect(login)

# ------------------- ABOUT AND CONTACT FUNCTIONS ENDS ---------------------
##########################



# ------------------- SHOP PAGES FUNCTIONS STARTS ---------------------
    
#shop-Index
def shop_reg(r):
    shps=shopsignup.objects.all()
    
    if r.method=='POST':
        e = r.POST.get('email')
        ph = r.POST.get('phone')
        u = r.POST.get('username')
        p = r.POST.get('password')
        p2 = r.POST.get('repassword')
   
        
        if p == p2:
            
            if shopsignup.objects.filter(username=u).exists():
                messages.info(r,"Username already exists",extra_tags="signup")
                return redirect(shop_login) 
            elif shopsignup.objects.filter(email=e).exists():
                messages.info(r,"Email already exists",extra_tags="signup")
                return redirect(shop_login)  
            elif shopsignup.objects.filter(phone=ph).exists():
                messages.info(r,"Phone=Number already exists",extra_tags="signup")
                return redirect(shop_login)
            else:
                
                frm=shopsignupform(r.POST,r.FILES)
                
                if frm.is_valid():
                    print('IN valid',e,ph,u,p,p2)
                    frm.save()
                    obj=shopsignup.objects.get(phone=ph)
                    return redirect(shop_extras,obj.id) 
        else:
            messages.info(r,"Passwords are not matching",extra_tags="signup")
            return redirect(shop_login)                     
    return render(r,'shops/shp_index.html',{'shps':shps})

#shop-login
def shop_login(r):
    if r.method=='POST':
        u = r.POST.get('username')
        p = r.POST.get('password')
        print(u,p)
        if shopsignup.objects.filter(username=u).exists():
            shp_usr=shopsignup.objects.get(username=u)
            if shp_usr.password==p:
                if shp_usr.permission=='pending':
                    messages.info(r,"Your Account is waiting for approval",extra_tags="login")
                elif shp_usr.permission=='rejected':
                    messages.info(r,"Your Account is blocked",extra_tags="login")
                else:
                    r.session['shpid']=[shp_usr.id,shp_usr.username,shp_usr.phone,shp_usr.shopname,shp_usr.email]
                    return redirect(shop_extras,r.session['shpid'][0])
            else:
                messages.info(r,"Incorrect Password",extra_tags="login")
        else:
            messages.info(r,"Invalid User",extra_tags="login")


    return render(r,'shops/shp_login.html')

def shop_extras(r,id):
    shp=shopsignup.objects.get(pk=id)
    usr_extras = shop_details.objects.filter(my_shop_id=shp).first()
    stck = orderitem.objects.filter(product__my_shop=shp)
    print(stck)
    vals=[i.product for i in stck if (i.product.stck<10 and i.stck_chnge==0) ]
    tot=len(vals)
    print(vals)   

    if r.method=='POST':
        shp_owner=r.POST.get('name')
        owner_pic=r.FILES.get('owner_pic')
        shop_description=r.POST.get('desc')
        own=shop_details.objects.create(my_shop=shp,shp_owner=shp_owner,owner_pic=owner_pic,shop_description=shop_description)
        own.save()
        return redirect(shop_extras,shp.id)
    return render(r,'shops/shop_extras.html',{'shp':shp,'det':usr_extras,'stck':vals,'tot':tot})


def stckupdate(r,id):    
    pdct=products.objects.get(pk=id)
    st=orderitem.objects.filter(product=pdct)
    print("ST",st)
    stck=pdct.stck
    print(pdct.name,pdct.my_shop.shopname)
    # se = r.session.get('shpid')
    # val=se[0]
    # shp = shopsignup.objects.get(id=val)
    # stck = orderitem.objects.filter(Q(product__my_shop=shp) & Q(stck_chnge==False))
    if r.method=='POST':
        for i in st:
            if i.stck_chnge==0 and i.product.stck==stck:
                i.stck_chnge=1
                i.save()
        pdct.stck=pdct.stck+int(r.POST.get('stck'))
        pdct.save()
        
        return redirect(shop_extras,pdct.my_shop.id)
    return HttpResponse(f'fot id-{id}')


def shop_profileedit(r):
    if 'shpid' in r.session:
        se = r.session.get('shpid')
        val=se[0]
        usr = shopsignup.objects.get(id=val)
        usr_extras = shop_details.objects.filter(my_shop_id=usr).first()
        
        try:
            print(usr_extras.shp_owner)
            if r.method == 'POST':
             
                usr_extras.shp_owner = r.POST.get('name')
                usr_extras.my_shop.email = r.POST.get('email')
                usr_extras.my_shop.phone = r.POST.get('phone')
                usr_extras.shop_description=r.POST.get('desc')

                pic = r.FILES.get('img')
                
                if pic == None:
                    usr_extras.save()
                else:
                    usr_extras.owner_pic=pic
                    usr_extras.save()

      
        except:
            url=f'shop_extras/{val}'
            msg='''
            <script>
            alert('Hi %s,you have to set the below details...,please give the details and check here..')
            window.location='%s'
            </script>
            '''%(usr.shopname,url)
            return HttpResponse(msg)

        return render(r,'shops/shop_profileedit.html',{'det':usr_extras})


def shop_change(r):
    if 'shpid' in r.session:
        se = r.session.get('shpid')
        val=se[0]
        usr = shopsignup.objects.get(id=val)
        if r.method == 'POST':
            srform=shopcrededit(r.POST,r.FILES,instance=usr)
            print("HELLO")
            if srform.is_valid():
                print("HELLO")
                if shopmsg.objects.filter(my_shop=usr).exists():
                    sh=shopmsg.objects.get(my_shop=usr)
                    sh.shopname=srform.cleaned_data['shopname']
                    sh.shop_pic=srform.cleaned_data['shop_pic']
                    sh.shop_license=srform.cleaned_data['shop_license']
                    sh.save()
                else:
                    sh=shopmsg.objects.create(my_shop=usr,shopname=srform.cleaned_data['shopname'],
                    shop_pic=srform.cleaned_data['shop_pic'],shop_license=srform.cleaned_data['shop_license'])
                    sh.save()
                url=f'shop_reg'
                msg='''
                    <script>
                    alert('Hi user-%s,your details has sent to admin,wait for the approval..')
                    window.location-'%s'
                    </script>
                    '''%(usr.shopname,url)
                return HttpResponse(msg)
            else:
                url=f'shop_reg'
                msg='''
                <script>
                alert('Hi user-%s,your details has not sent to admin..')
                window.location-'%s'
                </script>
                '''%(usr.shopname,url)
                return HttpResponse(msg)
                
         

        return render(r,"shops/shop_namepicedit.html",{'usr':usr})

def allshops(r):
    shops = shop_details.objects.all()

    return render(r,'shops/allshops.html',{'shps':shops})


def shop_logout(r):
    if 'shpid' in r.session:
        r.session.flush()
        return redirect(shop_reg)
    return redirect(shop_reg)


def addproduct(a2):
    if 'shpid' in a2.session:
        se = a2.session.get('shpid')
        val=se[0]
        shp=shopsignup.objects.get(id=val)
        if a2.method=='POST':
            n=a2.POST.get('name')
            dc=a2.POST.get('description')
            f=a2.POST.get('features')
            p=a2.POST.get('price')
            d=a2.POST.get('discount')
            c=a2.POST.get('category')
            st=a2.POST.get('stck')
            img=a2.FILES.get('img')
            obj = products.objects.create(name=n,price=p,description=dc,features=f,discount=d,category=c,image=img,stck=st,my_shop=shp)
            obj.save()
            return redirect(shop_reg) 
    else:
        url=f'shop_reg'
        msg='''
            <script>
            alert('Hi user,you have to login first..')
            window.location='%s'
            </script>
            '''%url
        return HttpResponse(msg)
    return render(a2,'shops/add-product.html')


def myproduct(r):
    if 'shpid' in r.session:
        se = r.session.get('shpid')
        val=se[0]
        shp=shopsignup.objects.get(id=val)
        pdct=products.objects.filter(my_shop=shp)
        print(pdct)
        shpown=shop_details.objects.get(my_shop=shp)
    return render(r,'shops/products.html',{'own':shpown,'pdct':pdct})

def editproduct(a2,wal):
    obj = products.objects.filter(id=wal).first()
    if a2.method=='POST':
        obj.name=a2.POST.get('name')
        obj.description=a2.POST.get('description')
        obj.features=a2.POST.get('features')
        obj.stck=a2.POST.get('stck')
        obj.price=a2.POST.get('price')
        obj.discount=a2.POST.get('discount') 
        obj.category=a2.POST.get('category')
        img = a2.FILES.get('img')
        if img == None:
            obj.save()
        else:
            obj.image=a2.FILES.get('img')
            obj.save()
        return redirect(myproduct)
    return render(a2,'shops/edit-product.html',{'obj':obj})

def deleteproduct(a2,wal):
    obj = products.objects.get(id=wal)
    obj.delete()
    return redirect(myproduct)

def myshare(r):
    if 'shpid' in r.session:
        se = r.session.get('shpid')
        val=se[0]
        shp=shopsignup.objects.get(id=val)
        o = orderitem.objects.filter(product__my_shop=shp)
        tot=0
        print(o)
        for i in o:
            tot=tot+(i.price*i.quantity)
            print(i.product.stck,i.product,i.price,i.quantity)
        return render(r,'shops/myshare.html',{'o':o,'tot':tot})
    return render(r,'shops/myshare.html')


# ------------------- SHOP PAGES FUNCTIONS ENDS ---------------------
# Single product

def single(r6,wal):
    if 'id' in r6.session:
        se = r6.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id = val)
        c = mycart.objects.filter(usr=val).all()
        g=[]
        for i in c:
            g.append(i.products)

        cnt = c.count()
        l=products.objects.filter(id=wal).first()
        return render(r6,'shop-single.html',{'l':l,'cnt':cnt,"usr":usr,'c':c,'g':g})
    else:
        l=products.objects.filter(id=wal).first()
        return render(r6,'shop-single.html',{'l':l})

# Category page

def shop(r7):
    if 'id' in r7.session:
        se = r7.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id = val)
        c = mycart.objects.filter(usr=val).all()
        g=[]
        for i in c:
            g.append(i.products_id)
        cnt = c.count()
        return render(r7,'shop.html',{'cnt':cnt,"usr":usr,'g':g})
    else:
        return render(r7,'shop.html')

##########################



# Sub pages - Category

def medicines(r10):
    if 'id' in r10.session:
        se = r10.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id = val)
        c = mycart.objects.filter(usr=val).all()
        g=[]
        for i in c:
            g.append(i.products_id)
        cnt = c.count()
        l=products.objects.all()
        return render(r10,'shop-list.html',{'l':l,'cnt':cnt,"usr":usr,'g':g })
    else:
        l=products.objects.all()
        return render(r10,'shop-list.html',{'l':l})

def diabetes(r10):
    if 'id' in r10.session:
        se = r10.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id = val)
        c = mycart.objects.filter(usr=val).all()
        cnt = c.count()
        obj=products.objects.all()
        l=[]
        for i in obj:
            if i.category=='a':
                l.append(i)
        return render(r10,'shop-list.html',{'l':l,'cnt':cnt,"usr":usr})
    else:
        obj=products.objects.all()
        l=[]
        for i in obj:
            if i.category=='a':
                l.append(i)
        return render(r10,'shop-list.html',{'l':l})

def health(r10):
    if 'id' in r10.session:
        se = r10.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id = val)
        c = mycart.objects.filter(usr=val).all()
        cnt = c.count()
        obj=products.objects.all()
        l=[]
        for i in obj:
            if i.category=='b':
                l.append(i)
        return render(r10,'shop-list.html',{'l':l,'cnt':cnt,"usr":usr})
    else:
        obj=products.objects.all()
        l=[]
        for i in obj:
            if i.category=='b':
                l.append(i)
        return render(r10,'shop-list.html',{'l':l})
    
def pain(r10):
    if 'id' in r10.session:
        se = r10.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id = val)
        c = mycart.objects.filter(usr=val).all()
        cnt = c.count()
        obj=products.objects.all()
        l=[]
        for i in obj:
            if i.category=='c':
                l.append(i)
        return render(r10,'shop-list.html',{'l':l,'cnt':cnt,"usr":usr})
    else:
        obj=products.objects.all()
        l=[]
        for i in obj:
            if i.category=='c':
                l.append(i)
        return render(r10,'shop-list.html',{'l':l})

def ayurveda(r10):
    if 'id' in r10.session:
        se = r10.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id = val)
        c = mycart.objects.filter(usr=val).all()
        cnt = c.count()
        obj=products.objects.all()
        l=[]
        for i in obj:
            if i.category=='d':
                l.append(i)
        return render(r10,'shop-list.html',{'l':l,'cnt':cnt,"usr":usr})
    else:
        obj=products.objects.all()
        l=[]
        for i in obj:
            if i.category=='d':
                l.append(i)
        return render(r10,'shop-list.html',{'l':l})

def homeo(r10):
    if 'id' in r10.session:
        se = r10.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id = val)
        c = mycart.objects.filter(usr=val).all()
        cnt = c.count()
        obj=products.objects.all()
        l=[]
        for i in obj:
            if i.category=='e':
                l.append(i)
        return render(r10,'shop-list.html',{'l':l,'cnt':cnt,"usr":usr})
    else:
        obj=products.objects.all()
        l=[]
        for i in obj:
            if i.category=='e':
                l.append(i)
        return render(r10,'shop-list.html',{'l':l})

def derma(r10):
    if 'id' in r10.session:
        se = r10.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id = val)
        c = mycart.objects.filter(usr=val).all()
        cnt = c.count()
        obj=products.objects.all()
        l=[]
        for i in obj:
            if i.category=='f':
                l.append(i)
        return render(r10,'shop-list.html',{'l':l,'cnt':cnt,"usr":usr})
    else:
        obj=products.objects.all()
        l=[]
        for i in obj:
            if i.category=='f':
                l.append(i)
        return render(r10,'shop-list.html',{'l':l})

def oral(r10):
    if 'id' in r10.session:
        se = r10.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id = val)
        c = mycart.objects.filter(usr=val).all()
        cnt = c.count()
        obj=products.objects.all()
        l=[]
        for i in obj:
            if i.category=='g':
                l.append(i)
        return render(r10,'shop-list.html',{'l':l,'cnt':cnt,"usr":usr})
    else:
        obj=products.objects.all()
        l=[]
        for i in obj:
            if i.category=='g':
                l.append(i)
        return render(r10,'shop-list.html',{'l':l})

def baby(r10):
    if 'id' in r10.session:
        se = r10.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id = val)
        c = mycart.objects.filter(usr=val).all()
        cnt = c.count()
        obj=products.objects.all()
        l=[]
        for i in obj:
            if i.category=='h':
                l.append(i)
        return render(r10,'shop-list.html',{'l':l,'cnt':cnt,"usr":usr})
    else:
        obj=products.objects.all()
        l=[]
        for i in obj:
            if i.category=='h':
                l.append(i)
        return render(r10,'shop-list.html',{'l':l})

def vitamins(r10):
    if 'id' in r10.session:
        se = r10.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id = val)
        c = mycart.objects.filter(usr=val).all()
        cnt = c.count()
        obj=products.objects.all()
        l=[]
        for i in obj:
            if i.category=='i':
                l.append(i)
        return render(r10,'shop-list.html',{'l':l,'cnt':cnt,"usr":usr})
    else:
        obj=products.objects.all()
        l=[]
        for i in obj:
            if i.category=='i':
                l.append(i)
        return render(r10,'shop-list.html',{'l':l})

def sports(r10):
    if 'id' in r10.session:
        se = r10.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id = val)
        c = mycart.objects.filter(usr=val).all()
        cnt = c.count()
        obj=products.objects.all()
        l=[]
        for i in obj:
            if i.category=='j':
                l.append(i)
        return render(r10,'shop-list.html',{'l':l,'cnt':cnt,"usr":usr})
    else:
        obj=products.objects.all()
        l=[]
        for i in obj:
            if i.category=='j':
                l.append(i)
        return render(r10,'shop-list.html',{'l':l})

def family(r10):
    if 'id' in r10.session:
        se = r10.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id = val)
        c = mycart.objects.filter(usr=val).all()
        cnt = c.count()
        obj=products.objects.all()
        l=[]
        for i in obj:
            if i.category=='k':
                l.append(i)
        return render(r10,'shop-list.html',{'l':l,'cnt':cnt,"usr":usr})
    else:
        obj=products.objects.all()
        l=[]
        for i in obj:
            if i.category=='k':
                l.append(i)
        return render(r10,'shop-list.html',{'l':l})

def supports(r10):
    if 'id' in r10.session:
        se = r10.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id = val)
        c = mycart.objects.filter(usr=val).all()
        cnt = c.count()
        obj=products.objects.all()
        l=[]
        for i in obj:
            if i.category=='l':
                l.append(i)
        return render(r10,'shop-list.html',{'l':l,'cnt':cnt,"usr":usr})
    else:
        obj=products.objects.all()
        l=[]
        for i in obj:
            if i.category=='l':
                l.append(i)
        return render(r10,'shop-list.html',{'l':l})


# ------------------- SHOP PAGES FUNCTIONS ENDS --------------------- 
##########################



# ------------------- ADMIN FUNCTIONS STARTS ---------------------

# Admin dashboard
#shops
def shops(r):
    obj=shopsignup.objects.all()
    app=0
    pen=0
    rej=0
    for i in obj:
        if i.permission=='approved':
            app=app+1
        elif i.permission=='pending':
            pen=pen+1
        else:
            rej=rej+1
    tot=[app,pen,rej]
    return render(r,'myadmin/shopss.html',{'obj':obj,'tot':tot})

def approve(r):
    # o = shopsignup.objects.all()    
    p=shop_details.objects.all()
    if r.method=='POST':
        st=r.POST.get('status')
        print("STATUS",st)
        
        p=shop_details.objects.filter(my_shop__permission__contains=st)


    return render(r,'myadmin/approval.html',{'o':p})

def permissionup(r,id):
    if r.method == "POST":
        st = shopsignup.objects.get(pk=id)
        st.permission = r.POST.get('status')
        st.save()
        return redirect(approve)



def adminindex(a2):
    obj = products.objects.all()
    usr = usersignup.objects.all()
    shps=shopsignup.objects.all()
    app=0
    pen=0
    rej=0
    objc = 0
    usrc = 0
    for i in obj:
        objc = objc + 1
    for j in usr:
        usrc = usrc + 1
    for i in shps:
        if i.permission=='approved':
            app=app+1
        elif i.permission=='pending':
            pen=pen+1
        else:
            rej=rej+1
    tot=[app+pen+rej,app,pen,rej]
    return render(a2,'myadmin/index.html',{'objc':objc,'usrc':usrc,'shpdetls':tot})

def adminpro(a2):
    obj=products.objects.all()
    return render(a2,'myadmin/products.html',{'obj':obj})

def bs(a2):
    return render(a2,'myadmin/base.html')

def detlschange(r,id):
    msg=shopmsg.objects.get(pk=id)
    msg.my_shop.shopname=msg.shopname
    msg.my_shop.shop_pic=msg.shop_pic
    msg.my_shop.shop_license=msg.shop_license
    msg.my_shop.save()
    msg.delete()
    return redirect(mess1)









def userss(a2):
    obj = usersignup.objects.all()
    return render(a2,'myadmin/users.html',{'obj':obj})


def userbookings(a2):
    o = order.objects.all()   
    sh = orderitem.objects.all()
    tot=0
    print(sh)

    for i in sh:
        tot=tot+(i.price*i.quantity)
        
    return render(a2,'myadmin/userbookings.html',{'o':o,'sh':sh,'tot':tot})

def statusup(r,wal):
    if r.method == "POST":
        st = order.objects.get(id=wal)
        st.status = r.POST.get('status')
        st.save()
        return redirect(userbookings)

def mess1(r):
    l=msg.objects.all()
    sh=shopmsg.objects.all()
    return render(r,'myadmin/messages.html',{'l':l,'sh':sh})

def reply(r,em):
    l=msg.objects.filter(id=em).first()
    return render(r,"myadmin/replymail.html",{'l':l})
 
def replymail(r,em):
    if r.method=='POST':
        l=msg.objects.filter(id=em).first()
        n=r.POST.get('message')
        try:
            send_mail('Reply from PHARMA', f'{n}','settings.EMAIL_HOST_USER', [l.email],fail_silently=False)
            return redirect(mess1)
        except:
            ms = "NETWORK CONNECTION FAILED"
            return render(r, 'myadmin/replymail.html',{"ms":ms})
        
    return render(r, 'myadmin/replymail.html')

def deletemsg(r,em):
    l=msg.objects.get(id=em)
    l.delete()
    return redirect(mess1)

def adsingle(r6,wal):
    if 'id' in r6.session:
        se = r6.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id = val)
        c = mycart.objects.filter(usr=val).all()
        cnt = c.count()
        l=products.objects.filter(id=wal).first()
        return render(r6,'myadmin/single.html',{'l':l,'cnt':cnt,"usr":usr,'c':c})
    else:
        l=products.objects.filter(id=wal).first()
        return render(r6,'myadmin/single.html',{'l':l})



# Admin dashboard end
 
# ------------------- ADMIN FUNCTIONS ENDS ---------------------


def profileedit(r):
    if 'id' in r.session:
        se = r.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id=val)
        c = mycart.objects.filter(usr=val).all()
        cnt = c.count()
        pro = profilepic.objects.filter(user=usr).first()
        if r.method == 'POST':
            usr.name = r.POST.get('name')
            usr.email = r.POST.get('email')
            usr.phone = r.POST.get('phone')
            pic = r.FILES.get('img')
            if pic == None:
                usr.save()
            else:
                if pro:
                    pro.user = usr
                    pro.propic = pic
                    usr.save()
                    pro.save()
                else:
                    cr = profilepic.objects.create(user=usr,propic=pic)
                    cr.save()
            return redirect(index)
        return render(r,'profileedit.html',{'usr':usr,'pro':pro,'cnt':cnt})
    return render(r,'profileedit.html')

def change(r):
    if 'id' in r.session:
        se = r.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id=val)
        c = mycart.objects.filter(usr=val).all()
        cnt = c.count()
        if r.method == 'POST':
            o = r.POST.get('opass')
            n = r.POST.get('npass')
            rp = r.POST.get('rpass')
            if o == usr.password:
                try:
                    y=re.search("(?=.{8,})(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[~!@#$%^&*?])",n)
                    if y==None:
                        messages.info(r,"Password is not strong")
                        return redirect(change)
                    else:
                        if n==rp:
                            usr.password=n
                            usr.save()
                            return redirect(profileedit)
                        else:
                            messages.info(r,"Password doesnt match")
                            return redirect(change) 
                except:
                    messages.info(r,"Invalid input")
                
            else:
                messages.info(r,"Incorrect old password")
                return redirect(change) 

        return render(r,"changepswd.html",{'usr':usr,'cnt':cnt})

# ------------------- PASSWORD FUNCTIONS STARTS ---------------------


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = usersignup.objects.get(email=email)
        except:
            messages.info(request,"Email id not registered")
            return redirect(forgot_password)
        # Generate and save a unique token
        token = get_random_string(length=4)
        PasswordReset.objects.create(user=user, token=token)

        # Send email with reset link
        reset_link = f'http://127.0.0.1:8000/reset/{token}'
        try:
          
            send_mail('Reset Your Password of User Account', f'Click the link to reset your password: {reset_link}','settings.EMAIL_HOST_USER', [email],fail_silently=False)
            
            msg=f'''Hi {user.name},Email has sent to your registered mail-id {user.email} ,
            check your inbox and please click the given link to reset password..'
            '''
            print("ALL")
            messages.info(request,msg)


        except:
            messages.info(request,"Network connection failed")
            return redirect(forgot_password)
        

    return render(request, 'password_reset_sent.html')

# def resetpage(r,token):
#     return render(r, 'reset_password.html')

def reset_password(request, token):
    # Verify token and reset the password
    password_reset = PasswordReset.objects.get(token=token)
    usr = usersignup.objects.get(id=password_reset.user_id)
    return render(request, 'reset_password.html',{'token':token})

def reset_password2(request, token):
    # Verify token and reset the password
    print(token)
    password_reset = PasswordReset.objects.get(token=token)
    usr = usersignup.objects.get(id=password_reset.user_id)
    if request.method == 'POST':
        new_password = request.POST.get('newpassword')
        repeat_password = request.POST.get('repeatpassword')
        if repeat_password == new_password:
            password_reset.user.password = new_password
            password_reset.user.save()
            password_reset.delete()
            return redirect(login)
        else:
            messages.info(request,"Passwords doesnot match")
    return render(request, 'reset_password.html')


#-----SHOP USER
def shopforgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = shopsignup.objects.get(email=email)
            print("USER",user,user.email,email)
        except:
            messages.info(request,"Email id not registered")
            return redirect(shopforgot_password)
        # Generate and save a unique token
        token = get_random_string(length=4)
        shopPasswordReset.objects.create(user=user, token=token)

        # Send email with reset link
        reset_link = f'http://127.0.0.1:8000/shopreset/{token}'
        try: 
            send_mail('Reset Your Password of Shop Account', f'Click the link to reset your password: {reset_link}','settings.EMAIL_HOST_USER', [email],fail_silently=False)
            msg=f'''Hi {user.username},Email has sent to your registered mail-id {user.email} ,
            check your inbox and please click the given link to reset password..'
            '''
            print("ALL")
            messages.info(request,msg)
            

        except:
            messages.info(request,"Network connection failed")
            return redirect(shopforgot_password)

    return render(request, 'shops/password_reset_sent.html')

# def resetpage(r,token):
#     return render(r, 'reset_password.html')

def shopreset_password(request, token):
    # Verify token and reset the password
    password_reset = shopPasswordReset.objects.get(token=token)
    usr = shopsignup.objects.get(id=password_reset.user_id)

    if request.method == 'POST':
        new_password = request.POST.get('newpassword')
        repeat_password = request.POST.get('repeatpassword')
        if repeat_password == new_password:
            password_reset.user.password = new_password
            password_reset.user.save()
            password_reset.delete()
            return redirect(shop_login)
        else:
            messages.info(request,"Passwords doesnot match")
    return render(request, 'shops/reset_password.html')

# ------------------- PASSWORD FUNCTIONS ENDS ---------------------





# ------------------- PAYMENT FUNCTIONS STARTS ---------------------



def placeorder(r):
    if 'id' in r.session:
        se = r.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id = val)
        c = mycart.objects.filter(usr=val).all()
        t=0
        for i in c:
            t=t+(i.products.discount*i.quantity)
        if r.method == 'POST':   
            if r.POST.get('save')=='save':
                fname = r.POST.get('fname')
                lname = r.POST.get('lname')
                email = r.POST.get('email')
                phone = r.POST.get('phone')
                address = r.POST.get('address')
                city = r.POST.get('city')
                state = r.POST.get('state')
                country = r.POST.get('country')
                pincode = r.POST.get('pincode')
                pro = profile.objects.filter(user=usr).first()  
                if pro:
                    
                    pro.fname = r.POST.get('fname')
                    pro.lname = r.POST.get('lname')
                    pro.email = r.POST.get('email')
                    pro.phone = r.POST.get('phone')
                    pro.address = r.POST.get('address')
                    pro.city = r.POST.get('city')
                    pro.state = r.POST.get('state')
                    pro.country = r.POST.get('country')
                    pro.pincode = r.POST.get('pincode')
                    pro.save()
                else:
                    cr = profile.objects.create(user=usr,fname=fname,lname=lname,email=email,phone=phone,address=address,city=city,state=state,country=country,pincode=pincode)
                    cr.save()
                return redirect(placeorder)
            else:
                neworder = order()
                neworder.user = usr
                neworder.fname = r.POST.get('fname')
                neworder.lname = r.POST.get('lname')
                neworder.email = r.POST.get('email')
                neworder.phone = r.POST.get('phone')
                neworder.address = r.POST.get('address')
                neworder.city = r.POST.get('city')
                neworder.state = r.POST.get('state')
                neworder.country = r.POST.get('country')
                neworder.pincode = r.POST.get('pincode')

                neworder.total_price = t

                neworder.payment_mode = r.POST.get('payment_mode')
                neworder.payment_id = r.POST.get('payment_id')

                trackno = 'pharma'+str(random.randint(1111111,9999999))
                while order.objects.filter(tracking_no=trackno) is None:
                    trackno = 'pharma'+str(random.randint(1111111,9999999))
                neworder.tracking_no = trackno
                neworder.save()

                for item in c:
                    orderitem.objects.create(
                        orderdet = neworder,
                        product = item.products,
                        price = item.products.discount,
                        quantity = item.quantity
                    )

                mycart.objects.filter(usr=val).delete()

                messages.success(r, 'Your order has been placed successfully')
                stck = orderitem.objects.all()
                l=[]
                for i in stck:
                    print("B4",i.product.stck)
                    if i.stck_chnge==0:
                        i.product.stck=i.product.stck-i.quantity
                        i.product.save()
                    print("AFTR",i.product.stck)


                payMode = r.POST.get('payment_mode')
                if payMode == "Razorpay":
                    return JsonResponse({'status':'Your order has been placed successfully'})

        return redirect(checkout)
    

def razorpaycheck(r):
    if 'id' in r.session:
        se = r.session.get('id')
        val = se[0]
        c = mycart.objects.filter(usr=val).all()
        t=0
        for i in c:
            t=t+(i.products.discount*i.quantity)

    return JsonResponse({
        'total_price':t
    })

def orderss(r):
    if 'id' in r.session:
        se = r.session.get('id')
        val = se[0]
        usr = usersignup.objects.get(id=val)
        o = order.objects.all()
        l=[]
        for i in o:
            if i.user==usr:
                l.append(i)
        return render(r,'myorders.html',{'l':l})
    return render(r,'myorders.html')