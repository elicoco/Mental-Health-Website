green = "#4CAF50";
red = "#F44336";
blue = "#2196F3";
orange ="#FFBF00";

let prompts = [];
fetch(PROMPTS_URL)
    .then(response => response.json())
    .then(data => {
        prompts = data.prompts;
    })
    .catch(error => {
        console.error("Error fetching prompts:", error);
    });

const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

function cancelEdit() {
    var userConfirmed = confirm("Are you sure you want to cancel the changes made to this journal?");
    if (userConfirmed){
        window.location.reload();
    }
}

function saveJournal(silent = false){
    const journalData = {
        title: document.getElementById('journal-title').innerText,
        content: document.getElementById('journal-content').innerText
    };
    fetch(window.location.href, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify(journalData)
    })
    .then(response => {
        if (response.ok){
            if (!silent) showSnackbar("Journal Successfully Saved", green);
        } else {
            showSnackbar("Failed to save journal, please try again", red);
        }
    })
    .catch(() => showSnackbar("Failed to save journal, please try again", red));
}

let autoSaveTimer;
function triggerAutoSave() {
    clearTimeout(autoSaveTimer);
    autoSaveTimer = setTimeout(() => saveJournal(true), 1500);
}

document.addEventListener("DOMContentLoaded", () => {
    document.getElementById('journal-title').addEventListener('input', triggerAutoSave);
    document.getElementById('journal-content').addEventListener('input', triggerAutoSave);
});

function deleteJournal(){
    var journalId = document.getElementById("journal-id").value;
    var userConfirmed = confirm("Are you sure you want to delete this journal?");
    if (userConfirmed){
        window.location.href = '/delete_journal/' + journalId;
    }
}

function showPrompt(){
    if (prompts.length === 0){
        showSnackbar("Prompts are still loading, please try again", orange);
        return;
    }
    const randomIndex = Math.floor(Math.random() * prompts.length);
    showSnackbar(prompts[randomIndex], blue, 10);
}
