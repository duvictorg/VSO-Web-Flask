document.addEventListener('DOMContentLoaded', function () {
    const Prof_btn = document.querySelector("#Prof-btn");
    const eleve_btn = document.querySelector("#Eleve-btn");
    const matiereField = document.querySelector(".matiere-field");
    const classeFields = document.querySelector(".classe-fields");
    const addBtn = document.querySelector('#add');
    const editBtn = document.querySelector('#edit');
    const deleteBtn = document.querySelector('#delete');
    const addForm = document.querySelector('#add-form');
    const deleteForm = document.querySelector('#delete-form');
    const eleveselect = document.querySelector('#select-eleve');
    const teacherselect = document.querySelector('#select-prof');

    Prof_btn.addEventListener('click', () => {
        matiereField.style.display = "none";
        classeFields.style.display = "block";
        teacherselect.style.display = "block";
    });

    eleve_btn.addEventListener('click', () => {
        matiereField.style.display = "flex";
        classeFields.style.display = "none";
        teacherselect.style.display = "none";
    });

    addBtn.addEventListener('click', function () {
        addForm.style.display = 'block';
        deleteForm.style.display = 'none';
    });

    editBtn.addEventListener('click', function () {
        addForm.style.display = 'none';
        deleteForm.style.display = 'block';
    });

    deleteBtn.addEventListener('click', function () {
        addForm.style.display = 'none';
        deleteForm.style.display = 'block';
    });
});
