// Algorithmes de recherche
document.addEventListener('DOMContentLoaded', function () {
    // On recupere tous les cadres de messages
    let box_messages = document.querySelectorAll('.box-message');
    
    // Recherche par date
    let search_date = document.getElementById('search_date');
    search_date.addEventListener('input', function () {
        let search_value = search_date.value;
        box_messages.forEach(function(box) {
            let date = box.getAttribute('data-date');
            // S'il y a un contenu dans la zone de recherche par sujet
            if(document.getElementById('search_content').value){
                content = document.getElementById('search_content').value
                box.style.display = ((date === search_value)&&(box.getAttribute('data-sujet').toLowerCase().includes(content.toLowerCase())))? 'block':'none';
            }else{
                box.style.display = (date === search_value)? 'block':'none';
            }
        })
    });

    // Recherche par contenu
    let search_content = document.getElementById('search_content');
    search_content.addEventListener('input', function () {
        let search_value = search_content.value.toLowerCase();
        box_messages.forEach(function(box) {
            let content = box.getAttribute('data-sujet').toLowerCase();
            // S'il y a un contenu dans la zone de recherche par date
            if (search_date.value){
                box.style.display = (content.includes(search_value)&&(search_date.value===box.getAttribute('data-date')))? 'block':'none';
            }else{
                box.style.display = content.includes(search_value)? 'block':'none';
            }
        })
    });
})