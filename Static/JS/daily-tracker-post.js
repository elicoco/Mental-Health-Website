green = "#4CAF50";
red = "#F44336";
blue = "#2196F3";
orange ="#FFBF00";

const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

showSleepHours();

function cancelEdit() {
    var userConfirmed = confirm("Are you sure you want to cancel the changes made to this daily tracker?");
    if (userConfirmed){
        window.location.reload();
    }
}

function getWakeupTime(){
    const [h, m] = document.getElementById('wakeup-input').value.split(':').map(Number);
    return h + m / 60;
}

function getBedTime(){
    const [h, m] = document.getElementById('bedtime-input').value.split(':').map(Number);
    return h + m / 60;
}

function saveDailyTracker(silent = false){
    showSleepHours();
    const dailyTrackerData = {
        comment: document.getElementById('daily-tracker-comment').innerText,
        mood_score: parseInt(document.getElementById('mood-display').innerText),
        wakeup_time: getWakeupTime(),
        bed_time: getBedTime(),
        exercise_mins: document.getElementById('exercise-mins-input').value || 0,
        productive_mins: document.getElementById('productive-mins-input').value || 0,
        meditation_mins: document.getElementById('meditation-mins-input').value || 0
    };
    fetch(window.location.href, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify(dailyTrackerData)
    })
    .then(response => {
        if (response.ok){
            if (!silent) showSnackbar("Daily Tracker Successfully Saved", green);
        } else {
            showSnackbar("Failed to save, please try again", red);
        }
    })
    .catch(() => showSnackbar("Failed to save, please try again", red));
}

let autoSaveTimer;
function triggerAutoSave() {
    clearTimeout(autoSaveTimer);
    autoSaveTimer = setTimeout(() => saveDailyTracker(true), 1500);
}

function deleteDailyTracker(){
    const dailyTrackerId = document.getElementById("daily-tracker-id").value;
    var userConfirmed = confirm("Are you sure you want to delete this daily tracker?");
    if (userConfirmed){
        window.location.href = '/delete_daily_tracker/' + dailyTrackerId;
    }
}

function updateMoodDisplay(value) {
    document.getElementById("mood-display").textContent = value;
}

function calculateSleepHours(){
    let hours = getWakeupTime() - getBedTime();
    if (hours < 0){ hours = hours + 24; }
    return hours;
}

function showSleepHours(){
    document.getElementById('sleep-hours').innerText = 'You slept for ' + calculateSleepHours().toFixed(1) + ' hours';
}

document.addEventListener("DOMContentLoaded", () => {
    document.getElementById('daily-tracker-comment').addEventListener('input', triggerAutoSave);
    document.getElementById('mood-slider').addEventListener('input', triggerAutoSave);
    document.getElementById('exercise-mins-input').addEventListener('input', triggerAutoSave);
    document.getElementById('productive-mins-input').addEventListener('input', triggerAutoSave);
    document.getElementById('meditation-mins-input').addEventListener('input', triggerAutoSave);

    document.getElementById('bedtime-input').addEventListener('change', showSleepHours);
    document.getElementById('bedtime-input').addEventListener('change', triggerAutoSave);
    document.getElementById('wakeup-input').addEventListener('change', showSleepHours);
    document.getElementById('wakeup-input').addEventListener('change', triggerAutoSave);
});
