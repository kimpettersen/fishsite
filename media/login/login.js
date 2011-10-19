$(document).ready(function() {
    $('#id_username').keyup(function() {
        //Get username when user types. This creates a lot of db activity        
        var uname = document. getElementById('id_username').value;
        //parse the string to JSON
        var obj = jQuery.parseJSON('{"username":"'+ uname +'"}');
        if (obj.username != ''){
            //Check if username is availabe            
            $.ajax({
            url: "/login/checkusername/" + obj.username,
            success: function(data){
                    response = jQuery.parseJSON(data)
                    if (response.user_exists === true){
                        $('#availability').empty().append('User already exists..');
                    }
                     else{
                    $('#availability').empty().append('Username is available')
                    }                
                }
            });    
        }
        
    });
 });
