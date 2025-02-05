const Prof_btn = document.querySelector("#Prof-btn");
const eleve_btn = document.querySelector("#eleve-btn");
const matiereField = document.querySelector(".matiere-field");
const classeField = document.querySelector(".classe-field");

Prof_btn.addEventListener('click', () => {
    matiereField.style.display = "block";
    classeField.style.display = "none";
});

eleve_btn.addEventListener('click', () => {
    matiereField.style.display = "none";
    classeField.style.display = "block";
});
