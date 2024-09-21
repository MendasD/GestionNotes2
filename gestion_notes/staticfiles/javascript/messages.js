// On récupère tous les boutons d'ouverture
let open_btn = document.querySelectorAll('.open-btn');

for (let i = 0; i < open_btn.length; i++) {
    open_btn[i].addEventListener('click', function () {
        let id_message = this.getAttribute('data-id');

        // Requête AJAX pour marquer le message comme lu
        fetch(`/message_to_lu/${id_message}`, {
            method: 'GET',
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            if (data.status === 'success') {
                console.log('Message marqué comme lu');
            } else {
                console.error('Erreur lors de la mise à jour du statut du message');
            }
        })
        .catch(error => {
            console.error('Erreur lors de la requête AJAX:', error);
        });

        // Afficher le modal avec Bootstrap
        let modalElement = document.getElementById(`messageModal${id_message}`);
        
        if (modalElement) {
            let modal = new bootstrap.Modal(modalElement);
            modal.show();
        } else {
            console.error("Le modal n'existe pas pour ce message");
        }
    });
}

