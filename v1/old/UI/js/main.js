document.getElementById("button-get_decks").addEventListener("click", ()=>{eel.get_decks()}, false);
document.getElementById("button-load-cards").addEventListener("click", ()=>{eel.import_cards()}, false);
document.getElementById("button-date").addEventListener("click", ()=>{eel.get_date()}, false);
document.getElementById("button-ip").addEventListener("click", ()=>{eel.get_ip()}, false);

eel.expose(prompt_alerts);
function prompt_alerts(description) {
  alert(description);
}

eel.expose(show_decks_eel);
function show_decks_eel(decks){
  document.getElementById("output").textContent = JSON.stringify(JSON.parse(decks), null, 2);
  // document.getElementById("output").textContent = decks;
}

eel.expose(display_progress);
function display_progress(progress){
  document.getElementById("output").textContent = progress;
}

eel.expose(import_cards_eel);
function import_cards_eel(path_csv){
  document.getElementById("output").textContent = path_csv;
  // document.getElementById("output").textContent = "Test";
}