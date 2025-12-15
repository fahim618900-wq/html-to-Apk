function generate(){
  let url = document.getElementById("url").value;
  let app = document.getElementById("app").value;
  let pkg = document.getElementById("pkg").value;

  if(!url || !app || !pkg){
    document.getElementById("msg").innerText = "সব ফিল্ড পূরণ করুন";
    return;
  }

  document.getElementById("msg").innerText =
    "APK Project Generated (Backend লাগবে Build করার জন্য)";
}
