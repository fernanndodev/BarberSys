function onChangeEmail() {
  toggleButtonDisabled()
  toggleEmailErrors()
  

}



function register() {
  window.location.href = "/register";
}

function onChangePassword() {
  toggleButtonDisabled()
  togglePasswordErrors()
}

// Verifica se email é vazio ou valida ele
function isEmailValid() {
  const email = document.getElementById("email").value;
  if (!email) {
    return false;
  }

  return validateEmail(email)

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
  const email = document.getElementById('email').value;

  if (!email) {
    document.getElementById('email-required-error').style.display="block";
  } else {
    document.getElementById('email-required-error').style.display = "none";
  }

  if (validateEmail(email)) {
    document.getElementById('email-invalid-error').style.display = "none";
  } else {
     document.getElementById('email-invalid-error').style.display = "block";
  }
}


// Habilita ou desabilita mensagem de erro caso haja erro na senha 
function togglePasswordErrors() {
  const password = document.getElementById('password').value;

  if (!password) {
    document.getElementById('password-required-error').style.display="block";
  } else {
    document.getElementById('password-required-error').style.display = "none";
  }

}

// Desabilita botoes caso email for invalido
function toggleButtonDisabled() {
  const emailValid = isEmailValid()
  document.getElementById("recover-password-btn").disabled = !emailValid;
  
  const passwordValid = isPasswordValid()
  document.getElementById('login-button').disabled = !emailValid || !passwordValid; 
  
}

