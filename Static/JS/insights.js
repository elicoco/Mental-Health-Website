const moodPoints  = JSON.parse(document.getElementById('mood-points').value);
const rollingAvg  = JSON.parse(document.getElementById('rolling-avg').value);
const dowLabels   = JSON.parse(document.getElementById('dow-labels').value);
const dowData     = JSON.parse(document.getElementById('dow-data').value);
const habitStats  = JSON.parse(document.getElementById('habit-stats').value);

const GREEN  = '#4CAF50';
const AMBER  = '#F9A825';
const RED    = '#E53935';
const GREY   = '#e0e0e0';

function moodColour(val) {
    if (val === null) return GREY;
    if (val >= 67) return GREEN;
    if (val >= 34) return AMBER;
    return RED;
}

// ── Mood Trend ──────────────────────────────────────────────
if (moodPoints.length > 0) {
    const trendCtx = document.getElementById('moodTrendChart').getContext('2d');
    new Chart(trendCtx, {
        type: 'line',
        data: {
            datasets: [
                {
                    label: 'Daily Mood',
                    data: moodPoints,
                    borderColor: 'transparent',
                    backgroundColor: moodPoints.map(p => moodColour(p.y)),
                    pointRadius: 4,
                    pointHoverRadius: 6,
                    showLine: false,
                    order: 2
                },
                {
                    label: '7-day Average',
                    data: rollingAvg,
                    borderColor: GREEN,
                    borderWidth: 2,
                    backgroundColor: 'transparent',
                    pointRadius: 0,
                    tension: 0.4,
                    order: 1
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: { mode: 'index', intersect: false },
            scales: {
                x: {
                    type: 'time',
                    time: { tooltipFormat: 'dd MMM yyyy', displayFormats: { month: 'MMM yyyy', day: 'd MMM' } },
                    grid: { display: false },
                    ticks: { color: '#aaa', font: { size: 11 }, maxTicksLimit: 8, maxRotation: 0 }
                },
                y: {
                    min: 0, max: 100,
                    ticks: { color: '#aaa', font: { size: 11 }, stepSize: 25 },
                    grid: { color: '#f0f0f0' }
                }
            },
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: ctx => ctx.dataset.label + ': ' + ctx.parsed.y
                    }
                }
            }
        }
    });
}

// ── Day of Week ──────────────────────────────────────────────
const dowCtx = document.getElementById('dowChart').getContext('2d');
new Chart(dowCtx, {
    type: 'bar',
    data: {
        labels: dowLabels,
        datasets: [{
            data: dowData,
            backgroundColor: dowData.map(v => moodColour(v)),
            borderRadius: 6,
            borderSkipped: false
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            x: { grid: { display: false }, ticks: { color: '#aaa', font: { size: 11 } } },
            y: {
                min: 0, max: 100,
                ticks: { color: '#aaa', font: { size: 11 }, stepSize: 25 },
                grid: { color: '#f0f0f0' }
            }
        },
        plugins: { legend: { display: false } }
    }
});

// ── Habit Completion ─────────────────────────────────────────
if (habitStats.length > 0) {
    const habitCtx = document.getElementById('habitChart').getContext('2d');
    new Chart(habitCtx, {
        type: 'bar',
        data: {
            labels: habitStats.map(h => h.name),
            datasets: [{
                data: habitStats.map(h => h.rate),
                backgroundColor: habitStats.map(h => moodColour(h.rate)),
                borderRadius: 6,
                borderSkipped: false
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    min: 0, max: 100,
                    ticks: { color: '#aaa', font: { size: 11 }, callback: v => v + '%' },
                    grid: { color: '#f0f0f0' }
                },
                y: { grid: { display: false }, ticks: { color: '#555', font: { size: 12 } } }
            },
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: { label: ctx => ctx.parsed.x + '%' }
                }
            }
        }
    });
}
