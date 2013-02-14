$(function(){

    var $search_results = $("#search-results");
        source = $("#search-item-template").html(),
        template = Handlebars.compile(source);

    $(".editable").focusin(function(){
        var $input = $(this);
        $input.parents('.control-group').removeClass("error");
        $input.siblings('.help-inline').text('');
    });

    $("#search-form").submit(function(e){
        e.preventDefault();
        $search_results.empty();
        var csrfToken = $.cookie('_csrf_token'),
            text = $("input[name=search_text]").val(),
            params = {'_csrf_token': csrfToken,
                      'search_text': text,
                      'search_by': $("input[name=search_by]:checked").val()
                     };
        if(text === ''){
            return;
        }
        $.post('/', params, function(data){
            if(data.errors){
                console.log('Error');
            } else {
                var result = data.result;
                if (result.length !== 0) {
                    result.forEach(function(item){
                        var rendered_html = template(item);
                        $search_results.append(rendered_html);
                    });
                } else {
                    $search_results.append("<p class='text-info'>Not found</p>");
                }
            }
        });
    });

});