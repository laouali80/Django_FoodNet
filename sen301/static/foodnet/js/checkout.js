console.log('yes checkout')
let form = document.querySelector('form')


if (user === 'AnonymousUser'){

form.addEventListener('submit', function(e){
    e.preventDefault()
    console.log('Not login')
    document.querySelector('form-button').classList.add('hidden')
    document.querySelector('payment-info').classList.remove('hidden')

})
// // return window.location.href = loginUrl;
}else{
console.log('User login')

}

