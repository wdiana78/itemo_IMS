from django import forms
from .models import (
    Item,
    Supplier,
    Client,
    SupplierOrder,
    StockIssue,
    PaymentRecord,
)


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            "name",
            "category",
            "description",
            "quantity",
            "unit_price",
            "status",
            "reorder_level",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
            "quantity": forms.NumberInput(attrs={"class": "form-control"}),
            "unit_price": forms.NumberInput(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "reorder_level": forms.NumberInput(attrs={"class": "form-control"}),
        }


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = [
            "name",
            "contact_person",
            "phone",
            "email",
            "address",
            "is_active",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "contact_person": forms.TextInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "address": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            "name",
            "contact_person",
            "phone",
            "email",
            "address",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "contact_person": forms.TextInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
        }


class SupplierOrderForm(forms.ModelForm):
    class Meta:
        model = SupplierOrder
        fields = [
            "supplier",
            "item",
            "quantity_ordered",
            "unit_price",
            "status",
            "notes",
        ]
        widgets = {
            "supplier": forms.Select(attrs={"class": "form-select"}),
            "item": forms.Select(attrs={"class": "form-select"}),
            "quantity_ordered": forms.NumberInput(
                attrs={"class": "form-control"}
            ),
            "unit_price": forms.NumberInput(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "notes": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
        }


class StockIssueForm(forms.ModelForm):
    class Meta:
        model = StockIssue
        fields = [
            "item",
            "client",
            "quantity",
            "issue_date",
            "issued_by",
            "notes",
        ]
        widgets = {
            "item": forms.Select(attrs={"class": "form-select"}),
            "client": forms.Select(attrs={"class": "form-select"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control"}),
            "issue_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "issued_by": forms.TextInput(attrs={"class": "form-control"}),
            "notes": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
        }


class PaymentRecordForm(forms.ModelForm):
    class Meta:
        model = PaymentRecord
        fields = [
            "order",
            "method",
            "amount",
            "status",
            "phone_number",
            "reference",
        ]
        widgets = {
            "order": forms.Select(attrs={"class": "form-select"}),
            "method": forms.Select(attrs={"class": "form-select"}),
            "amount": forms.NumberInput(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
            "reference": forms.TextInput(attrs={"class": "form-control"}),
        }
