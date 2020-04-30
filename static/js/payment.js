// initialise stripe functionality
var stripe = Stripe('pk_test_j8f56cTAACEJUymJMZftX16500A9hjRgzB');

// initialise elements
var elements = stripe.elements();
var card = elements.create('card');

// insert element onto page
card.mount('#card-element');

// capture errors and display on form
card.addEventListener('change', ({
    error
}) => {
    const displayError = document.getElementById('card-errors');
    if (error) {
        displayError.textContent = error.message;
    } else {
        displayError.textContent = '';
    }
});

// submit eventhandler for payment form
var form = document.getElementById('payment-form');
var errorContainer = document.getElementById('card-errors');

// get billing details 
var name = document.getElementById('id_billing_name');
var address = document.getElementById('id_billing_address');
var city = document.getElementById('id_billing_city');
// country is not coded in compatiable format for stripe, through not sent
var postCode = document.getElementById('id_billing_post_code');
var clientSecret = document.getElementById('payment-button');

// on submit, send stripe data and wait for response
form.addEventListener('submit', function (ev) {
    ev.preventDefault();
    stripe.confirmCardPayment(clientSecret.getAttribute('data-secret'), {
        payment_method: {
            card: card,
            billing_details: {
                name: name.value,
                address: {
                    city: city.value,
                    line1: address.value,
                    postal_code: postCode.value,
                }
            }
        }
    }).then(function (response) {
        // reset any previous error messages
        errorContainer.innerHTML = '';

        if (response.error) {
            // return any error messages to console
            errorContainer.innerHTML = '<strong>Error: </strong>';
            errorContainer.innerHTML += response.error.message;
        } else {
            if (response.paymentIntent.status === 'succeeded') {
                // pass-through stripe response
                stripeTokenHandler(response.paymentIntent);
            }
        }
    });
});

function stripeTokenHandler(token) {
    // add stripe token to shipping details form and submit
    var form = document.getElementById('shipping-details-form');
    var hiddenInput = document.createElement('input');
    hiddenInput.setAttribute('type', 'hidden');
    hiddenInput.setAttribute('name', 'stripe-token');
    hiddenInput.setAttribute('value', token.id);
    form.appendChild(hiddenInput);

    form.submit();
}