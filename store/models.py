from django.db import models
from django.utils import timezone


class Item(models.Model):
    STATUS_CHOICES = [
        ("OK", "OK"), #left side is how it's stored in database, right side is  how it's shown to user
        ("LOW", "Low Stock"),
        ("OUT", "Out of Stock"),
    ]

    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="OK")
    date_added = models.DateTimeField(auto_now_add=True)                            #It never updates again. It is basically a "created at" timestamp for the item.
    reorder_level = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["name"]     #tells Django that when you ask for a list of Items,  it should sort them by the name field in ascending order

    def __str__(self):          #When you print an Item object, Django will show its name, such as "Cement 50kg Bag".
        return self.name

    @property               #It means you can use it like a field, for example item.total_value, without calling it like a function.
    def total_value(self):
        return self.quantity * self.unit_price


class Supplier(models.Model):
    name = models.CharField(max_length=150)
    contact_person = models.CharField(max_length=150, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)   #means new suppliers start as active by default
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        ordering = ["name"]  #orders suppliers ascending order alphabetically by name


    def __str__(self):
        return self.name


class Client(models.Model):
    name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class SupplierOrder(models.Model):
    
    STATUS_CHOICES = [                      #variable to declare different status options for supplier orders
        ("PENDING", "Pending"),
        ("RECEIVED", "Received"),
        ("CANCELLED", "Cancelled"),
    ]

    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL,  null=True, blank=True)             #each SupplierOrder is linked to a specific supplier, but one supplier can have multiple orders.f someone tries to delete a supplier that has orders, it sets null.
    item = models.ForeignKey(       #links each order to one Item.
        Item,
        on_delete=models.SET_NULL, null=True, blank=True)
    
    quantity_ordered = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING",)
    ordered_at = models.DateField(auto_now_add=True, null=True, blank=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["-ordered_at"]     #Orders will be returned sorted by date in descending order.The minus sign means "newest first".

    def __str__(self):
        supplier_name = self.supplier.name if self.supplier else "Unknown supplier"
        return f"Order #{self.id} - {supplier_name}"   #self.id is the primary key auto integer.self.supplier.name shows the linked supplier name.

    @property
    def total_cost(self):     #not saved in the database, just computed when needed.
        return self.quantity_ordered * self.unit_price


class StockIssue(models.Model):     # SET_NULL must be combined with null=True (and usually blank=True)
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True,
        blank=True,)               # if Item is deleted, set item = NULL
    client = models.ForeignKey(          #this is optional relationship of issue to a Client
        Client,
        on_delete=models.SET_NULL,       # if Client is deleted, set client = NULL
        null=True,
        blank=True,
    )
    quantity = models.PositiveIntegerField(default=1)
    issue_date = models.DateField(default=timezone.now, null=True, blank=True)
    issued_by = models.CharField(max_length=150, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["-issue_date"]   #Issues will be listed from newest to oldest.

    def __str__(self):
        client_name = self.client.name if self.client else "N/A"         # item can now also be None because of SET_NULL
        item_name = self.item.name if self.item else "Item deleted"
        return f"Issue #{self.id} - {item_name} to {client_name}"


class PaymentRecord(models.Model):
    METHOD_CHOICES = [
        ("MPESA", "M-Pesa"),
        ("PAYPAL", "PayPal"),
        ("PAYSTACK", "Paystack"),
        ("CASH", "Cash"),
    ]

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("SUCCESS", "Success"),
        ("FAILED", "Failed"),
    ]

    order = models.ForeignKey(   #relationship to SupplierOrder
        "SupplierOrder",
        on_delete=models.SET_NULL,          #means if someone deletes the SupplierOrder, this payment record will stay, but its order field will be set to NULL.
        null=True,                          #means the payment can exist without being tied to an order.
        blank=True,                         #means the payment can exist without being tied to an order.
        related_name="payments",
    )
    method = models.CharField(max_length=20, choices=METHOD_CHOICES)      #Which payment method was used.
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING",
    )
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        help_text="Phone used for payment, for example M-Pesa number.",
    )
    reference = models.CharField(
        max_length=100,
        blank=True,
        help_text="Payment reference or transaction code.",
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]     #Payment records will appear from newest to oldest.

    def __str__(self):
        return f"{self.method} {self.amount} ({self.status})"
