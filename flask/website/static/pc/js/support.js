function active(tab) {
    try{
        active = document.querySelector("ul.nav > li > a.active");
        active.classList.replace("active","inactive");
    }
    catch {

    }
    tab.classList.replace("inactive","active");
    return true;
}

api = "http://127.0.0.1:5000/test/message/1/all"

function get(url) {
  return new Promise((resolve, reject) => {
    const req = new XMLHttpRequest();
    req.open('GET', url);
    req.onload = () => req.status === 200 ? resolve(req.response) : reject(Error(req.statusText));
    req.onerror = (e) => reject(Error(`Network Error: ${e}`));
    req.send();
  });
}
get(api).then((data) => console.log(data))