function generate(){
  let url = document.getElementById("url").value;
  let app = document.getElementById("app").value;
  let pkg = document.getElementById("pkg").value;

  if(!url || !app || !pkg){
    alert("সব ফিল্ড পূরণ করুন");
    return;
  }

  fetch("http://localhost:3000/build",{
    method:"POST",
    headers:{ "Content-Type":"application/json" },
    body: JSON.stringify({url:url, appName:app, packageName:pkg})
  })
  .then(res => res.json())
  .then(data => {
    if(data.download){
      window.location.href = "http://localhost:3000"+data.download;
    }else{
      alert(JSON.stringify(data));
    }
  })
  .catch(err => alert("Backend চলছে না"));
}
