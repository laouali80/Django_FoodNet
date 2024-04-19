document.addEventListener("DOMContentLoaded", function () {
    
    document.querySelector("#profile-info").addEventListener("click", () => profile_view("info"));
    document.querySelector("#profile-products").addEventListener("click", () => profile_view("products"));
    document.querySelector("#profile-sells").addEventListener("click", () => profile_view("sells"));
    document.querySelector("#profile-orders").addEventListener("click", () => profile_view('orders'));
  
})


function profile_view(view){

    const info_view = document.querySelector("#profile-info-div");
    const products_view = document.querySelector("#profile-products-div");
    const sells_view = document.querySelector("#profile-sells-div");
    const orders_view = document.querySelector("#profile-orders-div");

    if (view === 'info'){
        info_view.style.display = "block";
        products_view.style.display = "none";
        sells_view.style.display = "none";
        orders_view.style.display = "none";

        // console.log('info')
    }else if(view === 'products'){
        info_view.style.display = "none";
        products_view.style.display = "block";
        sells_view.style.display = "none";
        orders_view.style.display = "none";

        // console.log('products')
    }else if(view === 'sells'){
        info_view.style.display = "none";
        products_view.style.display = "none";
        sells_view.style.display = "block";
        orders_view.style.display = "none";

        // console.log('sells')
    }else if(view === 'orders'){
        info_view.style.display = "none";
        products_view.style.display = "none";
        sells_view.style.display = "none";
        orders_view.style.display = "block";

        // console.log('orders')
    }
    
    
}
