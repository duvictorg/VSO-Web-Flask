document.addEventListener('DOMContentLoaded', function () {
    const Prof_btn = document.querySelector("#Prof-btn");
    const eleve_btn = document.querySelector("#eleve-btn");
    const matiereField = document.querySelector(".matiere-field");
    const classeFields = document.querySelector(".classe-fields");
    const addBtn = document.querySelector('#add');
    const deleteBtn = document.querySelector('#delete');
    const addForm = document.querySelector('#add-form');
    const deleteForm = document.querySelector('#delete-form');

    Prof_btn.addEventListener('click', () => {
        matiereField.style.display = "block";
        classeFields.style.display = "none";
    });

    eleve_btn.addEventListener('click', () => {
        matiereField.style.display = "none";
        classeFields.style.display = "flex";
    });

    addBtn.addEventListener('click', function () {
        addForm.style.display = 'block';
        deleteForm.style.display = 'none';
    });

    deleteBtn.addEventListener('click', function () {
        addForm.style.display = 'none';
        deleteForm.style.display = 'block';
    });
});
