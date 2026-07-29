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
});
