document.getElementById("button-get_decks").addEventListener("click", ()=>{eel.get_decks()}, false);
document.getElementById("button-number").addEventListener("click", ()=>{eel.get_random_number()}, false);
document.getElementById("button-date").addEventListener("click", ()=>{eel.get_date()}, false);
document.getElementById("button-ip").addEventListener("click", ()=>{eel.get_ip()}, false);

eel.expose(prompt_alerts);
function prompt_alerts(description) {
  alert(description);
}

eel.expose(display_output);
function display_output(decks){
  document.getElementById("output").textContent = JSON.stringify(decks, null, 2);
}