
const updateBtns = document.querySelectorAll('.update-cart');

updateBtns.forEach(btn => {
  btn.addEventListener('click', function(){
    
    let productId = this.dataset.product
    let action = this.dataset.action

    // console.log('productId:', productId, 'Action:', action)

    // console.log('User: ', user)

    if (user === 'AnonymousUser'){
      console.log('Not login')

      addCookieItem(productId, action)

      location.reload()

      // return window.location.href = loginUrl;
    }else{
      // console.log('User login')

      updateUserOrder(productId, action)
    }

  })
})

function addCookieItem(productId, action){
  
  // illustration of a cookie cart
  // cart = {
  //   1:{'quantity':4},
  //   4:{'quantity':1},
  //   6:{'quantity':2}
  // }

  if (action == 'add'){
    if(cart[productId] == undefined){
      cart[productId] = {"quantity":1}
    }else{
      cart[productId]['quantity'] += 1
    }
  } else if (action == 'remove'){
    cart[productId]['quantity'] -= 1

    if (cart[productId]['quantity'] <= 0){
      delete cart[productId];
    }
  }
  
  // register or save the cookie
  document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
}

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
// const delivery = document.querySelector("#delivery");

const ship_form = document.querySelector("#form")


// listen to the form submission
// ship_form.addEventListener('submit', (e)=>{

//   e.preventDefault()

//   console.log(ship_form)

//   let shippingInfo = {
//     'name': ship_form.name.value,
//     'email': ship_form.email.value,
//     'phone_number': ship_form.phone_number.value,
//     'total': parseInt(total),
//     'address': ship_form.address.value,
//     'state': ship_form.state.value,
//     'city': ship_form.city.value,
//     'zipcode': ship_form.zipcode.value

//   }

//   fetch('/foodNet/place_order/', {
//     method: 'POST',
//     headers: {
//       'Content-Type':'application/json',
//       //passing csrftoken to a API
//       'X-CSRFToken': csrftoken,
//     },
//     body: JSON.stringify({
//       'shipping': shippingInfo
//     })
//   })
//   .then(response => {
//     return response.json()
//   })
//   .then(data => {
    
//     orderResponse(data, msg);

//   })
// })

// change in the shipping method
deliveryMeth.forEach(ratio => {
    ratio.addEventListener('change', ()=>{
        const shipp_div = document.querySelector("#shipping-info")
        let msg = document.querySelector('#message')

        if (ratio.value === 'delivery'){
          

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
               orderResponse(data, msg);
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
              
              orderResponse(data, msg);

              // to redirect to the market view
              // window.location.href = "{% url 'market' %}"
              // to reload a page
              // location.reload()
            })
          })
        }
    })
})


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
