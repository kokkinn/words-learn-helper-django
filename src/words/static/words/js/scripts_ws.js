function checker() {
    var result = confirm('Are you sure ?')
    if(result == false){
        event.preventDefault()
    }

}

function stripHtml(html)
{
   let tmp = document.createElement("DIV");
   tmp.innerHTML = html;
   return tmp.textContent || tmp.innerText || "";
}

function notify(type,message) {
  message = stripHtml(message);
  let n = document.createElement("div");
  const id = Math.random().toString(36).slice(2);
  n.setAttribute("id", id);
  n.classList.add("notification", type);
  n.innerText = message;
  document.getElementById("notification-area").appendChild(n);

  setTimeout(() => {
    const toRemove = document.getElementById(id);
    toRemove.remove()
  },5000);
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

