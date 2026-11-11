window.addEventListener("load", () => {
    let loader = document.querySelector(".loader");

    loader.classList.add("loader-hidden");

    loader.addEventListener("transitionend", () => {
        document.body.removeChild("loader")
    })
})

document.addEventListener("DOMContentLoaded", () => {

//Login Form Events
let loginBtn = document.getElementById("login-btn");
let loginMsg = document.getElementById("login-errmsg");

    if(loginBtn)
        if (loginMsg.innerHTML) {
            loginMsg.style.display = "block";
        } else {
            loginMsg.style.display = "none";
        }

//Dashboard Event
let albumCard = document.getElementsByClassName("album_card");
let albumBox = document.getElementsByClassName("album-box");

    for(let i = 0; i < albumCard.length; i++) {
        albumCard[i].addEventListener("click", ()=> {
            if((i % 2) != 0) {
                albumCard[i].classList.add("album_card-active-right");
            }
            else {
                albumCard[i].classList.add("album_card-active-left");
            }
        })
    }

    let colors_percent = [0.2126, 0.7152, 0.0722]
    for(let i = 0; i < albumCard.length; i++) {
        luma_numbers = albumCard[i].getAttribute("style").match(/\d+/g);
        let luma = 0;

        for(let j = 0; j < luma_numbers.length; j++) {
            luma += parseInt(luma_numbers[j]) * colors_percent[j];
        }

        if (luma < 80) {
            albumCard[i].style.color = "white";
        }
    }

})