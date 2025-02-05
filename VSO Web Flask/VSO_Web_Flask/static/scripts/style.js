const Prof_btn = document.querySelector("#Prof-btn");
const eleve_btn = document.querySelector("#eleve-btn");
const Add_btn = document.querySelector("#Add-btn");
const Modif_btn = document.querySelector("#Modif-btn");
const Sup_btn = document.querySelector("#Sup-btn");
const AddField = document.querySelector(".Add-field");
const ModifField = document.querySelector(".Modif-field");
const SupField = document.querySelector(".Sup-field");
const ProfField = document.querySelector(".Prof-field");
const eleveField = document.querySelector(".eleve-field");




Prof_btn.addEventListener('click', () => {
    Add_btn.addEventListener('click', () => {
        matiereField.style.display = "none";
        classeField.style.display = "none";
        AddField.style.display = "block";
        ModifField.style.display = "none";
        SupField.style.display = "none";
    });
    Modif_btn.addEventListener('click', () => {
        matiereField.style.display = "none";
        classeField.style.display = "none";
        AddField.style.display = "none";
        ModifField.style.display = "block";
        SupField.style.display = "none";
    });
    Sup_btn.addEventListener('click', () => {
        matiereField.style.display = "none";
        classeField.style.display = "none";
        AddField.style.display = "none";
        ModifField.style.display = "none";
        SupField.style.display = "block";
    });
});

eleve_btn.addEventListener('click', () => {-
    Add_btn.addEventListener('click', () => {
        matiereField.style.display = "none";
        classeField.style.display = "none";
        AddField.style.display = "block";
        ModifField.style.display = "none";
        SupField.style.display = "none";
    });
    Modif_btn.addEventListener('click', () => {
        matiereField.style.display = "none";
        classeField.style.display = "none";
        AddField.style.display = "none";
        ModifField.style.display = "block";
        SupField.style.display = "none";
    });
    Sup_btn.addEventListener('click', () => {
        matiereField.style.display = "none";
        classeField.style.display = "none";
        AddField.style.display = "none";
        ModifField.style.display = "none";
        SupField.style.display = "block";
    });
});