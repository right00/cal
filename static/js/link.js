$(function(){
    $('.autolink').each(function(){
        $(this).html($(this).html().replace(/\r?\n/g, '<br>'));
    });
});
$(function(){
    $('.autolink').each(function(){
        $(this).html($(this).html().replace(/(\b(https?|ftp|file):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])/ig,"<a href='$1' class='inks'  target='_blank' rel='noopener noreferrer'>$1</a>"));
    });
});


