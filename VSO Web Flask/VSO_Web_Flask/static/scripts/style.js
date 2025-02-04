const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn = document.querySelector("#sign-up-btn");
const Prof_btn = document.querySelector("#Prof-btn");
const eleve_btn = document.querySelector("#eleve-btn");
const container = document.querySelector(".form-container");
const matiereField = document.querySelector(".matiere-field");

sign_up_btn.addEventListener('click', () => {
    container.classList.add("sign-up-mode");
});

sign_in_btn.addEventListener('click', () => {
    container.classList.remove("sign-up-mode");
});

Prof_btn.addEventListener('click', () => {
    matiereField.style.display = "block";
});

eleve_btn.addEventListener('click', () => {
    matiereField.style.display = "none";
});