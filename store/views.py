
from django_daraja.mpesa.core import MpesaClient
from django.conf import settings
from django.contrib import messages #to show short messages
from django.contrib.auth.decorators import login_required   #so user must be logged in before they can view that page.
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render


from .forms import (
    ClientForm,
    ItemForm,
    PaymentRecordForm,
    StockIssueForm,
    SupplierForm,
    SupplierOrderForm,
)
from .models import (
    Client,
    Item,
    PaymentRecord,
    StockIssue,
    Supplier,
    SupplierOrder,
)




@login_required
def main_menu(request):
    return render(request, "store/main_menu.html")




@login_required       #checks "is the user logged in?" If not, they are sent to the login page.
def dashboard(request):    #request is the object that holds everything about the HTTP request,
    items_qs = Item.objects.all()   #like item list from database
    search_query = request.GET.get("search", "").strip()
    if search_query:
        items_qs = items_qs.filter(name__icontains=search_query)

    total_items = items_qs.count()
    total_stock = (
        items_qs.aggregate(total_qty=Sum("quantity"))["total_qty"] or 0
    )
    low_stock_count = items_qs.filter(
        quantity__gt=0, quantity__lte=5
    ).count()
    out_of_stock_count = items_qs.filter(quantity=0).count()
    recent_items = items_qs.order_by("-date_added")[:5]      #.order_by("-date_added") sorts items from newest to oldest.

    supplier_count = Supplier.objects.count()
    client_count = Client.objects.count()
    order_count = SupplierOrder.objects.count()
    pending_payment_count = PaymentRecord.objects.filter(
        status="PENDING"
    ).count()

    context = {
        "items": items_qs.order_by("-date_added"),
        "search_query": search_query,
        "total_items": total_items,
        "total_stock": total_stock,
        "low_stock_count": low_stock_count,
        "out_of_stock_count": out_of_stock_count,
        "recent_items": recent_items,
        "supplier_count": supplier_count,
        "client_count": client_count,
        "order_count": order_count,
        "pending_payment_count": pending_payment_count,
    }
    return render(request, "store/dashboard.html", context)


# Items

@login_required
def item_list(request):
    items = Item.objects.all().order_by("name")
    return render(request, "store/item_list.html", {"items": items})


@login_required
def item_create(request):
    if request.method == "POST":
        form = ItemForm(request.POST)    #if the http response is POST, create this item form filled in with submitted data
        if form.is_valid():
            form.save()
            messages.success(request, "Item saved successfully.")
            return redirect("store:item_list")
    else:
        form = ItemForm()
    return render(
        request,
        "store/item_form.html",
        {"form": form, "mode": "create"},
    )


@login_required
def item_update(request, pk):        #primary key (id) of the item from the URL.
    item = get_object_or_404(Item, pk=pk)           #fetch the item if not tgere show 404 page
    if request.method == "POST":
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Item updated successfully.")
            return redirect("store:item_list")
    else:
        form = ItemForm(instance=item)
    return render(
        request,
        "store/item_form.html",
        {"form": form, "mode": "edit", "item": item},
    )


@login_required
def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == "POST":
        item.delete()
        messages.success(request, "Item deleted.")
        return redirect("store:item_list")
    return render(
        request,
        "store/item_confirm_delete.html",
        {"item": item},
    )


# Suppliers

@login_required
def supplier_list(request):
    suppliers = Supplier.objects.all().order_by("name")   #fetsch all list of suppliers ordered by name
    return render(
        request,
        "store/supplier_list.html",
        {"suppliers": suppliers},
    )


@login_required
def supplier_create(request):
    if request.method == "POST":
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Supplier added successfully.")
            return redirect("store:supplier_list")
    else:
        form = SupplierForm()
    return render(
        request,
        "store/supplier_form.html",
        {"form": form, "mode": "create"},
    )


@login_required
def supplier_update(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == "POST":
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            messages.success(request, "Supplier updated successfully.")
            return redirect("store:supplier_list")
    else:
        form = SupplierForm(instance=supplier)
    return render(
        request,
        "store/supplier_form.html",
        {"form": form, "mode": "edit", "supplier": supplier},
    )


@login_required
def supplier_delete(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == "POST":
        supplier.delete()
        messages.success(request, "Supplier deleted.")
        return redirect("store:supplier_list")
    return render(
        request,
        "store/supplier_confirm_delete.html",
        {"supplier": supplier},
    )


# Clients


@login_required
def client_list(request):
    clients = Client.objects.all().order_by("name")
    return render(
        request,
        "store/client_list.html",
        {"clients": clients},
    )


@login_required
def client_create(request):
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Client added successfully.")
            return redirect("store:client_list")
    else:
        form = ClientForm()
    return render(
        request,
        "store/client_form.html",
        {"form": form, "mode": "create"},
    )


@login_required
def client_update(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == "POST":
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, "Client updated successfully.")
            return redirect("store:client_list")
    else:
        form = ClientForm(instance=client)
    return render(
        request,
        "store/client_form.html",
        {"form": form, "mode": "edit", "client": client},
    )


@login_required
def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == "POST":
        client.delete()
        messages.success(request, "Client deleted.")
        return redirect("store:client_list")
    return render(
        request,
        "store/client_confirm_delete.html",
        {"client": client},
    )


# Supplier orders


@login_required
def order_list(request):
    orders = SupplierOrder.objects.select_related("supplier", "item").order_by(
        "-ordered_at"
    )
    return render(
        request,
        "store/order_list.html",
        {"orders": orders},
    )


@login_required
def order_create(request):
    if request.method == "POST":
        form = SupplierOrderForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Supplier order recorded.")
            return redirect("store:order_list")
    else:
        form = SupplierOrderForm()
    return render(
        request,
        "store/order_form.html",
        {"form": form},
    )



@login_required
def order_update(request, pk):
    order = get_object_or_404(SupplierOrder, pk=pk)

    if request.method == "POST":
        form = SupplierOrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, "Order updated successfully.")
            return redirect("store:order_list")
    else:
        form = SupplierOrderForm(instance=order)

    return render(
        request,
        "store/order_form.html",          # <- keep using order_form.html
        {
            "form": form,
            "order": order,
            "page_title": "Edit supplier order",
        },
    )


@login_required
def order_delete(request, pk):
    order = get_object_or_404(SupplierOrder, pk=pk)

    if request.method == "POST":
        order.delete()
        messages.success(request, "Order deleted.")
        return redirect("store:order_list")

    return render(
        request,
        "store/order_confirm_delete.html",   # <- this template below
        {
            "order": order,
            "page_title": "Delete supplier order",
        },
    )

# Stock issues


@login_required
def issue_list(request):
    issues = StockIssue.objects.select_related("item", "client").order_by(
        "-issue_date"
    )
    return render(
        request,
        "store/issue_list.html",
        {"issues": issues},
    )


@login_required
def issue_create(request):
    if request.method == "POST":
        form = StockIssueForm(request.POST)
        if form.is_valid():
            issue = form.save(commit=False)  #form.save(commit=False) creates a StockIssue object in memory but does not save it to the database yet.This gives you a chance to adjust stock before saving.
            item = issue.item
            if issue.quantity > item.quantity:
                messages.error(
                    request,
                    "Cannot issue more than the current stock quantity.",
                )
            else:
                item.quantity -= issue.quantity
                item.save()
                issue.save()
                messages.success(
                    request,
                    "Issue recorded and stock updated.",
                )
                return redirect("store:issue_list")
    else:
        form = StockIssueForm()
    return render(
        request,
        "store/issue_form.html",
        {"form": form},
    )


@login_required
def issue_update(request, pk):
    issue = get_object_or_404(StockIssue, pk=pk)

    if request.method == "POST":
        form = StockIssueForm(request.POST, instance=issue)
        if form.is_valid():
            form.save()
            messages.success(request, "Issue updated successfully.")
            return redirect("store:issue_list")
    else:
        form = StockIssueForm(instance=issue)

    return render(
        request,
        "store/issue_form.html",
        {
            "form": form,
            "issue": issue,
            "mode": "edit",
        },
    )


@login_required
def issue_delete(request, pk):
    issue = get_object_or_404(StockIssue, pk=pk)

    if request.method == "POST":
        issue.delete()
        messages.success(request, "Issue deleted.")
        return redirect("store:issue_list")

    return render(
        request,
        "store/issue_confirm_delete.html",
        {"issue": issue},
    )








# Payments

@login_required
def payment_list(request):
    payments = PaymentRecord.objects.select_related("order").order_by(
        "-created_at"
    )
    return render(
        request,
        "store/payment_list.html",
        {"payments": payments},
    )


@login_required
def payment_create(request):
    if request.method == "POST":
        form = PaymentRecordForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Payment record saved.")
            return redirect("store:payment_list")
    else:
        form = PaymentRecordForm()
    return render(
        request,
        "store/payment_form.html",
        {"form": form},
    )


# M-Pesa payment for an order

@login_required
def start_mpesa_payment(request, order_id):
    """
    Start a real M-Pesa STK push using django_daraja MpesaClient.
    """
    order = get_object_or_404(SupplierOrder, id=order_id)
    cl = MpesaClient()

    if request.method == "POST":
        phone = request.POST.get("phone_number", "").strip()   #get phone number from user request nd if it doesn't exist, return empty string
        if not phone:
            messages.error(request, "Please enter a phone number.")
            return redirect("store:order_pay_mpesa", order_id=order.id)   #order_id=order.id passes the id into the URL.

        amount = order.total_cost or 1  # If total_cost is None or zero, or 1 ensures there is at least 1. Safaricom cannot process 0 shillings.

        # 1. Create a PaymentRecord first
        payment = PaymentRecord.objects.create(
            order=order,
            method="MPESA",
            amount=amount,
            status="PENDING",
            phone_number=phone,
        )

        # 2. Call Safaricom using MpesaClient
        account_reference = f"Order-{order.id}"
        transaction_desc = "ITEMO IMS payment"
        callback_url = settings.MPESA_CALLBACK_URL

        try:            #Start a block where we will "try" to run some code that might fail.
            response = cl.stk_push(
                phone,
                int(amount),  # amount must be an integer
                account_reference,
                transaction_desc,
                callback_url,
            )
            
            # Print to terminal for debugging
            print("M-Pesa STK raw response:", response)
            
            # Try to extract something readable
            try:
                resp_data = response
            except Exception:
                resp_data = str(response)
            
            # Optional: show part of it in the UI to users
            messages.info(
                request,
                f"M-Pesa response: {resp_data}"
            )
            
            messages.success(
                request,
                "STK push sent. Check your phone for the M-Pesa prompt and enter your PIN."
            )
            
            payment.reference = "MPESA_STK_SENT"
            payment.save()
        
        
        except Exception as e:
            # If anything fails, mark the payment as FAILED
            payment.status = "FAILED"
            payment.reference = "ERROR"
            payment.save()
            messages.error(
                request,
                f"Could not start M-Pesa payment. Reason: {e}"
            )

        return redirect("store:payment_list")

    # GET: show the pay form
    return render(request, "store/order_pay_mpesa.html", {"order": order})








#COMMENTED OUT AS I DECIDED TO USE MpesaClient Instead
# @login_required
# def order_pay_mpesa(request, pk):
#     """
#     Start an M-Pesa STK push (real if credentials are set, otherwise simulated).
#     """
#     order = get_object_or_404(SupplierOrder, pk=pk)
#
#     if request.method == "POST":
#         phone = request.POST.get("phone_number", "").strip()
#         if not phone:
#             messages.error(request, "Please enter a phone number.")
#             return redirect("store:order_pay_mpesa", pk=order.pk)
#
#         amount = float(order.total_cost)
#
#         consumer_key = getattr(settings, "MPESA_CONSUMER_KEY", "")
#         consumer_secret = getattr(settings, "MPESA_CONSUMER_SECRET", "")
#         shortcode = getattr(settings, "MPESA_SHORTCODE", "")
#         passkey = getattr(settings, "MPESA_PASSKEY", "")
#         callback_url = getattr(
#             settings,
#             "MPESA_CALLBACK_URL",
#             "https://example.com/store/mpesa/callback/",
#         )
#
#         mode = "simulation"
#         reference = ""
#         status = "PENDING"
#
#         # Only try real Daraja if credentials are present
#         if consumer_key and consumer_secret and shortcode and passkey:
#             try:
#                 # 1. Get access token
#                 auth_url = (
#                     "https://sandbox.safaricom.co.ke/oauth/v1/generate"
#                     "?grant_type=client_credentials"
#                 )
#                 auth_response = requests.get(
#                     auth_url,
#                     auth=(consumer_key, consumer_secret),
#                     timeout=10,
#                 )
#                 auth_response.raise_for_status()
#                 access_token = auth_response.json().get("access_token")
#
#                 # 2. Build password
#                 timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
#                 data_to_encode = f"{shortcode}{passkey}{timestamp}"
#                 password = base64.b64encode(
#                     data_to_encode.encode()
#                 ).decode()
#
#                 # 3. STK push request
#                 stk_url = (
#                     "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
#                 )
#                 headers = {
#                     "Authorization": f"Bearer {access_token}",
#                     "Content-Type": "application/json",
#                 }
#                 payload = {
#                     "BusinessShortCode": shortcode,
#                     "Password": password,
#                     "Timestamp": timestamp,
#                     "TransactionType": "CustomerPayBillOnline",
#                     "Amount": int(amount),
#                     "PartyA": phone,
#                     "PartyB": shortcode,
#                     "PhoneNumber": phone,
#                     "CallBackURL": callback_url,
#                     "AccountReference": f"ITEMO-ORDER-{order.id}",
#                     "TransactionDesc": "Payment for supplier order",
#                 }
#                 resp = requests.post(
#                     stk_url,
#                     json=payload,
#                     headers=headers,
#                     timeout=10,
#                 )
#                 resp.raise_for_status()
#                 data = resp.json()
#                 reference = data.get("CheckoutRequestID", "")
#                 mode = "real"
#             except Exception:
#                 # If anything fails, we still record a pending payment
#                 mode = "simulation"
#
#         PaymentRecord.objects.create(
#             order=order,
#             method="MPESA",
#             amount=order.total_cost,
#             status=status,
#             phone_number=phone,
#             reference=reference,
#         )
#
#         if mode == "real":
#             messages.success(
#                 request,
#                 "M-Pesa STK push sent. Check your phone to complete payment.",
#             )
#         else:
#             messages.info(
#                 request,
#                 "Payment recorded in simulation mode. Configure MPESA_* settings for real Daraja integration.",
#             )
#
#         return redirect("store:payment_list")
#
#     # GET: show a small form asking for phone
#     return render(
#         request,
#         "store/order_pay_mpesa.html",
#         {"order": order},
#     )
#