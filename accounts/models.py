from django.db import models

# Create your models (bảng - table trong sql) here.
# LƯU Ý: sau khi tạo 1 model mới thì cần 'python manage.py makemigrations' để tạo bảng (create table)
## và 'python manage.py migrate' để add bảng vào database (back-end)
## và nhớ register model trong admin.py để thêm bảng lên web (front-end) 

class Customer(models.Model):
	name = models.CharField(max_length=200, null=True) # 'null' cho phép nhập data có trường bị thiếu
	phone = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.name

class Tag(models.Model):
	name = models.CharField(max_length=200, null=True)

	def __str__(self):
		return self.name

class Product(models.Model):
	CATEGORY = (
			('Indoor', 'Indoor'),
			('Out Door', 'Out Door'),
			) 

	name = models.CharField(max_length=200, null=True)
	price = models.FloatField(null=True)
	category = models.CharField(max_length=200, null=True, choices=CATEGORY)
	description = models.CharField(max_length=200, null=True, blank=True) # 'blank': cho phép bỏ trống trường này
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	tags = models.ManyToManyField(Tag) # product thuộc thể loại nào
 
	def __str__(self):
		return self.name

class Order(models.Model):
	STATUS = ( 
			('Pending', 'Pending'),
			('Out for delivery', 'Out for delivery'),
			('Delivered', 'Delivered'),
			)

	customer = models.ForeignKey(Customer, null=True, on_delete= models.SET_NULL) # 'on_delete': nếu xóa customer A trong bảng Customer thì ông A ở table Order nên được treat thế nào? xóa luôn order chứa ông A, hay set trường customer là NULL
	product = models.ForeignKey(Product, null=True, on_delete= models.SET_NULL)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	status = models.CharField(max_length=200, null=True, choices=STATUS) # 'choices' = drop down menu
	
	def __str__(self):
		return self.product.name