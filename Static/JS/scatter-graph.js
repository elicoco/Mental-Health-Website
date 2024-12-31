// Original scatter plot data
const scatterData = [
    { x: 1, y: 2 },
    { x: 2, y: 3 },
    { x: 3, y: 5 },
    { x: 4, y: 7 },
    { x: 5, y: 11 }
];

// Function to calculate line of best fit (linear regression)
function calculateRegressionLine(data) {
    const n = data.length;
    let sumX = 0, sumY = 0, sumXY = 0, sumX2 = 0;

    data.forEach(point => {
        sumX += point.x;
        sumY += point.y;
        sumXY += point.x * point.y;
        sumX2 += point.x * point.x;
    });

    const slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX);
    const intercept = (sumY - slope * sumX) / n;

    // Generate points for the line of best fit
    const xValues = data.map(point => point.x);
    const maxX = Math.max(...xValues);
    return [
        { x: 0, y: intercept },
        { x: maxX, y: slope * maxX + intercept }
    ];
}

// Get regression line data
const regressionLine = calculateRegressionLine(scatterData);

// Chart.js configuration
const ctx = document.getElementById('scatterChart').getContext('2d');
const config = {
    type: 'scatter',
    data: {
        datasets: [
            {
                label: 'Scatter Dataset',
                data: scatterData,
                backgroundColor: 'blue',
                pointStyle: 'circle'
            },
            {
                label: 'Line of Best Fit',
                data: regressionLine,
                type: 'line', // Line overlay
                borderColor: 'red',
                borderWidth: 2,
                fill: false,
                showLine: true,
                tension: 0 // Straight line
            }
        ]
    },
    options: {
        scales: {
            x: {
                type: 'linear',
                position: 'bottom',
                title: {
                    display: true,
                    text: 'X-axis'
                },
                min: 0 // Force x-axis to start at 0
            },
            y: {
                title: {
                    display: true,
                    text: 'Y-axis'
                },
                min: 0 // Force y-axis to start at 0
            }
        }
    }
};
// Render the scatter plot with the line of best fit
new Chart(ctx, config);