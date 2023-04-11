function verifyPassword(){
    var pw = document.getElementById("pswd").value;
    var pw2 = document.getElementById("pswd2").value;

if(pw.length < 8 || pw2.length<8) {
    document.getElementById("message").innerHTML = "password must be at least 8 characters";
    document.getElementById("message2").innerHTML = "password must be at least 8 characters";
    document.getElementById("errorimg1").style.display="block";
    document.getElementById("errorimg2").style.display="block";
    return false;
 }


 if(pw.length > 15) {
    document.getElementById("message").innerHTML = "password length not be more than  15 characters";
    document.getElementById("message2").innerHTML = "password must not be more than 15 characters";
    document.getElementById("errorimg1").style.display="block";
    document.getElementById("errorimg2").style.display="block";
    return false;
 } 
 
}



function offenderslist(){
    document.getElementById("offenderslist").src="../Add Offence/offendericon2.png"
    document.getElementById("addoffence").src="../Add Offence/addoffence1.png"
    document.getElementById("offenderfont").style.color="rgba(185, 124, 33, 1)"
    document.getElementById("addoffencefont").style.color="white"
    document.getElementById("reportfont").style.color="white"
    document.getElementById("report").src="../Add Offence/report2.png"
    document.getElementById("sus").src="../Add Offence/suspension1.png"
    document.getElementById("exp").src="../Add Offence/expulsion1.png"
    document.getElementById("susfont").style.color="white"
    document.getElementById("expfont").style.color="white"
}
function addoffence(){
    document.getElementById("offenderslist").src="../Add Offence/offendericon1.png"
    document.getElementById("addoffence").src="../Add Offence/addoffence2.png"
    document.getElementById("addoffencefont").style.color="rgba(185, 124, 33, 1)"
    document.getElementById("offenderfont").style.color="white"
    document.getElementById("reportfont").style.color="white"
    document.getElementById("report").src="../Add Offence/report2.png"
    document.getElementById("sus").src="../Add Offence/suspension1.png"
    document.getElementById("exp").src="../Add Offence/expulsion1.png"
    document.getElementById("susfont").style.color="white"
    document.getElementById("expfont").style.color="white"
}

function report(){
    document.getElementById("offenderslist").src="../Add Offence/offendericon1.png"
    document.getElementById("addoffence").src="../Add Offence/addoffence1.png"
    document.getElementById("addoffencefont").style.color="white"
    document.getElementById("offenderfont").style.color="white"
    document.getElementById("reportfont").style.color="rgba(185, 124, 33, 1)"
    document.getElementById("report").src="../Add Offence/report.png"
    document.getElementById("sus").src="../Add Offence/suspension1.png"
    document.getElementById("exp").src="../Add Offence/expulsion1.png"
    document.getElementById("susfont").style.color="white"
    document.getElementById("expfont").style.color="white"
}
function sus(){
    document.getElementById("offenderslist").src="../Add Offence/offendericon1.png"
    document.getElementById("addoffence").src="../Add Offence/addoffence1.png"
    document.getElementById("addoffencefont").style.color="white"
    document.getElementById("offenderfont").style.color="white"
    document.getElementById("reportfont").style.color="white"
    document.getElementById("report").src="../Add Offence/report2.png"
    document.getElementById("sus").src="../Add Offence/suspension2.png"
    document.getElementById("exp").src="../Add Offence/expulsion1.png"
    document.getElementById("susfont").style.color="rgba(185, 124, 33, 1)"
    document.getElementById("expfont").style.color="white"
}
function exp(){
    document.getElementById("offenderslist").src="../Add Offence/offendericon1.png"
    document.getElementById("addoffence").src="../Add Offence/addoffence1.png"
    document.getElementById("addoffencefont").style.color="white"
    document.getElementById("offenderfont").style.color="white"
    document.getElementById("reportfont").style.color="white"
    document.getElementById("report").src="../Add Offence/report2.png"
    document.getElementById("sus").src="../Add Offence/suspension1.png"
    document.getElementById("exp").src="../Add Offence/expulsion2.png"
    document.getElementById("susfont").style.color="white"
    document.getElementById("expfont").style.color="rgba(185, 124, 33, 1)"
}

    window.onloadstart(document.getElementById("addoffence").src="../Add Offence/addoffence2.png",
    document.getElementById("addoffencefont").style.color="rgba(185, 124, 33, 1)")

