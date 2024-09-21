// Initialiser tous les popovers
document.addEventListener('DOMContentLoaded', function () {
    let popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]')
    popoverTriggerList.forEach(function(popoverTriggerEl){
        // On lance le popover
        new bootstrap.Popover(popoverTriggerEl);
    });
});