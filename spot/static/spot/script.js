document.addEventListener("DOMContentLoaded", () => {

//Login Form Events
let loginBtn = document.getElementById("login-btn");
let loginMsg = document.getElementById("login-errmsg");

    if (loginMsg.innerHTML) {
        loginMsg.style.display = "block";
    } else {
        loginMsg.style.display = "none";
    }

})