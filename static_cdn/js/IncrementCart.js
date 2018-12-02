var itemCount=document.getElementById('itemCount').innerText;
if(itemCount===null)
  itemCount=0;

document.getElementById('addToCart').addEventListener("click", function(){

  if(document.getElementById('addToCart').classList.contains('btn-info')){
    itemCount ++;
    document.getElementById('itemCount').innerText=itemCount;
    document.getElementById('itemCount').style.display='block';
    document.getElementById('addToCart').classList.remove('btn-info');
    document.getElementById('addToCart').classList.add('btn-danger');
    document.getElementById('addToCart').innerText="Remove From Cart";
  }
  else{
    document.getElementById('addToCart').classList.remove('btn-danger');
    document.getElementById('addToCart').classList.add('btn-info');
    var btn_Text = '<i class="fa fa-shopping-cart"></i> Add To Cart';
    document.getElementById('addToCart').innerHTML=btn_Text;
    decreaseCartcount();
  }

});

function decreaseCartcount(){
    var counter = document.getElementById('itemCount').innerText=itemCount;
    counter=counter-1;
    document.getElementById('itemCount').innerText=counter;
    //document.getElementById('itemCount').style.display='block';
    itemCount=counter;
}
// $('.clear').click(function() {
//   itemCount = 0;
//   $('#itemCount').html('').css('display', 'none');
//   $('#cartItems').html('');
// });
