
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