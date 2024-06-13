from django.db import models

# Create your models here.

# -------------------------------- USER TABLE -------------------------------

class usersignup(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.IntegerField()
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f'{self.name}'
    
# -------------------------------- SHOP TABLE -------------------------------
class shopsignup(models.Model):
    permchoices = (
        ('aproved','approved'),
        ('pending','pending'),
        ('rejected','rejected')
    )
    shopname = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.IntegerField()
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    shop_pic = models.ImageField(upload_to='shop/shoppic')
    shop_license = models.ImageField(upload_to='shop/license')
    permission= models.CharField(max_length=100,default='pending',choices=permchoices)

    def __str__(self) -> str:
        return f'{self.shopname}'
    

class shop_details(models.Model):
    my_shop=models.ForeignKey(shopsignup,on_delete=models.CASCADE)
    shp_owner=models.CharField(max_length=50)
    owner_pic = models.ImageField(upload_to='shop/owners')
    shop_description = models.TextField()

    def __str__(self) -> str:
        return f'{self.shp_owner}'



# -------------------------------- PRODUCTS -------------------------------

class products(models.Model):
    categorychoices = (
        ('a','Diabetescare'),
        ('b','Healthcare'),
        ('c','Painrelief'),
        ('d','Ayurveda'),
        ('e','Homeopathy'),
        ('f','Dermacare'),
        ('g','Oralcare'),
        ('h','Babycare'),
        ('i','Vitamins'),
        ('j','Sports'),
        ('k','Family'),
        ('l','Supports'),
    )
    my_shop=models.ForeignKey(shopsignup,on_delete=models.CASCADE,default=None)
    name = models.CharField(max_length=500)
    price = models.IntegerField()
    description = models.CharField(max_length=1000)
    features = models.CharField(max_length=1000)
    discount = models.IntegerField()
    stck=models.IntegerField(default=1)
    category = models.CharField(max_length=100,default='a',choices=categorychoices)
    image = models.ImageField(upload_to='images/product')

    def __str__(self) -> str:
        return f'{self.name}'


# -------------------------------- CART TABLE -------------------------------
    
class mycart(models.Model):
    products=models.ForeignKey(products,on_delete=models.CASCADE)
    usr = models.ForeignKey(usersignup,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1) 
    delivered=models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return f'{self.usr}'


# -------------------------------- PASSWORD RESET TABLE -------------------------------

class PasswordReset(models.Model):
    user = models.ForeignKey(usersignup, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

class shopPasswordReset(models.Model):
    user = models.ForeignKey(shopsignup, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


#messages table
class msg(models.Model):
    name=models.CharField(max_length=100)
    mobile=models.IntegerField()
    email=models.EmailField()
    message=models.TextField()

    def __str__(self) -> str:
        return f'{self.name}'
    

class shopmsg(models.Model):
    my_shop=models.ForeignKey(shopsignup,on_delete=models.CASCADE)
    shopname = models.CharField(max_length=50)
    shop_pic = models.ImageField(upload_to='shop/shoppic')
    shop_license = models.ImageField(upload_to='shop/license')

    def __str__(self) -> str:
        return f'{self.shopname}'
#----------ORDERS-----------


class order(models.Model):
    user = models.ForeignKey(usersignup, on_delete=models.CASCADE)
    fname = models.CharField(max_length=150, null=False)
    lname = models.CharField(max_length=150, null=False)
    email = models.CharField(max_length=150, null=False)
    phone = models.CharField(max_length=150, null=False)
    address = models.TextField(null=False)
    city = models.CharField(max_length=150, null=False)
    state = models.CharField(max_length=150, null=False)
    country = models.CharField(max_length=150, null=False)
    pincode = models.CharField(max_length=150, null=False)
    total_price = models.FloatField(null=False)
    payment_mode = models.CharField(max_length=150, null=False)
    payment_id = models.CharField(max_length=150, null=True)
    orderstatus = (
        ('Pending','Pending'),
        ('Out for shipping','Out for shipping'),
        ('Delivered','Delivered'),
        ('Cancelled','Cancelled')
    )
    status = models.CharField(max_length=150,choices=orderstatus, default='pending')
    message = models.TextField(null=True)
    tracking_no = models.CharField(max_length=150,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    def __str__(self) -> str:
        return f'{self.tracking_no}'
    
class orderitem(models.Model):
    orderdet = models.ForeignKey(order,on_delete=models.CASCADE)
    product = models.ForeignKey(products,on_delete=models.CASCADE)
    price = models.FloatField(null=False)
    quantity = models.IntegerField(null=False)
    stck_chnge=models.IntegerField(default=0)

    def __str__(self) -> str:
        return f'{self.orderdet}'


class profile(models.Model):
    user = models.OneToOneField(usersignup,on_delete=models.CASCADE)
    fname = models.CharField(max_length=150, null=False)
    lname = models.CharField(max_length=150, null=False)
    email = models.CharField(max_length=150, null=False)
    phone = models.CharField(max_length=150, null=False)
    address = models.TextField(null=False)
    city = models.CharField(max_length=150, null=False)
    state = models.CharField(max_length=150, null=False)
    country = models.CharField(max_length=150, null=False)
    pincode = models.CharField(max_length=150, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.user.username}'

class profilepic(models.Model):
    user = models.OneToOneField(usersignup,on_delete=models.CASCADE)
    propic = models.ImageField(upload_to='images/profilepic')

    def __str__(self) -> str:
        return f'{self.user.username}'