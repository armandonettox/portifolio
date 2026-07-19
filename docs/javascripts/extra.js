/* Scripts das paginas. Usa document$ do Material porque com navigation.instant
   o DOMContentLoaded so dispara no primeiro carregamento. */

document$.subscribe(function () {
  /* saudacao por horario na home */
  var saudacao = document.getElementById("pf-saudacao");
  if (saudacao) {
    var hora = new Date().getHours();
    var periodo = hora < 12 ? "bom dia" : hora < 18 ? "boa tarde" : "boa noite";
    saudacao.textContent = "Olá, " + periodo;
  }

  /* botao de copiar e-mail na pagina de contato */
  document.querySelectorAll(".pf-copy-btn").forEach(function (btn) {
    if (btn.dataset.pfBound) return;
    btn.dataset.pfBound = "1";
    btn.addEventListener("click", function () {
      var email = btn.getAttribute("data-copy");
      navigator.clipboard.writeText(email).then(function () {
        var original = btn.textContent;
        btn.textContent = "Copiado!";
        btn.classList.add("pf-copy-done");
        setTimeout(function () {
          btn.textContent = original;
          btn.classList.remove("pf-copy-done");
        }, 1500);
      });
    });
  });
});
