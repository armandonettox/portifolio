# Armando Netto { .pf-title-hidden }

<div class="pf-bio">
  <p><span id="pf-saudacao">Olá</span></p>
  <p>Sou Armando Netto — profissional de dados com atuação em análise, automação, IA aplicada e Machine Learning.</p>
  <p>Durante o dia, trabalho como Analista de Dados na Best Saúde, construindo análises, dashboards e fluxos automatizados no contexto de operadora de saúde. À noite e nos meus horários livres, desenvolvo produtos independentes e ferramentas que conectam dados e desenvolvimento de aplicações para resolver necessidades do meu dia a dia.</p>
</div>

<script>
(function () {
  var el = document.getElementById('pf-saudacao');
  if (!el) return;
  var hora = new Date().getHours();
  var periodo = hora < 12 ? 'bom dia' : hora < 18 ? 'boa tarde' : 'boa noite';
  el.textContent = 'Olá, ' + periodo;
})();
</script>
