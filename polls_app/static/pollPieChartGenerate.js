async function getPollResults(pollId) {
    const response = await fetch(`/api/${pollId}/results`).then(response => response.json())
    return response
}

async function generateChart() {

    const pollId = document.querySelector('#poll-results').dataset.pollId;
    const pollResults = await getPollResults(pollId)

    const pollAnswers = pollResults.map(subList => subList[0]);
    const pollVotes = pollResults.map(subList => subList[1]);
    const pollPercentages = pollResults.map(subList => subList[2]);

    const ctx = document.getElementById('poll-results');
    const chart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: pollAnswers,
            datasets: [{
                label: 'Number of Votes:',
                data: pollVotes,
                borderWidth: 1
            }]
        },
        options: {
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            const dataIndex = context.dataIndex;
                            const percentage = Math.round(pollPercentages[dataIndex], 2);
                            const label = `${context.dataset.label} ${context.raw} (${percentage}%)`;
                            return label;
                        }
                    }
                }
            }
        }
    });

    const chart_colors = chart.data.datasets[0].backgroundColor
    const progressBars = document.querySelectorAll('.progress-bar');
    for (let i = 0; i < progressBars.length; i++) {
        progressBars[i].style.backgroundColor = chart_colors[i];
    }
}

generateChart();
