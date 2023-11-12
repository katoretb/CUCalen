async function fetcher(path, bd){
    const response = await fetch(host + `/${path}`, {
        method: 'POST',
        body: JSON.stringify(bd),
        headers: {
            'Content-Type': 'application/json'
        }
    });
    var data = await response.json();
    if(data["success"]){
        return[data["data"], data["message"], data["status_code"], false]
    }
    return[{}, data["message"], data["status_code"], true]
    
}

async function hash(string) {
    const utf8 = new TextEncoder().encode(string);
    const hashBuffer = await crypto.subtle.digest('SHA-256', utf8);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    const hashHex = hashArray
      .map((bytes) => bytes.toString(16).padStart(2, '0'))
      .join('');
    return hashHex;
  }

async function getsubj(sc){
    var [data, msg, stc, err] = await fetcher("get_subject", {secret_code: sc});
    if(err){
        Swal.fire({
            title: `Error ${stc}!`,
            text: `${msg}\nplease contact web owner`,
            icon: 'error'
        })
        return 1
    } 
    sessionStorage.setItem("subjects", JSON.stringify(data["subjects"]));
    return 0;
}

async function bsl(){
    var subjs = JSON.parse(sessionStorage.getItem("subjects"))
    var ct = ""
    for(let i=0; i<subjs.length; i++){
        ct += `<tr>\
            <th scope="row">${i+1}</th>\
            <td><input class="form-control" id="cn${i}" value="${subjs[i]['courseno']}" type="number" min="1"></td>\
            <td><input class="form-control" id="sm${i}" value="${subjs[i]['semester']}" type="number" min="1" max="3"></td>\
            <td><input class="form-control" id="st${i}" value="${subjs[i]['section']}" type="number" min="1"></td>\
            <td><button type="button" onclick="delsubj(${i})" class="btn btn-danger"><i class="bi bi-x-lg"></td>\
        </tr>`
    }
    document.getElementById("subjbody").innerHTML = ct;
    return 0;
}

function delsubj(n){
    var subjs = JSON.parse(sessionStorage.getItem("subjects"))
    subjs.splice(n, 1);
    sessionStorage.setItem("subjects", JSON.stringify(subjs));
    bsl()
    return 0;
}

function addsubj(){
    var subjs = JSON.parse(sessionStorage.getItem("subjects"))
    if(document.getElementById("cnadd").value == ""){
        Swal.fire({
            title: `Course ID is empty!`,
            text: `Please fill Course ID to course that you will add`,
            icon: 'error'
        })
        return 0;
    }
    if(document.getElementById("smadd").value == ""){
        Swal.fire({
            title: `Semester is empty!`,
            text: `Please fill semester to course that you will add`,
            icon: 'error'
        })
        return 0;
    }
    if(document.getElementById("stadd").value == ""){
        Swal.fire({
            title: `Section is empty!`,
            text: `Please fill section to course that you will add`,
            icon: 'error'
        })
        return 0;
    }
    subjs.push({
        courseno: document.getElementById("cnadd").value,
        section: document.getElementById("stadd").value,
        semester: document.getElementById("smadd").value,
        studyProgram: "S",
        year: 2566
    })
    sessionStorage.setItem("subjects", JSON.stringify(subjs));
    document.getElementById("cnadd").value = ""
    document.getElementById("stadd").value = ""
    document.getElementById("smadd").value = ""
    bsl()
    return 0;
}   

async function submitsubj(){
    x = []
    for(let i=0; i<document.getElementById("subjbody").children.length; i++){
        x.push({
            courseno: document.getElementById(`cn${i}`).value,
            section: document.getElementById(`st${i}`).value,
            semester: document.getElementById(`sm${i}`).value,
            studyProgram: "S",
            year: 2566
        })
    }

    var [data, msg, stc, err] = await fetcher("edit_subject", {
        sid: getCookie("sid"),
        token: getCookie("token"),
        subjects: x
    });

    if(err){
        Swal.fire({
            title: `Error ${stc}!`,
            text: `${msg}\nplease contact web owner`,
            icon: 'error'
        })
        return
    }
    sessionStorage.removeItem("subjects");
    Swal.fire({
        title: `Registed subject successfully`,
        icon: 'success'
    })
    return
}

async function login(){
    var hp = await hash(document.getElementById("pass1").value)
    var [data, msg, stc, err] = await fetcher("login", {
        sid: document.getElementById("sid1").value,
        password: hp
    });
    if(err){
        if(stc == 400){
            Swal.fire({
                title: msg,
                icon: 'error',
                confirmButtonText: 'OK'
            })
        }else{
            Swal.fire({
                title: "Please contact support",
                text: msg,
                icon: 'error',
                confirmButtonText: 'OK'
            })
        }
        return
    }

    Swal.fire({
        title: `Sign-in successfully`,
        icon: 'success',
        confirmButtonText: 'OK'
    }).then(() => {
        document.cookie = `sid=${data['sid']}`
        document.cookie = `token=${data['token']}`
        document.cookie = `secret_code=${data['secret_code']}`
        document.cookie = `firstname=${data['firstname']}`
        document.cookie = `lastname=${data['lastname']}`
        document.cookie = `username=${data['username']}`
        document.cookie = `working_hour=${JSON.stringify(data['working_hour'])}`
        setmenu("main")
        loadpage("home")
        return
    })
}

async function regis(){
    var fn = document.getElementById("fn").value
    var ln = document.getElementById("ln").value
    var un = document.getElementById("uname").value
    var sid = document.getElementById("sid2").value
    if(fn == "" || !/^[A-Za-z]*$/.test(fn)){
        Swal.fire({
            title: `Firstname invalid form!`,
            text: `Firstname must contain only english alphabet`,
            icon: 'error',
            confirmButtonText: 'OK'
        }).then(() => {
            document.getElementById("fn").focus()
        })
        return
    }

    if(ln == "" || !/^[A-Za-z]*$/.test(ln)){
        Swal.fire({
            title: `Lastname invalid form!`,
            text: `Lastname must contain only english alphabet`,
            icon: 'error',
            confirmButtonText: 'OK'
        }).then(() => {
            document.getElementById("ln").focus()
        })
        return
    }

    if(un == "" || !/^[A-Za-z0-9]*$/.test(un)){
        Swal.fire({
            title: `Username invalid form!`,
            text: `Username must contain only english alphabet and number`,
            icon: 'error',
            confirmButtonText: 'OK'
        }).then(() => {
            document.getElementById("un").focus()
        })
        return
    }

    if(sid.length != 10 || !/^[0-9]*$/.test(sid)){
        Swal.fire({
            title: `Student ID invalid form!`,
            text: `Student ID must contain only number and 10 characters`,
            icon: 'error',
            confirmButtonText: 'OK'
        }).then(() => {
            document.getElementById("sid2").focus()
        })
        return
    }

    if(!cpwrqm()){
        Swal.fire({
            title: `Password invalid form!`,
            text: `You must fix your password as describe first`,
            icon: 'error',
            confirmButtonText: 'OK'
        }).then(() => {
            document.getElementById("pass21").focus()
        })
        return
    }

    if(!ccpw()){
        Swal.fire({
            title: `Confirm password not match!`,
            text: `Please fix your confirm password`,
            icon: 'error',
            confirmButtonText: 'OK'
        }).then(() => {
            document.getElementById("pass22").focus()
        })
        return
    }

    var hp = await hash(document.getElementById("pass21").value)
    
    var [data, msg, stc, err] = await fetcher("register", {
        firstname: fn,
        lastname: ln,
        username: un,
        sid: sid,
        password: hp
    });

    if(err){
        if(stc == 400){
            Swal.fire({
                title: msg,
                icon: 'error',
                confirmButtonText: 'OK'
            })
        }else{
            Swal.fire({
                title: "Please contact support",
                text: msg,
                icon: 'error',
                confirmButtonText: 'OK'
            })
        }
        return
    }
    document.cookie = `sid=${sid}`
    document.cookie = `token=${data['token']}`
    Swal.fire({
        title: `Sign-up successfully`,
        icon: 'success',
        confirmButtonText: 'OK'
    }).then(() => {
        Swal.fire({
            title: `Recovery authentication`,
            text: `Use your authentication app scan this to use for recovery or change the password`,
            imageUrl: data['qr'],
            icon: 'warning',
            confirmButtonText: 'OK'
        });
    }).then( async () => {
        var [data, msg, stc, err] = await fetcher("get_user_data", {
            sid: getCookie("sid"),
            token: getCookie("token")
        });

        document.cookie = `secret_code=${data['secret_code']}`
        document.cookie = `firstname=${data['firstname']}`
        document.cookie = `lastname=${data['lastname']}`
        document.cookie = `username=${data['username']}`
        document.cookie = `working_hour=${JSON.stringify(data['working_hour'])}`
    }).then(() => {
        setmenu("main")
        loadpage("home")
        return
    })
}
