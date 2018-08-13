$(document).ready(function () {
    //my code
var PUB_key= $('#payment-form').attr("data-toggle")


// Create a Stripe client.
var stripe = Stripe(PUB_key);
// console.log("kokooooooooo"+stripe)
// Create an instance of Elements.
var elements = stripe.elements();

// Custom styling can be passed to options when creating an Element.
// (Note that this demo uses a wider set of styles than the guide below.)
var style = {
  base: {
    color: '#32325d',
    lineHeight: '18px',
    fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
    fontSmoothing: 'antialiased',
    fontSize: '16px',
    '::placeholder': {
      color: '#aab7c4'
    }
  },
  invalid: {
    color: '#fa755a',
    iconColor: '#fa755a'
  }
};

// Create an instance of the card Element.
var card = elements.create('card', {style: style});

// Add an instance of the card Element into the `card-element` <div>.
card.mount('#card-element');

// Handle real-time validation errors from the card Element.
card.addEventListener('change', function(event) {
  var displayError = document.getElementById('card-errors');
  if (event.error) {
    displayError.textContent = event.error.message;
  } else {
    displayError.textContent = '';
  }
});

// Handle form submission.
// var form = document.getElementById('payment-form');
// form.addEventListener('submit', function(event) {
//   event.preventDefault();
//
//   stripe.createToken(card).then(function(result) {
//     if (result.error) {
//       // Inform the user if there was an error.
//       var errorElement = document.getElementById('card-errors');
//       errorElement.textContent = result.error.message;
//     } else {
//       // Send the token to your server.
//       stripeTokenHandler(result.token);
//
//     }
//   });
//
// });


///  my form
var form = $('#payment-form');
var bnt_load = form.find(".btn-load")
bnt_load.blur()
var defaultbtnhtml=bnt_load.html()
var defaultbtnclasses=bnt_load.attr('class')
var current_timeout
var loadtime
    



form.submit(function(event) {

  event.preventDefault();

  stripe.createToken(card).then(function(result) {
    if (result.error) {
      // Inform the user if there was an error.
      var errorElement = document.getElementById('card-errors');
      errorElement.textContent = result.error.message;
      loadtime=1000
      var errorbtnhtml="<i class='fa fa-warning'></i> Add Payment method"
      var errorbtnclasses="btn btn-danger disabled my-3 btn-load"
      change_btn_load(errorbtnhtml,errorbtnclasses,loadtime)

    } else {
        loadtime=3500
        var successbtnhtml="<i class='fa fa-spin fa-spinner'></i> loading.... "
        var successbtnclasses="btn btn-success my-3 btn-load"

        change_btn_load(successbtnhtml,successbtnclasses,loadtime)
        // Send the token to your server.
        stripeTokenHandler(result.token);


    }
  });

})

function change_btn_load(newhtml,newclasses,loadtime){

  // if (current_timeout){
  //     clearTimeout(current_timeout)
  // }
  bnt_load.html(newhtml)
  bnt_load.attr('class',newclasses)
  // alert("df")
  setTimeout(function() {
      bnt_load.html(defaultbtnhtml)
      bnt_load.attr('class',defaultbtnclasses)
  },loadtime)

}

// function clear_default_btn_load() {
//
//     bnt_load.html(defaultbtnhtml)
//     bnt_load.attr('class',defaultbtnclasses)
//
// }



function stripeTokenHandler(token){
    var Form_Method = $('#payment-form').attr('method')
    var action  = $('#payment-form').attr('action')
    var next_url = $('#payment-form').attr("data_next_url")
    $.ajax({
        url: action,
        method: Form_Method,
        data: {
            'token':token.id
        },
        // headers: { "X-CSRFToken": getCookie("csrftoken") },   // must used when using ajax , to inject in the ajax headers X-CSRFToken
        success: function (data) {


            card.clear()


            if (next_url){
                // alert(next_url)
                setTimeout(function () {
                window.location.href=next_url
            },1500)}

            $.alert({
                title: "Success!",
                content: data.message + "</br><i class='fa fa-spin fa-spinner'></i> Redirecting...." ,
                theme: "modern",
            })

        },
        error: function (error) {
                $.alert({
                    title: "Error!",
                    content: "please re-enter your payment card" ,
                    theme: "modern",
            })
        }
    });
    }



})