var cart_product_ajax=$(".cart-product-ajax")
var contact_form=$(".contact-form")
var loginSelector = $("#login-nav")
// var carticon_id = $('#carticon')
var remove_from_Cart = $('#remove_from_cart')
var remove_from_cart_btn = $('.remove_from_cart_btn')
var cart_items_count=$("#itemCount")
var Cart_Modal_body = $("#Cart_Modal_body")
var cartModal_items_count = $('#cartModal-items-count')


$(document).ready(function () {

// Auto search form
var searchform = $(".search-form")
    var typetimer
    var searchformvalue=searchform.find("[name='q']")
    // var searchbtn = searchform.find("[type='submit']")

    var searchbtn = $("#search_btn")
    // console.log(searchbtn)
    //will add the category and type





    searchformvalue.keyup(function (event) {
        console.log(searchformvalue.val())
        // key released
        clearTimeout(typetimer)
        typetimer=setTimeout(typesearch(event),500)
        //searchform.reset()
    })
    searchformvalue.keydown(function () {
        //key pressed
        clearTimeout(typetimer)
    })
    function typesearch(event){
        searchbtn.addClass("disabled")
        searchbtn.html("<i class=\"fa fa-spinner\" aria-hidden=\"true\"></i>searching...")
        //console.log(searchformvalue.val())
        setTimeout(function(){
            var SubType=$('select option:selected').val()
            var Type=$('select :selected').parent().attr('label')
            // alert(Type)
            // alert(SubType)
            window.location.href="/search/?q="+searchformvalue.val()+"&type="+Type+"&subtype="+SubType
        },2000)
        //alert("k")
        //console.log(window.location.href)
    }

    ///////////////////////////////////// ######################  Auto displaying colors ##################   ///////////////

    var select_color_sizes = $('.color_based_size')
    var dl_selector= $('.detailed_info')
    //
    // var dt_selector= dl_selector.find('Color')
    // alert(dt_selector.val())

    select_color_sizes.on('change' ,function(){
            result_colors=this.value

            str_colors="<div class='color-wrapper'><ul class=\"list-inline color-list\">"

            var my_colors_array = JSON.parse((result_colors).replace(/'/g, '"'))


            for (var i in my_colors_array){

                switch (my_colors_array[i]){
                    case 'red':
                       str_colors+= "<li class='color-list__item color-list__item--red'></li>"
                        break

                    case 'white':
                        str_colors+= "<li class='color-list__item color-list__item--white'></li>"
                        break
                    case 'blue':
                        str_colors+= "<li class='color-list__item color-list__item--blue'></li>"
                        break
                    case 'green':

                        str_colors+="<li class='color-list__item color-list__item--green'></li>"
                        break


                    case 'orange':

                        str_colors+= "<li class='color-list__item color-list__item--orange'></li>"
                        break


                    case 'purple':
                        str_colors+="<li class='color-list__item color-list__item--purple'></li>"
                        break

                    case 'yellow':

                        str_colors+="<li class='color-list__item color-list__item--yellow'></li>"
                        break

                    case 'black':
                        str_colors+="<li class='color-list__item color-list__item--black'></li>"
                }
            }

            str_colors+="</ul></div>"
        // $("dd:nth-child(4)").html(str_colors)
            $('#ul_Color_Sizes').html(str_colors)
            console.log(str_colors)
        });




    ///////////////////////////////////// ######################  end of Auto displaying colors ##################   ///////////////

////////////////////////////////##################### Bootstrap Modal #########################//////////////////////
    $("#click_Modal").click(function (event) {
        $('#loginModal').modal('show')

    })
    loginSelector.submit(function (event) {
    var errors_div=$('#loginModal').find('.put_errors')
    var error
    event.preventDefault()
    var $this = $(this)
    // alert($this)
    var method = $this.attr('method')
    var action = $this.attr('action')

    var dataformat = $this.serialize()
    $.ajax({
        url:action,
        method:method,
        data:dataformat,


        success:function (data) {

            console.log("success")
            if (data.case == 'valid'){
                $('#loginModal').modal('hide')
                setTimeout(function () {
                    window.location.reload(data.to_page)
                },1000)
            }
            if(data.case == 'invalid') {
                $('#loginModal').modal('show')
                // console.log(data.errors)
                if ((data.errors['Email'])) {
                    // console.log((data.errors['Email'])[0])
                    error = (data.errors['Email'])[0]
                }
                else {
                    // var obj = JSON.parse(data.errors)
                    // console.log((data.errors.__all__)[0])
                    error = (data.errors.__all__)[0]
                    // console.log(JSON.parse(error))
                }
            }
            errors_div.html(error)
        },

        error:function (error) {
            console.log("error")
            console.log(error)
        }
    })




})

////////////////////////////////##################### end of Bootstrap Modal #########################//////////////////////


////////////////////////#################### if the user is registered the modal of login should be appeared###///////////
    var Register_From=$('.Regitser_form')

    Register_From.submit(function (event) {
        // $(window).load(function () {
        //     $('#loginModal').modal('show')
        // })
        $(document).ready(function(){
            if(window.location.href == '/'){
                    $('#loginModal').modal('show');
                }
}       );
    })


////////////////////////#################### if the user is registered the modal of login should be appeared###///////////
    // cAdd to carts + cart.products.all display
contact_form.submit(function (event) {

    event.preventDefault()
    var $this = $(this)
    var method = $this.attr("method")
    var action = $this.attr("action")
    var DataFormat = $this.serialize()

    $.ajax({
        url: action,
        method: method,
        data: DataFormat,
        success: function (data) {
            contact_form[0].reset()
            $.alert({
                title:"Thank you",
                content:data.message,
                theme:"modern",
            })
        },
        error: function (error) {
            var ermsg=""
            //console.log(error.responseJSON)
            $.each(error.responseJSON,function (key,value) {
                //console.log(value)
                ermsg+=key+":"+value[0].message+ "<br/>"

                //console.log(value)
                //ermsg+=error.responseJSON[0].message+ "</br>"
            })
            $.alert({
                title: "Ops!",
                content: ermsg,
                theme: "modern",

            })

        }

    })

})

cart_product_ajax.submit(function (event) {
    event.preventDefault()
    var $this = $(this)
    var method = $this.attr("method")
    var action = $this.attr("action")
    var span_added= $this.find(".span-added")

    var DataFormat = $this.serialize()

    $.ajax({
        url: action,
        method: method,
        data: DataFormat,
        success: function (data) {

            if(data.added){
                span_added.html("<button id='RemoveFromCart' class='btn btn-danger form-control' name='remove'>Remove From Cart</button>")

            }else{
                span_added.html("<button id='addToCart' class='btn  btn-info form-control'><i class=\"fa fa-shopping-cart\">\n" +
                    "                            </i> Add to cart </button>")

            }

            cart_items_count.text(data.cart_items_count)

            // if(window.location.href.indexOf("cart") != -1){
            // RefreshCart()
            // }else{
            //
            // }
            location.reload()
        },
        error: function (data) {
            console.log(("Error with adding the product to the cart!"))
        }

    });

})


remove_from_cart_btn.click(function (event) {
    event.preventDefault()
    $this= $(this)
    // console.log($this.attr('id'))
    data= {
        'product_id':$this.val()
    }
    $.ajax({
        url:'/cart/api/remove_form_cart/',
        method:'post',
        data:data,
        success: function (data) {
            console.log(data.product_list)
            cart_items_count.text(data.cart_items_count)
            if(data.product_list.length > 0){
                var i=data.product_list.length
                $.each(data.product_list,function (index,obj) {
                    // console.log("obj",obj)
                    // console.log(Cart_Modal_body.find("#Cart_Modal_content").html())
                    Cart_Modal_body.empty()
                    Cart_Modal_body.html("<div class=\"media\">" +
                        "<a href="+obj.url+" class=\"mr-2\">" +
                        "<img class=\"img-fluid rounded\" src={% if" + obj.image_url  + "%}"+  + obj.image_url + "{% endif %} width=\"50\" alt=\"item image\"></a>"+

                        "<div class=\"media-body\" >"+
                        "<div id=\"Cart_Modal_content\">" +
                        "<a href="+ obj.url+" class=\"text-dark\">"+ obj.name + "</a></div>"+
                        "<span class=\"text-secondary\">KD " + obj.price+ "</span>" +
                        "<button class=\"remove_from_cart_btn btn close remove btn-link\" " +
                        "name=\"remove\" value=\""+ obj.id + "\">remove</button>"+
                        "</div></div>"
                    )
                    i--
                })


            }else{
                cartModal_items_count.html(data.cart_items_count+ '&nbsp;')
                cart_items_count.text(data.cart_items_count)
                Cart_Modal_body.empty()
                cart_product_ajax.find('.span-added').html("<button id='addToCart' class='btn  btn-info form-control'><i class=\"fa fa-shopping-cart\"> </i> Add to cart </button>")



            }


        },
        error: function (error) {
         console.log(error)
        }

    })
})



var FilterBy = $('.FilterBy')   // form class name
    // var input = FilterBy.find("[name='filter_brand']")

    FilterBy.on('change',function () {
        var brand =""

        $(':input[name=filter_brand]:checked').each(function() {
            $this= $(this)
            brand+=$this.val()
            brand+=","
        });

        var size =""

        $(':input[name=filter_size]:checked').each(function() {
            $this= $(this)
            size+=$this.val()
            size+=","
        });


        var color =""

        $(':input[name=filter_color]:checked').each(function() {
            $this= $(this)
            color+=$this.val()
            color+=","
        });


        // str=str.substring(0,str.lastIndex(','))
        // category = .split('/')
        // new_category=category[(category.length-1)]
        $.ajax({
            url:$this.attr("action"),
            method:'get',
            data:
                {
                    'filter_brand':brand,
                    'filter_size':size,
                    'filter_color':color

                },
            success: function (data) {
                new_str_size =""
                new_str_brand =""
                new_str_color=""

                $.each(size.replace(/,\s*$/, "").split(','),function (index,obj) {
                    new_str_brand+=obj+"--"

                })

                $.each(brand.replace(/,\s*$/, "").split(','),function (index,obj) {
                    new_str_size+=obj+"--"

                })

                $.each(color.replace(/,\s*$/, "").split(','),function (index,obj) {
                    new_str_color+=obj+"--"

                })
                // console.log(new_str.replace(/--\s*$/, ""))
                // console.log(window.location.href)
                window.history.pushState({}, document.title, "?"+new_str_brand.replace(/--\s*$/, "")+"--"+new_str_size.replace(/--\s*$/, "")+"--"+new_str_color.replace(/--\s*$/, ""));
                // $("html").html(data)
                // location.replace(new_str.replace(/--\s*$/, ""))
                // console.log($(data).find('#products-collection-child'))
                $('#products-collection-child').html($(data).find('#products-collection-child'))
                // console.log(data)
                // location.reload()
            },
            error: function (error) {
                console.log(error)
            }

        })
    })




// var carticonModal = $('#carticonModal')
// carticon_id.click(function (e) {
//
//     $.ajax({
//          url: '/cart/api/get_cart',
//          method: 'GET',
//         success: function (data) {
//          console.log(data[0].fields['products'])
//             carticonModal.find("[name='carticon']").val(data[0].fields['products'])
//           console.log(carticonModal.find("[name='carticon']").val(data[0].fields['products']))
//
//         },
//         error: function (error) {
//          console.log(error)
//         }
//
//     })
//
// })

function RefreshCart() {
    //alert("refreshcart")
    var carttable=$(".cart_table")
    var cartbody =carttable.find(".cart_body")
    var cart_product_rows=cartbody.find(".cart_products_rows")
    var cart_total=cartbody.find(".cart_total")
    var cart_subtotal=cartbody.find(".cart_subtotal")

    //cartbody.html("<h1>hossam</h1>")

    var RefreshUrl = "/api/show";
    var RefreshMethod = "GET"
    var RefreshData= {}
    var cart_item_remove_form=$(".cart_item-remove-form")
    //var currenturl = window.location.href

    $.ajax({
        url: RefreshUrl,
        method: RefreshMethod,
        data: RefreshData,
        success: function (data) {
            //console.log(data)


            if(data.product.length > 0){
                var i=data.product.length
                $.each(data.product,function (index,obj) {
                    console.log("obj",obj)
                    cart_item_remove_form.find(".removed_product_id").val(obj.id)
                    cartbody.prepend("<tr><th scope=\"row\">"+i+"</th><td ><a href='"+obj.url+"'>"+obj.name+"</a>" +
                        "<small>"+cart_item_remove_form.html()+"</small></td>" +
                        "<td>"+ obj.price +"</td></tr>")
                    i--
                })
                 cart_total.text(data.cart_subtotal)
                 cart_total.text(data.cart_total)

            }
        },
        error: function (data) {
            console.log(("error"))
        }

    });

}
$(".change").click(function () {
    event.preventDefault();

    $.ajax({
        action:'/cart/checkout/',
        method:'POST',
        data:{
            'change':true
        },
        success: function (data) {
            // console.log(data)

        },
        error: function (error) {
            console.log(error)
        }
    })

})

})