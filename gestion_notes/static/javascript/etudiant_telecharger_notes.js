document.getElementById('telechargerExcelBtn').addEventListener('click', function () {
     
    // Charger la bibliothèque ExcelJS
    const workbook = new ExcelJS.Workbook();
    const worksheet = workbook.addWorksheet('Bulletin');

    // Créer un tableau pour contenir les données combinées des deux semestres
    var data = [];

    // Extraire les informations du premier tableau (étudiant)
    var nomEtudiant = document.querySelector('table tbody tr td:nth-child(2)').innerText.trim();
    var classeEtudiant = document.querySelector('table tbody tr td:nth-child(3)').innerText.trim();
    var anneeScolaire = document.querySelector('table tbody tr td:nth-child(4)').innerText.trim();

    // Ajouter l'en-tête du bulletin
    worksheet.mergeCells('A1:D1');
    worksheet.getCell('A1').value = 'Bulletin de notes';
    worksheet.getCell('A1').font = { size: 16, bold: true, color: { argb: 'FF0000FF' } }; // Texte en bleu
    worksheet.getCell('A1').alignment = { horizontal: 'center' };

    // Ajouter les entêtes pour les informations de l'étudiant
    worksheet.mergeCells('A2:B2');
    worksheet.getCell('A2').value = 'Nom et prénom ' 
    worksheet.getCell('C2').value = 'Classe '
    worksheet.getCell('D2').value = 'Année scolaire '
    
    // Ajouter les informations de l'étudiant
    worksheet.mergeCells('A3:B3');
    worksheet.getCell('A3').value =  nomEtudiant;
    worksheet.getCell('A3').font = { bold: true };
    worksheet.getCell('C3').value = classeEtudiant;
    worksheet.getCell('C3').font = { bold: true };
    worksheet.getCell('D3').value = anneeScolaire;
    worksheet.getCell('D3').font = { bold: true };

    // Ajouter une ligne vide
    worksheet.addRow([]);

    // Ajouter l'en-tête des matières
    worksheet.addRow(['Matière', 'Crédit', 'Note 1', 'Note 2']);
    worksheet.getRow(5).font = { bold: true };
    ['A','B','C','D'].forEach((i) => {
        worksheet.getCell(`${i}5`).fill = {
            type: 'pattern', // indique que l'utilisation d'un motif de remplissage
            pattern: 'solid', // pour indiquer l'utilisation d'une couleur unie (uniforme, i.e sans variance de teinte)
            fgColor: { argb: 'FFFFD700' } // Fond jaune
        };
    })
    

    // Fonction pour extraire les données de deux tableaux simultanément
    function extractTableDataSideBySide(tableId1, tableId2, semester) {
        var table = document.getElementById(tableId1);
        var rows = table.querySelectorAll('tbody tr');
        // Ajout du semestre
        var row = worksheet.addRow([semester]);  
        worksheet.mergeCells(`A${row.number}:D${row.number}`);  // Fusionner de A à D sur la ligne courante
        worksheet.getCell(`A${row.number}`).alignment = { horizontal: 'center' };  // Centrer le texte
        worksheet.getCell(`A${row.number}`).font = { bold: true };  // Mettre le texte en gras


        rows.forEach((row) => {
            var rowData = [];
            var cols = row.querySelectorAll('td');
            cols.forEach(function (col) {
                rowData.push(col.innerText.trim());
            });
            worksheet.addRow(rowData);
        });
    }

    // Extraire les données des deux tableaux
    extractTableDataSideBySide('tableSemestre1', null, 'Semestre 1');
    worksheet.addRow([]);
    extractTableDataSideBySide('tableSemestre2', null, 'Semestre 2');

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
    var fileName = nomEtudiant + "_" + classeEtudiant + "_" + anneeScolaire + ".xlsx";
    workbook.xlsx.writeBuffer().then(function (data) {
        var blob = new Blob([data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
        var url = window.URL.createObjectURL(blob);
        var a = document.createElement('a');
        a.href = url;
        a.download = fileName;
        a.click();
        window.URL.revokeObjectURL(url);
    });

})





/*
document.getElementById('telechargerExcelBtn').addEventListener('click', function () {
    // Créer un tableau pour contenir les données combinées des deux semestres
    var data = [];

    // Extraire les informations du premier tableau (étudiant)
    var nomEtudiant = document.querySelector('table tbody tr td:nth-child(2)').innerText.trim();
    var classeEtudiant = document.querySelector('table tbody tr td:nth-child(3)').innerText.trim();
    var anneeScolaire = document.querySelector('table tbody tr td:nth-child(4)').innerText.trim();

    // Ajouter l'en-tête 
    data.push(['Matière', 'Crédit', 'Note 1', 'Note 2']);

    // Fonction pour extraire les données de deux tableaux simultanément
    function extractTableDataSideBySide(tableId1, tableId2) {
        var table1 = document.getElementById(tableId1);
        var table2 = document.getElementById(tableId2);
        
        var rows1 = table1.querySelectorAll('tbody tr');
        var rows2 = table2.querySelectorAll('tbody tr');

        data.push(['', '', '', '']);
        data.push(['Semestre 1','','','']);
        for (var i = 0; i < rows1.length; i++) {
            var rowData = [];

            // Remplir les données du tableau Semestre 1
            if (rows1[i]) {
                var cols1 = rows1[i].querySelectorAll('td');
                cols1.forEach(function (col) {
                    rowData.push(col.innerText.trim());
                });
            } else {
                rowData.push('', '', '', '');  // Lignes vides si le Semestre 1 a moins de lignes
            }

            data.push(rowData);
        }

        // Ajout d'une ligne vide pour espacer les deux semestres
        data.push(['', '', '', '']);
        data.push(['Semestre 2','','','']);

        for (var i = 0; i < rows2.length; i++) {
            var rowData = [];

            // Remplir les données du tableau Semestre 1
            if (rows2[i]) {
                var cols2 = rows2[i].querySelectorAll('td');
                cols2.forEach(function (col) {
                    rowData.push(col.innerText.trim());
                });
            } else {
                rowData.push('', '', '', '');  // Lignes vides si le Semestre 2 a moins de lignes
            }

            data.push(rowData);
        }

    }

    // Extraire les données des deux tableaux en les joignant côte à côte
    extractTableDataSideBySide('tableSemestre1', 'tableSemestre2');

    // Créer un nouveau classeur Excel
    var wb = XLSX.utils.book_new();

    // Créer une nouvelle feuille de calcul avec les données extraites
    var ws = XLSX.utils.aoa_to_sheet(data);

    // Ajouter la feuille de calcul au classeur
    XLSX.utils.book_append_sheet(wb, ws, "Notes");

    // Générer et télécharger le fichier Excel avec le nom dynamique
    var fileName = nomEtudiant + "_" + classeEtudiant + "_" + anneeScolaire + ".xlsx";
    XLSX.writeFile(wb, fileName);

})
*/



/*
document.getElementById('telechargerExcelBtn').addEventListener('click', function () {
    // Créer un tableau pour contenir les données combinées des deux semestres
    var data = [];

    // Extraire les informations du premier tableau (étudiant)
    var nomEtudiant = document.querySelector('table tbody tr td:nth-child(2)').innerText.trim();
    var classeEtudiant = document.querySelector('table tbody tr td:nth-child(3)').innerText.trim();
    var anneeScolaire = document.querySelector('table tbody tr td:nth-child(4)').innerText.trim();

    // Ajouter l'en-tête pour Semestre 1 et Semestre 2 côte à côte
    data.push(['Matière S1', 'Crédit S1', 'Note 1 S1', 'Note 2 S1', '', 'Matière S2', 'Crédit S2', 'Note 1 S2', 'Note 2 S2']);
    
    // Fonction pour extraire les données de deux tableaux simultanément
    function extractTableDataSideBySide(tableId1, tableId2) {
        var table1 = document.getElementById(tableId1);
        var table2 = document.getElementById(tableId2);
        
        var rows1 = table1.querySelectorAll('tbody tr');
        var rows2 = table2.querySelectorAll('tbody tr');

        var maxRows = Math.max(rows1.length, rows2.length);  // Obtenir le plus grand nombre de lignes

        for (var i = 0; i < maxRows; i++) {
            var rowData = [];

            // Remplir les données du tableau Semestre 1
            if (rows1[i]) {
                var cols1 = rows1[i].querySelectorAll('td');
                cols1.forEach(function (col) {
                    rowData.push(col.innerText.trim());
                });
            } else {
                rowData.push('', '', '', '');  // Lignes vides si le Semestre 1 a un nombre de lignes inerieur à maxRows
            }

            // Ajout d'une colonne vide pour espacer les deux semestres
            rowData.push('');

            // Remplir les données du tableau Semestre 2
            if (rows2[i]) {
                var cols2 = rows2[i].querySelectorAll('td');
                cols2.forEach(function (col) {
                    rowData.push(col.innerText.trim());
                });
            } else {
                rowData.push('', '', '', '');  // Lignes vides si le Semestre 2 a un nombre de lignes inerieur à maxRows
            }

            data.push(rowData);  // Ajouter la ligne complète au tableau de données
        }
    }

    // Extraire les données des deux tableaux en les joignant côte à côte
    extractTableDataSideBySide('tableSemestre1', 'tableSemestre2');

    // Créer un nouveau classeur Excel
    var wb = XLSX.utils.book_new();

    // Créer une nouvelle feuille de calcul avec les données extraites
    var ws = XLSX.utils.aoa_to_sheet(data);

    // Ajouter la feuille de calcul au classeur
    XLSX.utils.book_append_sheet(wb, ws, "Notes");

    // Générer et télécharger le fichier Excel avec le nom dynamique
    var fileName = nomEtudiant + "_" + classeEtudiant + "_" + anneeScolaire + ".xlsx";
    XLSX.writeFile(wb, fileName);
});
*/
