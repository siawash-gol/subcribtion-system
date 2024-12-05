from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from config.apps.ClientHub.models import Plan, UserPlan, PayHistory
from config.apps.ClientHub.utils import handel_subscribtion
from config.auth.Users.models import User
from config.auth.Users.utils import Util
import paypalrestsdk
import os


paypalrestsdk.configure({
    "mode": "sandbox",
    "client_id": os.environ.get("PAYPAL_CLIENT_ID"),
    "client_secret": os.environ.get("PAYPAL_CLIENT_SECRET"),
})


class CreatePaymentRequestView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        plan_sku = kwargs.get('sku', None)
        plan = get_object_or_404(Plan, sku=plan_sku)
        amount = plan.price
        currency = "CAD"

        if UserPlan.objects.filter(user=user, plan=plan).exists():
            return Response("You have already purchased this plan.", status=status.HTTP_409_CONFLICT)

        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal",
            },
            "redirect_urls": {
                "return_url": os.environ.get("PAYPAL_RETURN_URL", "http://127.0.0.1:8000/pricing/execute-payment"),
                "cancel_url": os.environ.get("PAYPAL_CANCEL_URL", "http://127.0.0.1:8000/pricing/payment-cancel"),
            },
            "transactions": [
                {
                    "amount": {
                        "total": str(amount),
                        "currency": currency,
                    },
                    "item_list": {
                        "items": [
                            {
                                "name": plan.plan,
                                "sku": plan.sku,
                                "price": str(amount),
                                "currency": currency,
                                "quantity": 1,
                            }
                        ]
                    },
                    "description": f"Your plan: {plan.plan} and duration: {plan.get_duration}"
                }
            ],
        })

        if payment.create():

            approval_url = next(link.href for link in payment.links if link.rel == "approval_url")
            return Response({"approval_url": approval_url}, status=status.HTTP_200_OK)
        else:
            return Response({"error": payment.error}, status=status.HTTP_400_BAD_REQUEST)


class ExecutePayment(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        payment_id = request.GET.get('paymentId', None)
        payer_id = request.GET.get('PayerID', None)

        if not payment_id or not payer_id:
            return Response({"error": "Missing paymentId or PayerID"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            payment = paypalrestsdk.Payment.find(payment_id)
            plan_sku = payment['transactions'][0]['item_list']['items'][0]['sku']
            plan = get_object_or_404(Plan, sku=plan_sku)
            amount = payment['transactions'][0]['amount']['total']

            if payment.execute({"payer_id": payer_id}):
                user = request.user
                user_subscription = handel_subscribtion(payment_id=payment_id, user_id=user.id, plan=plan, amount=amount)

                if user_subscription:

                    email_body = (
                        f"Hi {user.username},\n\n"
                        f"Thank you for purchasing the {plan.plan} plan on our site."
                    )
                    email_data = {
                        'email_body': email_body,
                        'email_to': user.email,
                        'email_subject': 'Plan Purchase Confirmation'
                    }
                    Util.send_email(email_data)

                    PayHistory.objects.create(
                        user=user,
                        payment_for=plan,
                        payment_methode="paypal",
                        amount=amount,
                        paid=True,
                    )

                    return Response("Payment executed successfully", status=status.HTTP_200_OK)

                else:
                    return Response(
                        "Payment successful but subscription creation failed. Please contact support.",
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )
            else:
                return Response({"error": payment.error}, status=status.HTTP_400_BAD_REQUEST)

        except paypalrestsdk.ResourceNotFound:
            return Response({"error": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)
