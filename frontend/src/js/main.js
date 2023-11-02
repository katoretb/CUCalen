function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for(let i = 0; i <ca.length; i++) {
      let c = ca[i];
      while (c.charAt(0) == ' ') {
        c = c.substring(1);
      }
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
      }
    }
    return "";
}
//===========================
async function setpage(){
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    if(!urlParams.has('page')){
        loadDoc('home');
        return 0;
    }
    await loadDoc(urlParams.get('page'));
    let mm = document.getElementById("mainmenu").children
    for(let i = 0; i < mm.length; i++){
      mm[i].children[0].classList.remove("active")
    }
    document.getElementById(urlParams.get('page')).classList.add("active");
    return 0;
}
//===========================
async function loadDoc(name) {
    const xhttp = new XMLHttpRequest();
    xhttp.onload = function() {
        document.querySelector(".content").innerHTML =
        this.responseText;
    }
    xhttp.open("GET", "pages/" + name + ".html");
    xhttp.send();
    return 0;
}
//===========================