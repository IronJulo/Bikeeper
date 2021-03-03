
function selectSub(elem){
    document.querySelector(".selected-sub input").checked = false;
    document.querySelector(".selected-sub").classList.remove("selected-sub")
    elem.parentNode.parentNode.parentNode.classList.add("selected-sub")
    document.querySelector(".selected-sub input").checked = true;
}

function selectSubscription(elem){
    document.querySelector(".selected-sub").classList.remove("selected-sub")
    elem.classList.add("selected-sub")
}

function checkRadio(elem){
    elem.children[0].checked = "true"
}