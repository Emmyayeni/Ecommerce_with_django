"use strict";

var Addbtn = document.getElementsByClassName('add-btn');
var cart = document.getElementsByClassName('cartno');
var actionbtns = document.getElementsByClassName('update-cart');

for (var i = 0; i < actionbtns.length; i++) {
  actionbtns[i].addEventListener('click', function () {
    var productId = this.dataset.product;
    var action = this.dataset.action;
    console.log('productId:', productId, 'Action:', action);
    console.log('USER:', user);
    console.log('product:', productId);

    if (user == 'AnonymousUser') {
      addCookieItem(productId, action);
    } else {
      console.log('cartc', cartc);
      document.cookie = 'cartc=' + JSON.stringify(cartc) + ";domain=;path=/";
      location.reload();
      updateUserOrder(productId, action);
    }
  });
}

function addCookieItem(productId, action) {
  console.log(" User is not authenticated..");
  console.log(cartc);

  if (action == 'add') {
    if (cartc[productId] == undefined) {
      cartc[productId] = {
        'quantity': 1
      };
    } else {
      cartc[productId]['quantity'] += 1;
    }
  }

  if (action == 'remove') {
    cartc[productId]['quantity'] -= 1;

    if (cartc[productId] <= 0) {
      console.log('this item is about to be deleted ');
      delete cartc[productId];
    }
  }

  console.log('cartc', cartc);
  document.cookie = 'cartc=' + JSON.stringify(cartc) + ";domain=;path=/";
  location.reload();
}

function updateUserOrder(productId, action) {
  console.log('User is logged in, sending data...');
  var url = '/update_item/';
  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken
    },
    body: JSON.stringify({
      'productId': productId,
      'action': action
    })
  }).then(function (response) {
    return response.json();
  }).then(function (data) {
    console.log('data:', data);
    location.reload();
  });
} // for (let i = 0; i < Addbtn.length; i++) {
//     Addbtn[i].addEventListener('click',()=>{
//         console.log('it working ')
//         for (let i = 0; i < cart.length; i++) {
//            cart[i].innerHTML = parseInt(cart[i].innerHTML) + 1
//         }
//     })
// }