function telechargerTable(classe) {
    // Charger la bibliothèque ExcelJS
     const workbook = new ExcelJS.Workbook();
     const worksheet = workbook.addWorksheet('Liste des étudiants de ' + classe);

     // Ajouter l'en-tête 
     worksheet.mergeCells('A1:C1');
     worksheet.getCell('A1').value = 'Liste des étudiants de ' + classe;
     worksheet.getCell('A1').font = { size: 14, bold: true, color: { argb: 'FF0000FF' } }; // Texte en bleu
     worksheet.getCell('A1').alignment = { horizontal: 'center' };

     worksheet.addRow(['Matricule', 'Nom et prénom', 'Année Scolaire']);
     worksheet.getRow(2).font = { bold: true };

     // Extraire les données de la table
     var table = document.querySelector('#' + classe + ' table tbody');
     var rows = table.querySelectorAll('tr');
     
     rows.forEach(function(row) {
         var cols = row.querySelectorAll('td');
         if (cols.length > 0) {
             var rowData = [];
             // Ignorer la dernière colonne (Actions)
             for (var i = 0; i < cols.length - 1; i++) {
                 rowData.push(cols[i].innerText.trim());
             }
             worksheet.addRow(rowData);
         }
     });

     // Appliquer des bordures sur toutes les cellules remplies
     worksheet.eachRow({ includeEmpty: false }, function (row, rowNumber) {
         row.eachCell({ includeEmpty: false }, function (cell, colNumber) {
             cell.border = {
                 top: { style: 'thin' },
                 left: { style: 'thin' },
                 bottom: { style: 'thin' },
                 right: { style: 'thin' }
             };
         });
     });

     // Générer et télécharger le fichier Excel avec le nom dynamique
     var fileName = classe + "_etudiants.xlsx" +  ".xlsx";
     workbook.xlsx.writeBuffer().then(function (data) {
         var blob = new Blob([data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
         var url = window.URL.createObjectURL(blob);
         var a = document.createElement('a');
         a.href = url;
         a.download = fileName;
         a.click();
         window.URL.revokeObjectURL(url);
     });
 }





 /*
function telechargerTable(classe) {
    var data = [];
    // Ajouter les en-têtes
    data.push(['Matricule', 'Nom', 'Année Scolaire']);
    
    // Extraire les données de la table
    var table = document.querySelector('#' + classe + ' table tbody');
    var rows = table.querySelectorAll('tr');
    
    rows.forEach(function(row) {
        var cols = row.querySelectorAll('td');
        if (cols.length > 0) {
            var rowData = [];
            // Ignorer la dernière colonne (Actions)
            for (var i = 0; i < cols.length - 1; i++) {
                rowData.push(cols[i].innerText.trim());
            }
            data.push(rowData);
        }
    });
    
    // Créer un nouveau classeur Excel
    var wb = XLSX.utils.book_new();
    var ws = XLSX.utils.aoa_to_sheet(data);
    XLSX.utils.book_append_sheet(wb, ws, "Liste d'Étudiants");
    XLSX.writeFile(wb, classe + "_etudiants.xlsx");
}
*/


/*
Pour remplir une maquette excel existante avant de la telecharger


<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Remplir et Télécharger Excel</title>
</head>
<body>

    <button id="downloadExcel">Télécharger le fichier Excel modifié</button>

    <script>
        document.getElementById('downloadExcel').addEventListener('click', async function() {
            // Créer un nouveau workbook Excel
            var workbook = new ExcelJS.Workbook();

            // Charger le fichier Excel existant (la maquette dans votre projet)
            await fetch('/path/to/your/excel/template.xlsx')  // Remplacez avec le bon chemin vers votre maquette
                .then(response => response.arrayBuffer())
                .then(data => {
                    return workbook.xlsx.load(data);
                });

            // Sélectionner la feuille de calcul que vous souhaitez modifier (par index ou par nom)
            var worksheet = workbook.getWorksheet(1);  // Utilisez le nom ou l'index (commence à 1)

            // Remplir les cellules avec des données
            worksheet.getCell('A2').value = "Nouvelle valeur A2";
            worksheet.getCell('B2').value = "Nouvelle valeur B2";
            worksheet.getCell('C2').value = 42;  // Un exemple de valeur numérique

            // Générer le fichier Excel modifié et préparer le téléchargement
            workbook.xlsx.writeBuffer().then(function(buffer) {
                // Créer un Blob et déclencher le téléchargement
                var blob = new Blob([buffer], { type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" });
                var link = document.createElement('a');
                link.href = URL.createObjectURL(blob);
                link.download = 'maquette_modifiee.xlsx';  // Nom du fichier téléchargé
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            });
        });
    </script>

</body>
</html>


*/