document.addEventListener("DOMContentLoaded", () => {
    const rows = document.querySelectorAll("tr[data-href]")
    console.log(rows);


    rows.forEach(row => {
        rows.addEventListener("click", () => {
            windows.location.href = row.dataset.href;
        });
    });
});