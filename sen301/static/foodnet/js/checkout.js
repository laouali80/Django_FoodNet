let form = document.querySelector('form')


// if (user === 'AnonymousUser'){
// // console.log('Not login')

// // return window.location.href = loginUrl;
// }else{
// // console.log('User login')

// }

form.addEventListener('submit', function(e){
    e.preventDefault()

    document.querySelector('form-button').classList.add('hidden')
    document.querySelector('payment-info').classList.remove('hidden')

})