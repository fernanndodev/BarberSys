function onChangeEmail() {
  toggleButtonDisabled();
  toggleEmailErrors();
}

function register() {
  window.location.href = "/register";
}

function cliente() {
  window.location.href = "/cliente";
}

function cadastroCliente() {
  window.location.href = "/cliente";
}

function incluir() {
  window.location.href = "/incluir";
}
function incluiCliente() {
  window.location.href = "/incluir";
}
function listarCliente() {
  window.location.href = "/listarCliente";
}

function voltar() {
  window.location.href = "/listarCliente";
}

function voltarCliente() {
  window.location.href = "/cliente";
}

function voltarHome() {
  window.location.href = "/voltarHome";
}

function barbeiro() {
  window.location.href = "/barbeiro";
}

function incluirB() {
  window.location.href = "/incluirB";
}

function listarBarbeiro() {
  window.location.href = "/listarBarbeiro";
}

function voltarB() {
  window.location.href = "/listarBarbeiro";
}


function voltarBarbeiro() {
  window.location.href = "/barbeiro";
}

function agendamento() {
  window.location.href = "/agendamento";
}


function incluiCliente_Agendamento() {
  window.location.href = "/agendamentoCliente";
}


function servico() {
  window.location.href = "/servico";
}

function meus_agendamentos() {
  window.location.href = "/meus_agendamentos"
}


function voltar_agendamento() {
  window.location.href = "/voltar_agendamento";
}





function onChangePassword() {
  toggleButtonDisabled();
  togglePasswordErrors();
}

// Verifica se email é vazio ou valida ele
function isEmailValid() {
  const email = document.getElementById("email").value;
  if (!email) {
    return false;
  }

  return validateEmail(email);
}
// Verifica se senha é vazio ou valida ele
function isPasswordValid() {
  const password = document.getElementById("password").value;
  if (!password) {
    return false;
  }
  return true;
}

// Expressao que valida email
function validateEmail(email) {
  return /\S+@\S+\.\S+/.test(email);
}

// Habilita ou desabilita mensagem de erro caso haja erro no email
function toggleEmailErrors() {
  const email = document.getElementById("email").value;

  if (!email) {
    document.getElementById("email-required-error").style.display = "block";
  } else {
    document.getElementById("email-required-error").style.display = "none";
  }

  if (validateEmail(email)) {
    document.getElementById("email-invalid-error").style.display = "none";
  } else {
    document.getElementById("email-invalid-error").style.display = "block";
  }
}

// Habilita ou desabilita mensagem de erro caso haja erro na senha
function togglePasswordErrors() {
  const password = document.getElementById("password").value;

  if (!password) {
    document.getElementById("password-required-error").style.display = "block";
  } else {
    document.getElementById("password-required-error").style.display = "none";
  }
}

// Desabilita botoes caso email for invalido
function toggleButtonDisabled() {
  const emailValid = isEmailValid();
  document.getElementById("recover-password-btn").disabled = !emailValid;

  const passwordValid = isPasswordValid();
  document.getElementById("login-button").disabled =
    !emailValid || !passwordValid;
}

document.addEventListener("DOMContentLoaded", () => {
    const botoes = document.querySelectorAll(".auto-send");
    const form = document.getElementById("form-servicos");
    const servicoHidden = document.getElementById("servico");

    botoes.forEach(botao => {
        botao.addEventListener("click", () => {
            const valor = botao.dataset.value;

            servicoHidden.value = valor;

            form.submit();
        });
    });
});

