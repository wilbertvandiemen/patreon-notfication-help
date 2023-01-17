$( document ).ready(function() {
    var socket = io.connect(window.location.origin);

    socket.on('from server', function(msg) {
         try{
            //navigator.clipboard.writeText(msg);
            copyToClipboard(msg)
         } catch {
         }
         $('#result').val(msg)
    });

    $('#send').on('click', function() {

        var emoticons = $('#emoticons').val();
        var naam = $('input.naam:checked').val()
        var tekst = $('input.tekst:checked').val()

        socket.emit('message', {'tekst' : tekst, 'emoticons' : emoticons, 'naam' : naam});

    });

    function copyToClipboard(text) {
      var $temp = $("<input>");
      $("body").append($temp);
      $temp.val(text).select();
      document.execCommand("copy");
      $temp.remove();
}


});
