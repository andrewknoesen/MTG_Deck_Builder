document.getElementById("button-get_decks").addEventListener("click", ()=>{eel.get_decks()}, false);
document.getElementById("button-load-cards").addEventListener("click", ()=>{eel.get_random_number()}, false);
document.getElementById("button-date").addEventListener("click", ()=>{eel.get_date()}, false);
document.getElementById("button-ip").addEventListener("click", ()=>{eel.get_ip()}, false);

eel.expose(prompt_alerts);
function prompt_alerts(description) {
  alert(description);
}

eel.expose(get_decks_eel);
function get_decks_eel(decks){
  document.getElementById("output").textContent = JSON.stringify(decks, null, 2);
  // document.getElementById("output").textContent = "Test";
}

eel.expose(display_progress);
function display_progress(progress){
  document.getElementById("output").textContent = progress;
}