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
    var [data, msg, stc, err] = await fetcher("sha256", {str: string});
    return data['hash'];
  }

async function getsubj(sc){
    var [data, msg, stc, err] = await fetcher("get_subject", {secret_code: sc});
    if(err){
        Swal.fire({
            title: `Error ${stc}!`,
            text: `${msg}\nPlease contact web administrator`,
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
            <td><input class="form-control" id="cn${i}" placeholder="Course ID" type="number" value="${subjs[i]['courseno']}" min="1"></td>\
            <td><input class="form-control" id="sm${i}" placeholder="Semester" type="number" value="${subjs[i]['semester']}" min="1" max="3"></td>\
            <td><input class="form-control" id="st${i}" placeholder="Section" type="number" value="${subjs[i]['section']}" min="1"></td>\
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
    const cn = document.getElementById("cnadd").value
    if(cn == "" || cn.length != 7){
        Swal.fire({
            title: `Course ID is invalid/unspecified!`,
            text: `Please fill Course ID correctly`,
            icon: 'error'
        })
        return 0;
    }
    if(document.getElementById("smadd").value == ""){
        Swal.fire({
            title: `Semester is unspecified!`,
            text: `Please fill semester to added courses`,
            icon: 'error'
        })
        return 0;
    }
    if(document.getElementById("stadd").value == ""){
        Swal.fire({
            title: `Section is unspecified!`,
            text: `Please fill section to added courses`,
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

    Swal.fire({
        title: 'Processing ...',
        showConfirmButton: false,
        allowEscapeKey: false,
        allowOutsideClick: false,
        imageUrl: "https://i.giphy.com/media/IwSG1QKOwDjQk/giphy.webp"
    })

    var [data, msg, stc, err] = await fetcher("edit_subject", {
        sid: getCookie("sid"),
        token: getCookie("token"),
        subjects: x
    });

    Swal.close()

    if(err){
        Swal.fire({
            title: `Error ${stc}!`,
            text: `${msg}\nPlease contact web administrator`,
            icon: 'error'
        })
        return
    }
    // sessionStorage.removeItem("subjects");
    Swal.fire({
        title: `Subjects added`,
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
        title: `Signed in`,
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
            title: `Firstname is in an invalid form!`,
            text: `Only English letters are allowed`,
            icon: 'error',
            confirmButtonText: 'OK'
        }).then(() => {
            document.getElementById("fn").focus()
        })
        return
    }

    if(ln == "" || !/^[A-Za-z]*$/.test(ln)){
        Swal.fire({
            title: `Lastname is in an invalid form!`,
            text: `Only English letters are allowed`,
            icon: 'error',
            confirmButtonText: 'OK'
        }).then(() => {
            document.getElementById("ln").focus()
        })
        return
    }

    if(un == "" || !/^[A-Za-z0-9]*$/.test(un)){
        Swal.fire({
            title: `Username is in an invalid form!`,
            text: `Only English letters and numbers are allowed`,
            icon: 'error',
            confirmButtonText: 'OK'
        }).then(() => {
            document.getElementById("un").focus()
        })
        return
    }

    if(sid.length != 10 || !/^[0-9]*$/.test(sid)){
        Swal.fire({
            title: `Student ID is in an invalid form!`,
            text: `Student ID must be 10 digits`,
            icon: 'error',
            confirmButtonText: 'OK'
        }).then(() => {
            document.getElementById("sid2").focus()
        })
        return
    }

    if(!cpwrqm()){
        Swal.fire({
            title: `Password is in an invalid form!`,
            text: `Please refer to the criteria above`,
            icon: 'error',
            confirmButtonText: 'OK'
        }).then(() => {
            document.getElementById("pass21").focus()
        })
        return
    }

    if(!ccpw()){
        Swal.fire({
            title: `Passwords do not match!`,
            text: `Please try again`,
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
        title: `Signed up`,
        icon: 'success',
        confirmButtonText: 'OK'
    }).then(() => {
        Swal.fire({
            title: `Recovery code`,
            text: `Please scan the QR code using the authenticator app on your smartphone in case of losing a password`,
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

async function gtt_submit_subj(){
    var raw_freetime = JSON.parse(sessionStorage.gtt_freetime)
    var freetime2 = [
        1,
        {
            "LECT": [],
            "LAB": []
        }
    ]
    var subjl = JSON.parse(sessionStorage.gtt_subjects)
    if(subjl.length < 1){
        Swal.fire({
            title: `Subject list is empty!`,
            text: `Specify at least one subject`,
            icon: 'error',
            confirmButtonText: 'OK'
        })
        return
    }

    Object.keys(raw_freetime).forEach((item, index) => {
        raw_freetime[item].forEach((item2, index2) => {
            freetime2[1]["LECT"].push(
                {
                    "day": [index+1], 
                    "time": [`${item2+8}:00:00`, `${item2+9}:00:00`]
                }
            )
        })
    })

    var [data, msg, stc, err] = await fetcher("gtt", {
        subj_list: subjl,
        st_time: 8,
        ed_time: 18,
        freetime: freetime2
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

    sessionStorage.setItem('gttnum', '1')
    sessionStorage.setItem('gttposs', JSON.stringify(data['possible']))
    sessionStorage.setItem('gttdata', JSON.stringify(data['dataset']))
    document.getElementById("gttmin").innerHTML = sessionStorage.getItem('gttnum')
    document.getElementById("gttmax").innerHTML = data['possible'].length
    gtt_show_tt()
    return
}
