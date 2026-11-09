document.getElementById("formularz").addEventListener("submit", async (e) => {
  e.preventDefault();

  try {
    await zapytanie("/api/login", { nazwa: document.getElementById("nazwa").value });
    location.href = "menu.html";
  } catch (blad) {
    document.getElementById("blad").textContent = blad.message;
  }
});

// jak ktoś jest już zalogowany to od razu do menu
fetch("/api/ja").then((odp) => {
  if (odp.ok) {
    location.href = "menu.html";
  }
});
