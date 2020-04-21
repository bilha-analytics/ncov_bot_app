document.addEventListener("DOMContentLoaded", function(event) { 
    setupScreen()
});


$(document).ready(function(){
    setupScreen()
}); 

function setupScreen(){
    //full screen it
    document.documentElement.requestFullscreen()
    document.location.hash = '#bottomz';     
    document.getElementById('askBot').focus(); 
    document.getElementById('jhumap').src = document.getElementById('jhumap').src 
}