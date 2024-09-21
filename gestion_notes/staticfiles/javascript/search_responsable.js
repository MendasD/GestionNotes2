document.addEventListener('DOMContentLoaded', function(){
    // On récupère tous les cadres de messages
    let box_messages = document.querySelectorAll('.box-message');

    // Recherche par classe
    let search_classe = document.getElementById('search_classe');
    search_classe.addEventListener('input',function(){
        let search_value = search_classe.value.toLowerCase();
    
        let search_subject = document.getElementById('search_subject').value.toLowerCase()
        let search_date = document.getElementById('search_date').value
        let search_student = document.getElementById('search_student').value.toLowerCase()
        box_messages.forEach(function(box){

            let correct_value = box.getAttribute('data-classe').toLowerCase()

            let correct_date = box.getAttribute('data-date');
            let correct_subject = box.getAttribute('data-sujet');
            let correct_name = box.getAttribute('data-name').toLowerCase();
            let correct_matricule = box.getAttribute('data-matricule').toLowerCase();
            if (search_date && search_student && search_subject){
                box.style.display = ((correct_value.includes(search_value))&&(search_date===correct_date)&&(correct_subject.includes(search_subject))&&((correct_name.includes(search_student))||correct_matricule.includes(search_student)))? 'block':'none';
            }else if(search_date && search_student){
                box.style.display = ((correct_value.includes(search_value))&&(search_date===correct_date)&&((correct_name.includes(search_student))||correct_matricule.includes(search_student)))? 'block':'none';
            }else if(search_date && search_subject){
                box.style.display = ((correct_value.includes(search_value))&&(search_date===correct_date)&&(correct_subject.includes(search_subject)))? 'block':'none';
            }else if(search_student && search_subject){
                box.style.display = ((correct_value.includes(search_value))&&((correct_name.includes(search_student))||correct_matricule.includes(search_student))&&(correct_subject.includes(search_subject)))? 'block':'none';
            }else if(search_date){
                box.style.display = ((correct_value.includes(search_value))&&(search_date===correct_date))? 'block':'none';
            }else if(search_student){
                box.style.display = ((correct_value.includes(search_value))&&((correct_name.includes(search_student))||correct_matricule.includes(search_student)))? 'block':'none';
            }else if(search_subject){
                box.style.display = ((correct_value.includes(search_value))&&(correct_subject.includes(search_subject)))? 'block':'none';
            }else{
                box.style.display = correct_value.includes(search_value)? 'block':'none';
            }
        })
    });

    // Recherche par étudiant
    let search_student = document.getElementById('search_student');
    search_student.addEventListener('input',function(){
        let search_value = search_student.value.toLowerCase();

        let search_classe = document.getElementById('search_classe').value.toLowerCase()
        let search_subject = document.getElementById('search_subject').value.toLowerCase()
        let search_date = document.getElementById('search_date').value
        box_messages.forEach(function(box){
            let correct_name = box.getAttribute('data-name').toLowerCase();
            let correct_matricule = box.getAttribute('data-matricule').toLowerCase();

            let correct_classe = box.getAttribute('data-classe').toLowerCase();
            let correct_subject = box.getAttribute('data-sujet');
            let correct_date = box.getAttribute('data-date');

            if (search_date && search_classe && search_subject){
                box.style.display = ((correct_name.includes(search_value)||correct_matricule.includes(search_value))&&(search_date===correct_date)&&(correct_classe.includes(search_classe))&&(correct_subject.includes(search_subject)))? 'block':'none';
            }else if(search_date && search_classe){
                box.style.display = ((correct_name.includes(search_value)||correct_matricule.includes(search_value))&&(search_date===correct_date)&&(correct_classe.includes(search_classe)))? 'block':'none';
            }else if(search_date && search_subject){
                box.style.display = ((correct_name.includes(search_value)||correct_matricule.includes(search_value))&&(search_date===correct_date)&&(correct_subject.includes(search_subject)))? 'block':'none';
            }else if(search_classe && search_subject){
                box.style.display = ((correct_name.includes(search_value)||correct_matricule.includes(search_value))&&(correct_classe.includes(search_classe))&&(correct_subject.includes(search_subject)))? 'block':'none';
            }else if(search_date){
                box.style.display = ((correct_name.includes(search_value)||correct_matricule.includes(search_value))&&(search_date===correct_date))? 'block':'none';
            }else if(search_classe){
                box.style.display = ((correct_name.includes(search_value)||correct_matricule.includes(search_value))&&(correct_classe.includes(search_classe)))? 'block':'none';
            }else if(search_subject){
                box.style.display = ((correct_name.includes(search_value)||correct_matricule.includes(search_value))&&(correct_subject.includes(search_subject)))? 'block':'none';
            }else{
                box.style.display = (correct_name.includes(search_value)||correct_matricule.includes(search_value))? 'block':'none';
            }
        })
    });

    // Recherche sujet
    let search_subject = document.getElementById('search_subject');
    search_subject.addEventListener('input',function(){
        let search_value = search_subject.value.toLowerCase();

        let search_classe = document.getElementById('search_classe').value.toLowerCase()
        let search_student = document.getElementById('search_student').value.toLowerCase()
        let search_date = document.getElementById('search_date').value
        box_messages.forEach(function(box){
            let correct_subject = box.getAttribute('data-sujet').toLowerCase();
            let correct_classe = box.getAttribute('data-classe').toLowerCase();
            let correct_name = box.getAttribute('data-name').toLowerCase();
            let correct_matricule = box.getAttribute('data-matricule').toLowerCase();
            let correct_date = box.getAttribute('data-date');

            if (search_date && search_classe && search_student){
                box.style.display = ((correct_subject.includes(search_value))&&(search_date===correct_date)&&(correct_classe.includes(search_classe))&&((correct_name.includes(search_student))||correct_matricule.includes(search_student)))? 'block':'none';
            }else if(search_date && search_classe){
                box.style.display = ((correct_subject.includes(search_value))&&(search_date===correct_date)&&(correct_classe.includes(search_classe)))? 'block':'none';
            }else if(search_date && search_student){
                box.style.display = ((correct_subject.includes(search_value))&&(search_date===correct_date)&&((correct_name.includes(search_student))||correct_matricule.includes(search_student)))? 'block':'none';
            }else if(search_classe && search_student){
                box.style.display = ((correct_subject.includes(search_value))&&(correct_classe.includes(search_classe))&&((correct_name.includes(search_student))||correct_matricule.includes(search_student)))? 'block':'none';
            }else if(search_date){
                box.style.display = ((correct_subject.includes(search_value))&&(search_date===correct_date))? 'block':'none';
            }else if(search_classe){
                box.style.display = ((correct_subject.includes(search_value))&&(correct_classe.includes(search_classe)))? 'block':'none';
            }else if(search_student){
                box.style.display = ((correct_subject.includes(search_value))&&((correct_name.includes(search_student))||correct_matricule.includes(search_student)))? 'block':'none';
            }else{
                box.style.display = correct_subject.includes(search_value)? 'block':'none';
            }
        })
    });

    // Recherche par date
    let search_date = document.getElementById('search_date');
    search_date.addEventListener('input',function(){
        let search_value = search_date.value;

        let search_classe = document.getElementById('search_classe').value.toLowerCase()
        let search_subject = document.getElementById('search_subject').value.toLowerCase()
        let search_student = document.getElementById('search_student').value.toLowerCase()
        box_messages.forEach(function(box){
            let correct_date = box.getAttribute('data-date');
            let correct_classe = box.getAttribute('data-classe').toLowerCase();
            let correct_subject = box.getAttribute('data-sujet');
            let correct_name = box.getAttribute('data-name').toLowerCase();
            let correct_matricule = box.getAttribute('data-matricule').toLowerCase();

            if (search_classe && search_subject && search_student){
                box.style.display = ((search_value===correct_date)&&(correct_classe.includes(search_classe))&&(correct_subject.includes(search_subject))&&((correct_name.includes(search_student))||correct_matricule.includes(search_student)))? 'block':'none';
            }else if(search_classe && search_subject){
                box.style.display = ((search_value===correct_date)&&(correct_classe.includes(search_classe))&&(correct_subject.includes(search_subject)))? 'block':'none';
            }else if(search_classe && search_student){
                box.style.display = ((search_value===correct_date)&&(correct_classe.includes(search_classe))&&((correct_name.includes(search_student))||correct_matricule.includes(search_student)))? 'block':'none';
            }else if(search_subject && search_student){
                box.style.display = ((search_value===correct_date)&&(correct_subject.includes(search_subject))&&((correct_name.includes(search_student))||correct_matricule.includes(search_student)))? 'block':'none';
            }else if(search_classe){
                box.style.display = ((search_value===correct_date)&&(correct_classe.includes(search_classe)))? 'block':'none';
            }else if(search_subject){
                box.style.display = ((search_value===correct_date)&&(correct_subject.includes(search_subject)))? 'block':'none';
            }else if(search_student){
                box.style.display = ((search_value===correct_date)&&((correct_name.includes(search_student))||correct_matricule.includes(search_student)))? 'block':'none';
            }else{
                box.style.display = (search_value===correct_date)? 'block':'none';
            }
        })
    });
})