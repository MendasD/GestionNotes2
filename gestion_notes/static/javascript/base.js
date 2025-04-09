// Toggle sidebar
document.getElementById("toggleSidebar").addEventListener("click", function() {
    if (document.getElementById("sidebar").classList.toggle("deactive")){
            document.getElementById("sidebar").classList.toggle("active");
            document.getElementById("mainContent").classList.toggle("reshifted");
            document.getElementById("sidebar").classList.remove('deactivate');
            document.getElementById("mainContent").classList.remove('shifted');
    } else {
        
        document.getElementById("sidebar").classList.toggle("active");
        document.getElementById("mainContent").classList.toggle("shifted");
        document.getElementById("sidebar").classList.remove('activate');
        document.getElementById("mainContent").classList.remove('reshifted');
    };
});



document.addEventListener("DOMContentLoaded", function () {
    let links = document.querySelectorAll(".nav-link");
    let currentUrl = window.location.pathname; // Récupère la page actuelle

    links.forEach(link => {
    if (link.getAttribute("href") === currentUrl) {
        if(!link.classList.contains("dropdown-item") && !link.classList.contains("dropdown-item-text")){    
            link.classList.add("active"); // Ajoute la classe active au lien
        }

        // Vérifier si le lien est dans un dropdown et activer le parent
        let dropdown = link.closest(".dropdown-menu"); // Trouve le menu parent
        if (dropdown) {
            let parentLink = dropdown.previousElementSibling; // Sélectionne le <a class="dropdown-toggle">
            if (parentLink) {
                parentLink.classList.add("active"); // Active le parent
            }
        }
    }
    });
});
   