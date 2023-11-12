const host = "http://kato14123.ddns.net:5001";
// const host = "http://127.0.0.1:5000";
//===========================
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

function clearcookie(){
    var Cookies = document.cookie.split(';');

    for (var i = 0; i < Cookies.length; i++){
        if(Cookies[i] != "allowcookie"){
            document.cookie = Cookies[i] + "=;expires=" + new Date(0).toUTCString();
        }
    }
    return
}

function logout(){
    clearcookie()
    setmenu("login")
    setpage()
    Swal.fire({
        title: `Logout successfully`,
        icon: 'success'
    })
    return
}

//===========================
async function setpage(){
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    if(!urlParams.has('page')){
        window.history.replaceState(null, null, "?page=home");
        await loadDoc('home');
        return;
    }
    var x = urlParams.get('page')
    await loadDoc(x);
    let mm = document.getElementById("mainmenu").children
    for(let i = 0; i < mm.length; i++){
        mm[i].children[0].classList.remove("active")
    }
    
    if(x != "empty"){
        document.getElementById(x).classList.add("active");
    }
    return
}

//
async function loadpage(page){
    window.history.replaceState(null, null, `?page=${page}`)
    await setpage()
    switch (page) {
        case "subject":
            await getsubj(getCookie("secret_code"))
            bsl()
            break
        case "profile":
            loadprofile()
    }
    
    return;
}

function loadprofile(){
    document.getElementById("profileun").innerHTML = getCookie("username")
    document.getElementById("profilesid").innerHTML = getCookie("sid")
    document.getElementById("profilefn").innerHTML = getCookie("firstname")
    document.getElementById("profileln").innerHTML = getCookie("lastname")
}

//===========================
// async function testfetcher(){
//     const response = await fetch(`/pages/profile.html`);
//     var data = await response.text();
//     console.log(data)
// }

async function loadDoc(name) {
    const response = await fetch(`/pages/${name}.html`);
    var data = await response.text();
    document.querySelector(".content").innerHTML = data
    return
}

// async function loadDoc(name) {
//     const xhttp = new XMLHttpRequest();
//     xhttp.onload = function() {
//         document.querySelector(".content").innerHTML =
//         this.responseText;
//     }
//     console.log(await xhttp.open("GET", "pages/" + name + ".html"));
//     await xhttp.send();
//     return;
// }
//===========================
function setmenu(mn="login"){
    if(mn != "main"){
        window.history.replaceState(null, null, `?page=empty&menu=${mn}`)
    }
    loadmenu(mn)
}

function loadmenu(visible){
    document.getElementById("lobut").style.display = 'none';
    document.getElementById("mainmenu").style.display = 'none';
    document.getElementById("regis").style.display = 'none';
    document.getElementById("login").style.display = 'none';
    document.getElementById("regbut").style.display = 'none';
    document.getElementById("libut").style.display = 'none';
    if(visible == "main"){
        document.getElementById("mainmenu").style.display = 'block';
        document.getElementById("lobut").style.display = 'block';
    }else if(visible == "login"){
        document.getElementById("login").style.display = 'block';
        document.getElementById('libut').style.display = 'block';
    }else{
        document.getElementById('regis').style.display = 'block';
        document.getElementById('regbut').style.display = 'block';
    }
}

function showpass(pi, vb){
    var x = document.getElementById(pi);
    if (x.type === "password") {
        x.type = "text";
    } else {
        x.type = "password";
    }
    var y = document.getElementById(vb);
    if (x.type === "password") {
        y.innerHTML = `<i class="bi bi-eye-slash"></i>`
    } else {
        y.innerHTML = `<i class="bi bi-eye"></i>`
    }
}

function cpwrqm(){
    var x = document.getElementById("pass21").value
    var l = cn = uc = lc = cr = ""
    var re = 0
    if(x.length >= 8){
        var l = " style='color:#31f537;'"
        re++;
    }
    if(/(?=.*[0-9])/.test(x)){
        var cn = " style='color:#31f537;'"
        re++;
    }
    if(/(?=.*[a-z])/.test(x)){
        var lc = " style='color:#31f537;'"
        re++;
    }
    if(/(?=.*[A-Z])/.test(x)){
        var uc = " style='color:#31f537;'"
        re++;
    }
    if(!/[^A-Za-z0-9]+/.test(x)){
        var cr = " style='color:#31f537;'"
        re++;
    }
    var y = [
        `<li${l}>At least 8 characters</li>`,
        `<li${cn}>At least 1 number</li>`,
        `<li${uc}>At least 1 uppercase</li>`,
        `<li${lc}>At least 1 lowercase</li>`,
        `<li${cr}>No special characters</li>`
    ]
    if(re == 5){
        document.getElementById("cpwrqm").innerHTML = ""
        return true
    }else{
        document.getElementById("cpwrqm").innerHTML = y.join("")
        return false
    }
}

function ccpw(){
    var x = document.getElementById("pass21").value
    var y = document.getElementById("pass22").value
    if(x == y){
        document.getElementById("ccpw").innerHTML = ""
        return true
    }else{
        document.getElementById("ccpw").innerHTML = "<a style='color: #575757'>Password not match</a>"
        return false
    }
}

function askcookie(){
    if(getCookie("allowcookie") == ''){
        Swal.fire({
            title: "Do you allow us to use cookie to store necessary data?",
            showDenyButton: true,
            icon: "warning",
            confirmButtonText: "Allow",
            denyButtonText: `Not allow`
        }).then((result) => {
            if (result.isConfirmed) {
                document.cookie = "allowcookie=1"
            } else if (result.isDenied) {
                location.href = "https://youtu.be/dQw4w9WgXcQ";
            }
        });
    }
    return
}