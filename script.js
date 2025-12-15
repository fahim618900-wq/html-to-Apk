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
  .then(res=>res.json())
  .then(data=>{
    if(data.download){
      window.location.href = "http://localhost:3000" + data.download;
    }else{
      alert(JSON.stringify(data));
    }
  });
}
