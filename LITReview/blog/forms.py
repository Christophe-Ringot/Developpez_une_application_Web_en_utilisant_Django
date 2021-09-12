from .models import Ticket, Review
from django import forms


class UploadTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ("title", "description", "image", "user")


class UploadReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("headline", "body", "rating", "ticket", "user")

