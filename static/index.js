$('#all_recipes_list').on('click', '.stars a', function(){
    $(this).closest(".stars span").removeClass('active');
    $(this).prevAll(".stars span a").removeClass('active');
    $(this).nextAll(".stars span a").removeClass('active');
    $(this).addClass('active');
    $(this).closest(".stars span").addClass('active');
});
