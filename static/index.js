$('#all_recipes_list').on('click', '.stars a', function(e){
    $(this).closest(".stars span").removeClass('active');
    $(this).prevAll(".stars span a").removeClass('active');
    $(this).nextAll(".stars span a").removeClass('active');
    $(this).addClass('active');
    $(this).closest(".stars span").addClass('active');

    // alert($(this).text());
    // alert($(this).closest(".listica").attr('id'));


    e.preventDefault();
    var package = {};
    package.rating = $(this).text();
    package.identifier = $(this).closest(".listica").attr('id');

    post_ajax('http://localhost:8000/', JSON.stringify(package), rating_ok, rating_not_ok);

});

function post_ajax(url, data, success_function, failure_function) {
    //var token = get_cookie("_xsrf");
    //alert(token);

    $.ajax({
      type: 'POST',
      url: url,
      headers : {
        //'X-XSRFToken' : token
      },
      data: data,
      contentType: "json",
      success: success_function,
      error: failure_function
    });
}

function rating_ok(data){

    // TODO: set value of an rating in recipe
    // alert(data);
    obj = JSON.parse(data);
    //alert(obj.identifier);
    //alert(id)
    //rating = data.avg_rating
    $('#'+obj.identifier+' .averaged').html('<a style="font-weight: 600;">This meal has rating number of: </a>'+obj.avg_rating);

}

function rating_not_ok(data){
    // TODO: alert error
}