from django.urls import path
from config.apps.ClientHub.views.pricing_views import (
    CreatePaymentRequestView,
    ExecutePayment,
)

urlpatterns = [
    # PayPal Payment Routes
    path(
        'payment/paypal/create/<slug:sluhg>',
        CreatePaymentRequestView.as_view(),
        name='create_paypal_payment',
    ),
    path(
        'payment/paypal/execute/',
        ExecutePayment.as_view(),
        name='execute_paypal_payment',
    ),

]
