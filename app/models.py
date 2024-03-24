from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


# phan loai sp
class Category(models.Model):
    sub_category = models.ForeignKey('self' , on_delete= models.CASCADE , related_name='sub_categories',null = True,blank=True)
    is_sub = models.BooleanField(default=False)
    name = models.CharField(max_length=200,null=True)
    slug = models.SlugField(max_length=200,unique=True)
    def __str__(self):
        return self.name

#thay doi form django
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','password1','password2']

# tt sp
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ManyToManyField(Category,related_name='product')
    name = models.CharField(max_length = 200 , null = True)
    price = models.FloatField()
    difital = models.BooleanField(default=False,null=True,blank=False)
    image = models.ImageField(null = True, blank= True)
    detail = models.TextField(null=True,blank=True)
    # Thêm trường nhà cung cấp
    supplier = models.ForeignKey('Supplier', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Thêm trường số lượng
    quantity = models.IntegerField(default=0, null=True, blank=True)
    def __str__(self) :

        return self.name
    @property 
    def ImageURL(self):
        try :
            url = self.image.url
        except :
            url = ''
        return url
    
# tt don hang
class Order(models.Model):
    customer = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)
    date_order = models.DateTimeField(auto_now_add=True)

    # ham kiem tra don hang thanh cong hay k
    complete = models.BooleanField(default=False,null=True,blank=False)
    transaction_id = models.CharField(max_length=200,null=True)
    
    def __str__(self) :

        return str(self.id)
    
    # ham tinh tong hang mua
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    
    # ham tinh tong tien
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

# tt sp mua
class OrderItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,blank=True,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property 
    def get_total(self):
        total = self.product.price * self.quantity
        return total

# tt nguoi mua
class ShippingAddress(models.Model):
    customer = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    
    address = models.CharField(max_length=200,null=True)
    city = models.CharField(max_length=200,null=True)
    state = models.CharField(max_length=200,null=True)
    mobile = models.CharField(max_length=10,null=True)
    

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

#tt nha cung cap
class Supplier(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.name

#tthoa don
class Invoice(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    customer_name = models.CharField(max_length=255)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=15)
    customer_address = models.TextField()
    order_items = models.ManyToManyField('OrderItem')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f'Invoice for {self.customer_name}'