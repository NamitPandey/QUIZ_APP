function toggleSignup(){
   document.getElementById("login-toggle").style.backgroundColor="#fff";
    document.getElementById("login-toggle").style.color="#222";
    document.getElementById("signup-toggle").style.backgroundColor="#de9714";
    document.getElementById("signup-toggle").style.color="#fff";
    document.getElementById("login-form").style.display="none";
    document.getElementById("signup-form").style.display="block";
    document.getElementById("body").style.height="130vh";
}

function toggleLogin(){
    document.getElementById("login-toggle").style.backgroundColor="#de9714";
    document.getElementById("login-toggle").style.color="#fff";
    document.getElementById("signup-toggle").style.backgroundColor="#fff";
    document.getElementById("signup-toggle").style.color="#222";
    document.getElementById("signup-form").style.display="none";
    document.getElementById("login-form").style.display="block";
    document.getElementById("body").style.height="100vh";
}


function validateform2(){
    var v1= document.frm_signup.email.value;
    var v2= document.frm_signup.semester.value;
    
    str = v1.includes("gsfcuniversity");

    if(str == false){
        alert("Enter university mail-id !!!");
        document.frm_signup.email.focus();
        return false;
    }

    if(v2 < 1 || v2 > 8){
        alert("Semester cannot be lesser then 1 or it cannot be greater then 8");
        document.frm_signup.semester.focus();
        return false;
    }
}