// Duree d'affichage des messages
setTimeout(function(){
    var messages = document.querySelector('.messages');
    if(messages) {
        messages.style.display = 'none';
    }
}, 3000);  // 3000 millisecondes = 3 secondes