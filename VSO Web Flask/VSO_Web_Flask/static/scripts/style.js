const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn = document.querySelector("#sign-up-btn");
const Prof_btn = document.querySelector("#Prof-btn");
const eleve_btn = document.querySelector("#eleve-btn");
const container = document.querySelector(".form-container");

sign_up_btn.addEventListener('click', () => {
    container.classList.add("sign-up-mode");
});

sign_in_btn.addEventListener('click', () => {
    container.classList.remove("sign-up-mode");
});


Prof_btn.addEventListener('click', () => {
    container.classList.remove("");
});

eleve_btn.addEventListener('click', () => {
    container.classList.remove("");
});


function afficherDiv() {
    var div = document.getElementById("maDiv");
    if (div.style.display === "none") {
        div.style.display = "block"; // Affiche la div
    } else {
        div.style.display = "none"; // Cache la div si elle est déjà visible
    }
}