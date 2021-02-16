
let buttons_sidebar = document.querySelectorAll("#devices > form > button");
let username_sidebar = document.querySelector("#img-profile + span").textContent;

$.ajax({
    url: "/api/current_device/"+username_sidebar,
    success: function (result) {
        currentDevice = result.response;
        for (let elem of buttons_sidebar){
            if (elem.value == currentDevice){
                elem.style.color = "red";
            }
        }
    },
    error: function (err) {
        console.log("Error")
        console.log(err)
    }
});



