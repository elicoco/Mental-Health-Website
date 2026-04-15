green = "#4CAF50";
red = "#F44336";
blue = "#2196F3";
orange ="#FFBF00";
let prompts = [];  // Declare an array to store the prompts
// Fetch the JSON data from the static folder
fetch('/static/JSON/prompts.json') 
    .then(response => response.json())
    .then(data => {
        prompts = data.prompts;  // Store the prompts in the array
    })
    .catch(error => {
        console.error("Error fetching prompts:", error);
    });

function cancelEdit() {
    var userConfirmed = confirm("Are you sure you want to cancel the changes made to this journal?");
    // checks if user wants to cancel the edit
        if (userConfirmed){
            window.location.reload();
        }
}
function saveJournal(){
    const journalData = {
        title: document.getElementById('journal-title').innerText,
        content: document.getElementById('journal-content').innerText
    };
    // gets the data from the HTML
    if (journalData.title == "Add Title" || journalData.content == "Add Content"){ 
        // input validation
        showSnackbar("Journal could not be saved: Title or Content is missing", orange)
        // shows snackbar if not saved
    }
    else{
        fetch(window.location.href, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(journalData)
        });
        showSnackbar("Journal Successfully Saved",green)
        // shows snackbar if successfully saved
    }
}
function deleteJournal(){
    var journalId = document.getElementById("journalId").value;
    // gets this from a hidden HTML input value
    var userConfirmed = confirm("Are you sure you want to delete this journal?");
// checks if user wants to delete the journal
    if (userConfirmed){
        window.location.href = '/delete_journal/'+ journalId;
    }
}
function prompt(){
    showSnackbar(getRandomPrompt(),blue, time=10)
}
function getRandomPrompt() {
    const randomIndex = Math.floor(Math.random() * prompts.length);
    return prompts[randomIndex];
}
