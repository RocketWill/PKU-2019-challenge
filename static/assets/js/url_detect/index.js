
$(document).ready(function(){

    resizeContent();

    $(window).resize(function() {
        resizeContent();
    });
    
   $('.services-item').matchHeight();
});

function resizeContent() {
    $height = $(window).height() -250;
     $('#page-frame').height($height);
}