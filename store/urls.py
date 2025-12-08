from django.urls import path
from . import views

app_name = "store"

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),

    # items
    path("items/", views.item_list, name="item_list"),
    path("items/add/", views.item_create, name="item_create"),
    path("items/<int:pk>/edit/", views.item_update, name="item_update"),
    path("items/<int:pk>/delete/", views.item_delete, name="item_delete"),

    # suppliers
    path("suppliers/", views.supplier_list, name="supplier_list"),
    path("suppliers/add/", views.supplier_create, name="supplier_create"),
    path("suppliers/<int:pk>/edit/", views.supplier_update, name="supplier_update"),
    path("suppliers/<int:pk>/delete/", views.supplier_delete, name="supplier_delete"),

    # clients
    path("clients/", views.client_list, name="client_list"),
    path("clients/add/", views.client_create, name="client_create"),
    path("clients/<int:pk>/edit/", views.client_update, name="client_update"),
    path("clients/<int:pk>/delete/", views.client_delete, name="client_delete"),

    # orders
    path("orders/", views.order_list, name="order_list"),
    path("orders/add/", views.order_create, name="order_create"),
    path("orders/<int:pk>/edit/", views.order_update, name="order_update"),
    path("orders/<int:pk>/delete/", views.order_delete, name="order_delete"),
    path("orders/<int:order_id>/pay-mpesa/", views.start_mpesa_payment, name="order_pay_mpesa",
    ),

    # issues
    path("issues/", views.issue_list, name="issue_list"),
    path("issues/add/", views.issue_create, name="issue_create"),

    # payments
    path("payments/", views.payment_list, name="payment_list"),
    path("payments/add/", views.payment_create, name="payment_create"),
]
