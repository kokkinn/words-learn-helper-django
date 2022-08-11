function checker() {
    var result = confirm('Are you sure')
    if(result == false){
        event.preventDefault()
    }
}

function decodeHtml(html) {
    var txt = document.createElement("textarea");
    txt.innerHTML = html;
    return txt.value;
}

function stripHtml(html)
{
   let tmp = document.createElement("DIV");
   tmp.innerHTML = html;
   return tmp.textContent || tmp.innerText || "";
}
function notify(type,message){
  (()=>{
    console.log(message);
    message = decodeHtml(message);
    message = stripHtml(message);
    console.log(message);
    let n = document.createElement("div");
    let id = Math.random().toString(36).substr(2,10);
    n.setAttribute("id",id);
    n.classList.add("notification",type);
    n.innerText = message;
    document.getElementById("notification-area").appendChild(n);
    setTimeout(()=>{
      var notifications = document.getElementById("notification-area").getElementsByClassName("notification");
      for(let i=0;i<notifications.length;i++){
        if(notifications[i].getAttribute("id") == id){
          notifications[i].remove();
          break;
        }
      }
    },10000);
  })();
}

function notifySuccess(message){
    notify("success",message);

}
function notifyError(message){
  notify("error", message);
}
function notifyInfo(){
  notify("info","This is demo info notification message");
}
