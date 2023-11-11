var Addbtn= document.getElementsByClassName('add-btn')
var cart = document.getElementsByClassName('cartno')
var actionbtns = document.getElementsByClassName('update-cart')

for (let i = 0; i < actionbtns.length; i++) {
    actionbtns[i].addEventListener('click',function(){
        var productId = this.dataset.product
        var  action = this.dataset.action
        console.log('productId:',productId,'Action:',action)
		console.log('USER:', user)
		console.log('product:', productId)

        if(user == 'AnonymousUser'){
            addCookieItem(productId,action)
            if(action == 'remove'){
                document.querySelector('.swalDefaultSuccess2').click()
            }else if(action == 'add'){
                document.querySelector('.swalDefaultSuccess').click()
            }

            
		}else{
			updateUserOrder(productId, action)
           
                if(action == 'remove'){
                    document.querySelector('.swalDefaultSuccess2').click()
                }else if(action == 'add'){
                    document.querySelector('.swalDefaultSuccess').click()
                }
            
		}
    })
    
}
function addCookieItem(productId,action){
    console.log(" User is not authenticated..")
    console.log(cartc)
    if(action == 'add'){
        if(cartc[productId] == undefined){
            cartc[productId] = {'quantity':1}
        }else{
            cartc[productId]['quantity'] += 1
        }
        document.querySelector('.swalDefaultSuccess').click()
    }
    if(action == 'remove'){
        cartc[productId]['quantity'] -= 1

        if(cartc[productId] <= 0){
            console.log('this item is about to be deleted ')
                delete cartc[productId];
            }
        
    }

    console.log('cartc',cartc)
    document.cookie ='cartc=' + JSON.stringify(cartc)+ ";domain=;path=/"
    location.reload()
   
}

function updateUserOrder(productId,action){
        console.log('User is logged in, sending data...')
        var url = '/update_item/';
        fetch(url,{
            method:'POST',
            headers:{
                'Content-Type':'application/json',
                'X-CSRFToken':csrftoken,
            },
            body:JSON.stringify({'productId': productId, 'action':action})
         })
        .then((response)=>{
            return response.json()
        })
        .then((data)=>{
            console.log('data:',data)
            location.reload()
        })
    }
    

