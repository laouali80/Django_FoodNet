
const ship_form = document.querySelector("#form")


if (user === 'AnonymousUser'){

ship_form.addEventListener('submit', function(e){
    e.preventDefault()
    console.log('Not login')
    document.querySelector('#form-button').classList.add('hidden')
    document.querySelector('#payment-info').classList.remove('hidden')
})

// document.querySelector("#make-payment").addEventListener('click', function(e){
//   // console.log('triger')  
//   submitFormData()
// })


function submitFormData() {
    let shippingInfo = {}
    let msg = document.querySelector('#message')


    if (document.querySelector("#pickUp").checked) {
        // console.log('free')
        shippingInfo = {
            'name': ship_form.name.value,
            'email': ship_form.email.value,
            'phone_number': ship_form.phone_number.value,
            'total': parseInt(total),
            'address': ship_form.address.value,
            'state': ship_form.state.value,
            'city': ship_form.city.value,
            'zipcode': ship_form.zipcode.value
        }
    }
    else if (document.querySelector("#delivery").checked) {
        // console.log('pay')
        shippingInfo = {
            'name': ship_form.name.value,
            'email': ship_form.email.value,
            'phone_number': ship_form.phone_number.value,
            'total': parseInt(total) + 500,
            'address': ship_form.address.value,
            'state': ship_form.state.value,
            'city': ship_form.city.value,
            'zipcode': ship_form.zipcode.value
        }
    }


    // send a request to process the order
    fetch('/foodNet/place_order/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            //passing csrftoken to a API
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'shipping': shippingInfo
        })
    })
        .then(response => {
            return response.json()
        })
        .then(data => {

            console.log('success:', data)

            cart = {}
            document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
            orderResponse(data, msg)
        })
}

}else{
// console.log('I am here now')

const deliveryMeth = document.querySelectorAll("[type='radio']");


const ship_form = document.querySelector("#form")

// const test = document.querySelector("#delivery").checked


// listen to the form submission
ship_form.addEventListener('submit', (e)=>{

    e.preventDefault()
    let shippingInfo = {}
    let msg = document.querySelector('#message')


    if (document.querySelector("#pickUp").checked){
        // console.log('free')
        shippingInfo = {
            'name': ship_form.name.value,
            'email': ship_form.email.value,
            'phone_number': ship_form.phone_number.value,
            'total': parseInt(total),
            'address': ship_form.address.value,
            'state': ship_form.state.value,
            'city': ship_form.city.value,
            'zipcode': ship_form.zipcode.value
        
          }
    }
    else if(document.querySelector("#delivery").checked){
        // console.log('pay')
        shippingInfo = {
            'name': ship_form.name.value,
            'email': ship_form.email.value,
            'phone_number': ship_form.phone_number.value,
            'total': parseInt(total) + 500,
            'address': ship_form.address.value,
            'state': ship_form.state.value,
            'city': ship_form.city.value,
            'zipcode': ship_form.zipcode.value
        
          }
    }

    
    // send a request to process the order
    fetch('/foodNet/place_order/', {
      method: 'POST',
      headers: {
        'Content-Type':'application/json',
        //passing csrftoken to a API
        'X-CSRFToken': csrftoken,
      },
      body: JSON.stringify({
        'shipping': shippingInfo
      })
    })
    .then(response => {
      return response.json()
    })
    .then(data => {
      
      orderResponse(data, msg);

      // to redirect to the market view
      // window.location.href = "{% url 'market' %}"
      // to reload a page
      // location.reload()
    })
  })




// change in the shipping method
deliveryMeth.forEach(ratio => {
    ratio.addEventListener('change', ()=>{
        const shipp_div = document.querySelector("#shipping-info")
        
        if (ratio.value === 'delivery'){
          

            shipp_div.style.display = 'block';

            const order_total = document.querySelector('#order-total')

            let newTotal = parseInt(total)+500

            order_total.innerText = `Total: ${naira(newTotal)}`

        }else if (ratio.value === 'pickUp'){


          shipp_div.style.display = 'none';

          const order_total = document.querySelector('#order-total')

          order_total.innerText = `Total: ${naira(parseInt(total))}`

          
        }
    })
})


}


function orderResponse(data, msg) {
  if (data.response === 'Fail') {

    msg.classList.add('alert-danger');
    msg.innerHTML = `<strong>Info!</strong> You do not have enough cash to make this order.
                        <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                  `;
    msg.style.display = "block";

    setTimeout(function () {
      msg.style.display = "none";
    }, 3000);
    
    // location.reload()
    // window.location.reload(true);
  } else if (data.response === 'Success') {

    msg.classList.add('alert-success');
    msg.innerHTML = `<strong>Success!</strong> Your order has been place successfuly.
                        <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                  `;
    msg.style.display = "block";

    setTimeout(function () {
      return window.location.href = marketUrl;
    }, 3000);
  }
  else {

    msg.classList.add('alert-danger');
    msg.innerHTML = `<strong>Danger!</strong> Intruder!! Someone wants to change the data.
                        <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                  `;
    msg.style.display = "block";

    setTimeout(function () {
      msg.style.display = "none";
    }, 3000);
  }
}

function naira(value) {
  // Format value as Naira
  return '₦' + value.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
}


// paypal payment
window.paypal
  .Buttons({
    style: {
      shape: "rect",
      layout: "vertical",
      color: "gold",
      label: "paypal",
    } ,
    async createOrder() {
      try {
        const response = await fetch("/api/orders", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          // use the "body" param to optionally pass additional order information
          // like product ids and quantities
          body: JSON.stringify({
            cart: [
              {
                id: "YOUR_PRODUCT_ID",
                quantity: "YOUR_PRODUCT_QUANTITY",
              },
            ],
          }),
        });

        const orderData = await response.json();

        if (orderData.id) {
          return orderData.id;
        }
        const errorDetail = orderData?.details?.[0];
        const errorMessage = errorDetail
          ? `${errorDetail.issue} ${errorDetail.description} (${orderData.debug_id})`
          : JSON.stringify(orderData);

        throw new Error(errorMessage);
      } catch (error) {
        console.error(error);
        // resultMessage(`Could not initiate PayPal Checkout...<br><br>${error}`);
      }
    } ,
    async onApprove(data, actions) {
      try {
        const response = await fetch(`/api/orders/${data.orderID}/capture`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
        });

        const orderData = await response.json();
        // Three cases to handle:
        //   (1) Recoverable INSTRUMENT_DECLINED -> call actions.restart()
        //   (2) Other non-recoverable errors -> Show a failure message
        //   (3) Successful transaction -> Show confirmation or thank you message

        const errorDetail = orderData?.details?.[0];

        if (errorDetail?.issue === "INSTRUMENT_DECLINED") {
          // (1) Recoverable INSTRUMENT_DECLINED -> call actions.restart()
          // recoverable state, per
          // https://developer.paypal.com/docs/checkout/standard/customize/handle-funding-failures/
          return actions.restart();
        } else if (errorDetail) {
          // (2) Other non-recoverable errors -> Show a failure message
          throw new Error(`${errorDetail.description} (${orderData.debug_id})`);
        } else if (!orderData.purchase_units) {
          throw new Error(JSON.stringify(orderData));
        } else {
          // (3) Successful transaction -> Show confirmation or thank you message
          // Or go to another URL:  actions.redirect('thank_you.html');
          const transaction =
            orderData?.purchase_units?.[0]?.payments?.captures?.[0] ||
            orderData?.purchase_units?.[0]?.payments?.authorizations?.[0];
          resultMessage(
            `Transaction ${transaction.status}: ${transaction.id}<br>
          <br>See console for all available details`
          );
          console.log(
            "Capture result",
            orderData,
            JSON.stringify(orderData, null, 2)
          );
        }
      } catch (error) {
        console.error(error);
        resultMessage(
          `Sorry, your transaction could not be processed...<br><br>${error}`
        );
      }
    } ,
  })
  .render("#paypal-button-container"); 
