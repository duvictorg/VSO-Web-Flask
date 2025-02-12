document.addEventListener('DOMContentLoaded', function () {
    const Prof_btn = document.querySelector("#Prof-btn");
    const Eleve_btn = document.querySelector("#Eleve-btn");
    const matiereFields = document.querySelectorAll(".matiere-field");
    const classeFields = document.querySelectorAll(".classe-fields");
    const addBtn = document.querySelector('#add');
    const editBtn = document.querySelector('#edit');
    const deleteBtn = document.querySelector('#delete');
    const addForm = document.querySelector('#add-form');
    const editForm = document.querySelector('#edit-form');
    const deleteForm = document.querySelector('#delete-form');

    function toggleFields(isMatiere) {
        matiereFields.forEach(field => {
            field.style.display = isMatiere ? "block" : "none";
        });
        classeFields.forEach(field => {
            field.style.display = isMatiere ? "none" : "flex";
        });
    }

    Prof_btn.addEventListener('click', () => toggleFields(true));
    Eleve_btn.addEventListener('click', () => toggleFields(false));

    addBtn.addEventListener('click', function () {
        addForm.style.display = 'block';
        editForm.style.display = 'none';
        deleteForm.style.display = 'none';
    });

    editBtn.addEventListener('click', function () {
        addForm.style.display = 'none';
        editForm.style.display = 'block';
        deleteForm.style.display = 'none';
    });

    deleteBtn.addEventListener('click', function () {
        addForm.style.display = 'none';
        editForm.style.display = 'none';
        deleteForm.style.display = 'block';
    });
});
