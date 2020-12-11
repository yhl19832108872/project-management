document.querySelector('.img__btn').addEventListener('click', function() {
    document.querySelector('.content').classList.toggle('s--signup')
})

function register(){
    var name =document.getElementsByName('username')[0];
    var password=document.getElementsByName('password')[0];
    if(name.value.length<5||name.value.length>20){
        alert('The length of username must between 5 and 10!');
    }
    if(password.value.length<6||password.value.length>16){
        alert('The length of password must between 6 and 16!');
    }
            
}