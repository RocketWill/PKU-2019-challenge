
$(document).ready(function(){
    /*
    resizeContent();
    */
    $(window).resize(function() {
        $('.services-item').matchHeight();
    });
    
   $('.services-item').matchHeight();
});

function resizeContent() {
    $height = $(window).height() - 250;
    $('#hero-area').height($height);
}