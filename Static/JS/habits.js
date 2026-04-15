document.querySelectorAll('.habit-checkbox').forEach(checkbox => {
    checkbox.addEventListener('change', function() {
        const habitId = parseInt(this.dataset.habitId);
        const date = this.dataset.date;
        const nameSpan = this.nextElementSibling;

        fetch('/toggle_habit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ habit_id: habitId, date: date })
        })
        .then(response => response.json())
        .then(data => {
            if (data.completed) {
                nameSpan.classList.add('completed');
            } else {
                nameSpan.classList.remove('completed');
            }
        })
        .catch(() => {
            // revert checkbox if request failed
            this.checked = !this.checked;
        });
    });
});
