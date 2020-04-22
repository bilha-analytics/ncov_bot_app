document.addEventListener("DOMContentLoaded", function(event) { 
    setupScreen()
});


$(document).ready(function(){
    setupScreen()
}); 

function setupScreen(){
    document.location.hash = '#bottomz';     
    document.getElementById('askBot').focus(); 
    
    //full screen it
    document.documentElement.requestFullscreen()

    window.onload = function() {
        window.moveTo(0, 0);

        if (document.all) {
            top.window.resizeTo(screen.availWidth, screen.availHeight);
        }

        else if (document.layers || document.getElementById) {
            if (top.window.outerHeight < screen.availHeight || top.window.outerWidth < screen.availWidth) {
                top.window.outerHeight = screen.availHeight;
                top.window.outerWidth = screen.availWidth;
            }
        }
    }
}