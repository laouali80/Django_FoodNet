
const updateBtns = document.querySelectorAll('.update-cart');

updateBtns.forEach(btn => {
  btn.addEventListener('click', function(){
    
    let productId = this.dataset.product
    let action = this.dataset.action

    // console.log('productId:', productId, 'Action:', action)

    console.log('User: ', user)

    if (user === 'AnonymousUser'){
      // console.log('Not login')
    }else{
      // console.log('User login')

      updateUserOrder(productId, action)
    }

  })
})


function updateUserOrder(productId, action){

  fetch('/foodNet/update_item/', {
    method: 'POST',
    headers: {
      'Content-Type':'application/json',
      //passing csrftoken to a API
      'X-CSRFToken': csrftoken,
    },
    body: JSON.stringify({
      'productId': productId,
      'action': action
    })
  })
  .then(response => {
    return response.json()
  })
  .then(data => {
    // console.log(data)

    location.reload()
  })
}

const deliveryMeth = document.querySelectorAll("[type='radio']");

const ship_form = document.querySelector("#form")

deliveryMeth.forEach(ratio => {
    ratio.addEventListener('change', ()=>{
        const shipp_div = document.querySelector("#shipping-info")
        let msg = document.querySelector('#message')

        if (ratio.value === 'delivery'){
          console.log(msg)

            shipp_div.style.display = 'block';

            const order_total = document.querySelector('#order-total')

            let newTotal = parseInt(total)+500

            order_total.innerText = `Total: ${naira(newTotal)}`

            // listen to the form submission
            ship_form.addEventListener('submit', (e)=>{

              e.preventDefault()
            
              let shippingInfo = {
                'name': ship_form.name.value,
                'email': ship_form.email.value,
                'phone_number': ship_form.phone_number.value,
                'total': parseInt(total) + 500,
                'address': ship_form.address.value,
                'state': ship_form.state.value,
                'city': ship_form.city.value,
                'zipcode': ship_form.zipcode.value
            
              }
            
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
                console.log(data)
            
                // to redirect to the market view
                // window.location.href = "{% url 'market' %}"
               
                msg.classList.add('alert-danger');
                msg.innerHTML = `<strong>Info!</strong> You do not have enough cash to make this order.
                      <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                          <span aria-hidden="true">&times;</span>
                      </button>
                `
                msg.style.display = "block";

                setTimeout(function () { // wait 3 seconds and reload
                  window.location.reload(true);
                }, 6000);
                // location.reload()

              })
            })

        }else if (ratio.value === 'pickUp'){

          shipp_div.style.display = 'none';

          const order_total = document.querySelector('#order-total')

          order_total.innerText = `Total: ${naira(parseInt(total))}`

          // listen to the form submission
          ship_form.addEventListener('submit', (e)=>{

            e.preventDefault()
          
            let shippingInfo = {
              'name': ship_form.name.value,
              'email': ship_form.email.value,
              'phone_number': ship_form.phone_number.value,
              'total': parseInt(total),
              'address': ship_form.address.value,
              'state': ship_form.state.value,
              'city': ship_form.city.value,
              'zipcode': ship_form.zipcode.value
          
            }
          
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
              console.log(data)
          
              // to redirect to the market view
              // window.location.href = "{% url 'market' %}"
              location.reload()
            })
          })
        }
    })
})


function naira(value) {
  // Format value as Naira
  return '₦' + value.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
}
