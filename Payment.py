from paypalrestsdk import Payment, Order

import paypalrestsdk
import logging

class PaymentOperations:
    def __init__(self):
        paypalrestsdk.configure({
            "mode": "sandbox",
            "client_id": "AcS2tiO8Wd52NiDr5ihyNm5qOXuytDn91JovIHBNtuPUzLDoOygcU6VC6n8uv9cLLsLyI7tiuy3YoQil",
            "client_secret": "EGhwdBssqDo0xWllytj5y23BdObWycBqEwV0F3_c79mv4BISB7jrXYBk5iSgOTpj95ysxVw9iFEpdiWg"
        })



    def make_payment(self, amount, email):
       
        # Payment
        # A Payment Resource; create one using
        # the above types and intent as 'sale'
        payment = Payment({
            "intent": "sale",

            # Payer
            # A resource representing a Payer that funds a payment
            # Payment Method as 'paypal'
            "payer": {
                "payment_method": "paypal"},

            # Redirect URLs
            "redirect_urls": {
                "return_url": "https://roomr-222721.appspot.com/execute",
                #"return_url": "http://192.168.0.109:8080/execute",
                "cancel_url": "http://localhost:3000/"},

            # Transaction
            # A transaction defines the contract of a
            # payment - what is the payment for and who
            # is fulfilling it.
            "transactions": [{

                # ItemList
                "item_list": {
                    "items": [{
                        "name": "This month's rent",
                        "sku": "item",
                        "price": amount,
                        "currency": "CAD",
                        "quantity": 1}]},

                    # Amount
                    # Let's you specify a payment amount.
                "amount": {
                "total": amount,
                "currency": "CAD"
                },
                "payee": {
                    "email": email
                },
                "description": "Rent paid by tenant"}
                ]
                })

        # Create Payment and return status
        if payment.create():
            print("Payment[%s] created successfully" % (payment.id))
            # Redirect the user to given approval url
            for link in payment.links:
                if link.rel == "approval_url":
                    # Convert to str to avoid google appengine unicode issue
                    # https://github.com/paypal/rest-api-sdk-python/pull/58
                    approval_url = str(link.href)
                    print("Redirect for approval: %s" % (approval_url))
            return (approval_url, payment.id)

        


