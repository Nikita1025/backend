import stripe
import json
from flask_cors import CORS

from flask import Flask, jsonify, request


stripe.api_key = 'sk_test_51OVZadCH3dnwWZ7miWVnVfw0CddrO7Te4q6mrBIMw72cLJ8Ol3GigNU9KacNntWHt964iF7TCuegdbWDKoxLwf1500VXhvPL9p'


endpoint_secret = 'whsec_iFntZnznNPMbLvKS1fwXcMubEiUu4krR'
app = Flask(__name__)
CORS(app)

user_info = {}


@app.route('/sub', methods=['POST'])
def sub():
    email = request.json.get('email', None)
    payment_method = request.json.get('payment_method', None)
    plan_id = request.json.get('plan_id', None)

    if not email:
        return 'You need to send an Email!', 400
    if not payment_method:
        return 'You need to send an payment_method!', 400

    # This creates a new Customer and attaches the default PaymentMethod in one API call.
    customer = stripe.Customer.create(
        payment_method=payment_method,
        email=email,
        invoice_settings={
            'default_payment_method': payment_method,
        },
    )
    # Creates a subscription and attaches the customer to it
    subscription = stripe.Subscription.create(
        customer=customer['id'],
        items=[
            {
                'plan': plan_id,
            },
        ],
        expand=['latest_invoice.payment_intent'],
    )

    status = subscription['latest_invoice']['payment_intent']['status']
    client_secret = subscription['latest_invoice']['payment_intent']['client_secret']

    user_info['customer_id'] = customer['id']
    user_info['email'] = email

    return {'status': status, 'client_secret': client_secret}, 200


@app.route('/create-payment-intent', methods=['POST'])
def create_payment():
    data = json.loads(request.data)
    payment_method_type = data['paymentMethodType']
    currency = data['currency']
    formatted_payment_method_type = [
        'link', 'card'] if payment_method_type == 'link' else [payment_method_type]
    params = {
        'payment_method_types': formatted_payment_method_type,
        'amount': 5999,
        'currency': currency
    }
    if payment_method_type == 'acss_debit':
        params['payment_method_options'] = {
            'acss_debit': {
                'mandate_options': {
                    'payment_schedule': 'sporadic',
                    'transaction_type': 'personal'
                }
            }
        }

    try:
        intent = stripe.PaymentIntent.create(**params)

        # Send PaymentIntent details to the front end.
        return jsonify({'clientSecret': intent.client_secret})
    except stripe.error.StripeError as e:
        return jsonify({'error': {'message': str(e)}}), 400
    except Exception as e:
        return jsonify({'error': {'message': str(e)}}), 400


if __name__ == '__main__':
    app.run(port=4242, debug=True)
