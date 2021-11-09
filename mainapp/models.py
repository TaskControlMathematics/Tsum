from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField


class Categories(models.Model):
    category = models.TextField()
    id_parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.category
        # full_path = [self.category]
        # k = self.id_parent
        # while k is not None:
        #     full_path.append(k.category)
        #     k = k.id_parent
        # return ' -> '.join(full_path[::-1])


class Product(models.Model):
    title = models.CharField(max_length=256, blank=True, null=True)
    brand = models.CharField(max_length=256, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    color = models.CharField(max_length=200, null=True, blank=True)
    in_stock = models.BooleanField(null=True, blank=True)
    category = models.ForeignKey(Categories, blank=True, null=True, on_delete=models.CASCADE)
    category_tree = models.CharField(max_length=256, blank=True, null=True)
    image_array = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return self.title


class ProductInBasket(models.Model):
    session_key = models.CharField(max_length=128, default=None)
    product = models.ForeignKey(Product, blank=True, null=True, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)
    total_price = models.IntegerField(default=0)
    price_per_item = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Товар в корзине"
        verbose_name_plural = "Товары в корзине"

    def save(self, *args, **kwargs):
        price_per_item = int(self.product.price)
        self.price_per_item = price_per_item

        self.total_price = int(self.count) * self.price_per_item

        super(ProductInBasket, self).save(*args, **kwargs)


class Order(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, default=None, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    sirname = models.CharField(max_length=256)
    email = models.EmailField()
    phone = models.CharField(max_length=256)
    comment = models.TextField()
    delivery = models.TextField()
    total_price = models.IntegerField(default=0)

    def __str__(self):
        return "Заказ %s " % self.id

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def save(self, *args, **kwargs):
        super(Order, self).save(*args, **kwargs)


class ProductInOrder(models.Model):
    order = models.ForeignKey(Order, blank=True, null=True, default=None, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, blank=True, null=True, default=None, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)
    total_price = models.IntegerField(default=0)
    price_per_item = models.IntegerField(default=0)

    def __str__(self):
        return "%s" % self.product.title

    class Meta:
        verbose_name = "Товар в заказе"
        verbose_name_plural = "Товары в заказе"

    def save(self, *args, **kwargs):
        price_per_item = self.product.price
        self.price_per_item = price_per_item

        self.total_price = self.count * self.price_per_item

        super(ProductInOrder, self).save(*args, **kwargs)
