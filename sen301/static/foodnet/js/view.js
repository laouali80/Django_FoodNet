document.addEventListener("DOMContentLoaded", function () {

    const plus = document.querySelector('#plus');
    const minus = document.querySelector('#minus');
    
    plus.addEventListener('click', add);
    minus.addEventListener('click', remove);
  });
  

function add(){
    const quantity = document.querySelector('#quantity');

    let num = parseInt(quantity.innerText);
    if (num > 0){
        num = ++num;
        quantity.innerText = num;
    }
}

function remove(){
    const quantity = document.querySelector('#quantity');

    let num = parseInt(quantity.innerText);
    if (num > 1 ){
        num = --num;
        quantity.innerText = num;
    }
}