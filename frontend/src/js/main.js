// const host = "http://kato14123.ddns.net:5001";
const host = "http://127.0.0.1:5001";
const date = new Date()
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
        setframe()
        return;
    }
    var x = urlParams.get('page')
    await loadDoc(x);
    if(x == "home"){
        setframe()
    }
    let mm = document.getElementById("mainmenu").children
    for(let i = 0; i < mm.length; i++){
        mm[i].children[0].classList.remove("active")
    }
    
    if(x != "empty"){
        document.getElementById(x).classList.add("active");
    }
    return
}

function setframe(){
    document.getElementById('monthgrid_link').setAttribute('onclick', `navigator.clipboard.writeText('${window.location.origin}/calendar.html?type=month&sc=${getCookie("secret_code")}')`)
    document.getElementById('monthgrid_show').src = `../calendar.html?type=month&sc=${getCookie("secret_code")}`
    document.getElementById('daygrid_link').setAttribute('onclick', `navigator.clipboard.writeText('${window.location.origin}/calendar.html?type=day&sc=${getCookie("secret_code")}')`)
    document.getElementById('daygrid_show').src = `../calendar.html?type=day&sc=${getCookie("secret_code")}`
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
            break
        case "schgen":
            gtt_disabler_gen()
            break
        case "home":
            setframe()
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
    if(name == "empty"){
        document.querySelector(".content").innerHTML = ""
        return
    }
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

function gtt_disabler_gen(){
    document.getElementById("gtt_yradd").value = (date.getFullYear()+543).toString()
    gtt_subj_gen()
    a = {}
    x = ""
    y = ["MON", "TUE", "WED", "THU", "FRI"]
    for(let i=0;i<5;i++){
        x += `<div class="row" style="height:50px;"><div class="col gtt-nav">${y[i]}</div>`
        a[i.toString()] = [4]
        for(let j=0;j<10;j++){
            z = "#FFF"
            if(j == 4){
                z = "rgb(222, 222, 222)"
            }
            x += `<div class="col gtt-ele" style="background-color: ${z};" id="gtt-ft-${i}${j}" onclick="togglett('gtt-ft-${i}${j}')"></div>`
        }
        x += `</div>`
    }
    document.getElementById('gttft').innerHTML += x
    sessionStorage.setItem("gtt_freetime", JSON.stringify(a))
}

function togglett(id){
    var x = JSON.parse(sessionStorage.getItem("gtt_freetime"))
    var [r, c] = id.split("-")[2].split("")
    c = parseInt(c)
    if(document.getElementById(id).style.backgroundColor == "rgb(222, 222, 222)"){
        document.getElementById(id).style.backgroundColor = "#FFF"
        const index = x[r].indexOf(c);
        if (index > -1) {
            x[r].splice(index, 1);
        }
        sessionStorage.setItem("gtt_freetime", JSON.stringify(x))
        return
    }
    x[r].push(c)
    document.getElementById(id).style.backgroundColor = "rgb(222, 222, 222)"
    sessionStorage.setItem("gtt_freetime", JSON.stringify(x))
    return
}

async function gtt_subj_gen(){
    if (JSON.parse(sessionStorage.getItem("gtt_subjects")) == null){
        sessionStorage.setItem("gtt_subjects", JSON.stringify([]))
        return
    }
    var subjs = JSON.parse(sessionStorage.getItem("gtt_subjects"))
    var ct = ""
    for(let i=0; i<subjs.length; i++){
        var sbj = subjs[i].split("-")
        ct += `<tr>\
            <th scope="row">${i+1}</th>\
            <td>${sbj[0]}</td>\
            <td>${sbj[1]}</td>\
            <td>${sbj[2]}</td>\
            <td><button type="button" onclick="gtt_del_subj(${i})" class="btn btn-danger"><i class="bi bi-x-lg"></td>\
        </tr>`
    }
    document.getElementById("gtt_subjbody").innerHTML = ct;
    return;
}

function gtt_del_subj(n){
    var subjs = JSON.parse(sessionStorage.getItem("gtt_subjects"))
    subjs.splice(n, 1);
    sessionStorage.setItem("gtt_subjects", JSON.stringify(subjs));
    gtt_subj_gen()
    return;
}

function gtt_add_subj(){
    var subjs = JSON.parse(sessionStorage.getItem("gtt_subjects"))
    const cn = document.getElementById("gtt_cnadd").value
    const yr = document.getElementById("gtt_yradd").value
    const sm = document.getElementById("gtt_smadd").value
    if(cn == "" || cn.length != 7){
        Swal.fire({
            title: `Course ID is empty or invalid!`,
            text: `Please fill Course ID correctly`,
            icon: 'error'
        })
        return 0;
    }
    if(yr == ""){
        Swal.fire({
            title: `Year is empty!`,
            text: `Please fill Year correctly`,
            icon: 'error'
        })
        return 0;
    }
    if(sm == ""){
        Swal.fire({
            title: `Semester is empty!`,
            text: `Please fill Semester correctly`,
            icon: 'error'
        })
        return 0;
    }
    subjs.push(`${cn}-${yr}-${sm}`)
    sessionStorage.setItem("gtt_subjects", JSON.stringify(subjs));
    document.getElementById("gtt_cnadd").value = ""
    document.getElementById("gtt_smadd").value = ""
    gtt_subj_gen()
    return 0;
}   

function gtt_change_page(pagenum){
    if(parseInt(sessionStorage.getItem('gttnum')) + pagenum < 1) return;
    if(parseInt(sessionStorage.getItem('gttnum')) + pagenum > parseInt(document.getElementById("gttmax").innerHTML)) return;
    sessionStorage.setItem('gttnum', String(parseInt(sessionStorage.getItem('gttnum')) + pagenum))
    document.getElementById("gttmin").innerHTML = sessionStorage.getItem('gttnum')
    gtt_show_tt()
    return
}

function getColor(str, opts){
    var h, s, l;
    opts = opts || {};
    opts.hue = opts.hue || [0, 360];
    opts.sat = opts.sat || [75, 100];
    opts.lit = opts.lit || [40, 60];

    var range = function(hash, min, max) {
        var diff = max - min;
        var x = ((hash % diff) + diff) % diff;
        return x + min;
    }

    var hash = 0;
    if (str.length === 0) return hash;
    for (var i = 0; i < str.length; i++) {
        hash = str.charCodeAt(i) + ((hash << 5) - hash);
        hash = hash & hash;
    }

    h = range(hash, opts.hue[0], opts.hue[1]);
    s = range(hash, opts.sat[0], opts.sat[1]);
    l = range(hash, opts.lit[0], opts.lit[1]);

    return `hsl(${h}, ${25 + 70 * (s/100)}%, ${85 + 10 * (l/100)}%)`;
}

async function check_gtt(num, lis){
    var ret = []
    lis.forEach(element => {
        if(num == element[2]){
            ret = element
        }
    })
    return ret
}

async function gtt_show_tt(){
    var page = parseInt(sessionStorage.getItem('gttnum'))-1
    var possible = JSON.parse(sessionStorage.getItem('gttposs'))
    var dataset = JSON.parse(sessionStorage.getItem('gttdata'))
    // var day = {
    //     0: [
    //         [
    //             "name building room <br> section",
    //             color,
    //             position,
    //             num

    var day = {
        0: [],
        1: [],
        2: [],
        3: [],
        4: []
    }

    possible[page].forEach(element => {
        var cn = dataset[element[0]]["subject_name"].replace("GENERAL", 'GEN').replace("BIOLOGY", 'BIO').replace("PROGRAMMING", 'PROG').replace("CALCULUS", 'CAL').replace(" LAB", '')
        dataset[element[0]]["class"][element[1]]["LECT"].forEach(element2 => {
            var room = element2["Room"]
            var building = element2["building"]
            var start = parseInt(element2["time"][0].split(":")[0])-8
            var amount = parseInt(element2["time"][1].split(":")[0])-8-start
            element2["day"].forEach(element3 => {
                day[element3-1].push(
                    [
                        `LECT ${cn} ${building} ${room} Section: ${element[1]}`,
                        getColor(cn),
                        start,
                        amount
                    ]
                )
            })

        })

        dataset[element[0]]["class"][element[1]]["LAB"].forEach(element2 => {
            var room = element2["Room"]
            var building = element2["building"]
            var start = parseInt(element2["time"][0].split(":")[0])-8
            var amount = parseInt(element2["time"][1].split(":")[0])-8-start
            element2["day"].forEach(element3 => {
                day[element3-1].push(
                    [
                        `LAB ${cn} ${building} ${room} Section: ${element[1]}`,
                        getColor(cn),
                        start,
                        amount
                    ]
                )
            })

        })
    });

    y = ["MON", "TUE", "WED", "THU", "FRI"]
    var x = `<div class="row">
                <div class="col-2 gtt-nav">
                    Day/Time
                </div>
                <div class="col-1 gtt-nav">
                    8-9
                </div>
                <div class="col-1 gtt-nav">
                    9-10
                </div>
                <div class="col-1 gtt-nav">
                    10-11
                </div>
                <div class="col-1 gtt-nav">
                    11-12
                </div>
                <div class="col-1 gtt-nav">
                    12-13
                </div>
                <div class="col-1 gtt-nav">
                    13-14
                </div>
                <div class="col-1 gtt-nav">
                    14-15
                </div>
                <div class="col-1 gtt-nav">
                    15-16
                </div>
                <div class="col-1 gtt-nav">
                    16-17
                </div>
                <div class="col-1 gtt-nav">
                    17-18
                </div>
            </div>`
    for(let i=0;i<5;i++){
        x += `<div class="row" style="height:50px;"><div class="col gtt-nav">${y[i]}</div>`
        for(let j=0;j<10;j++){
            var z = "#FFF"
            var size = 1
            var cname = ""
            var data = await check_gtt(j, day[i])
            if(data.length != 0){
                size = data[3]
                z = data[1]
                cname = data[0]
            }
            j += size-1
            x += `<div class="col-${size} gtt-ele" style="background-color: ${z};font-size: 50%;">${cname}</div>`
        }
        x += `</div>`
    }
    document.getElementById("gttgen").innerHTML = x
    return
}