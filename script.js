function generate(){
  fetch("http://localhost:3000/build",{
    method:"POST",
    headers:{ "Content-Type":"application/json" },
    body:JSON.stringify({
      url: document.getElementById("url").value,
      appName: document.getElementById("app").value,
      packageName: document.getElementById("pkg").value
    })
  })
  .then(res => res.json())
  .then(data => alert(JSON.stringify(data)))
  .catch(err => alert("Backend not running"));
}
