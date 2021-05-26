products = document.querySelectorAll('tr#product')
cartFinalQuantity = document.querySelector('#cart_final_quantity')
cartFinalPrice = document.querySelector('#cart_final_price')

products.forEach(product => product.addEventListener('change', e => {
    productPrice = product.children[2]
    productQuantity = product.children[3].children[0]
    productTotalPrice = product.children[4]
    
    newPrice = productQuantity.value*productPrice.innerHTML
    productTotalPrice.innerHTML = newPrice

    quantity = []
    productsQuantity = document.querySelectorAll('#product_quantity')
    productsQuantity.forEach(q => quantity.push(q.value))
    console.log(quantity);

    price = []
    productsFinalPrice = document.querySelectorAll('#product_final_price')
    productsFinalPrice.forEach(p => price.push(p.innerHTML))
    console.log(price);

    cartFinalQuantity.innerHTML = quantity.reduce((a, b) => Number(a) + Number(b), 0)
    cartFinalPrice.innerHTML = price.reduce((a, b) => Number(a) + Number(b), 0)

})
)

