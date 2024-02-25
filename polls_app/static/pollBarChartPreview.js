async function getPollResults(pollId) {
    const response = await fetch(`/api/${pollId}/results`).then(response => response.json())
    return response
}

const polls = document.querySelectorAll('.poll-results-chart');
polls.forEach((poll, index) => {
    const pollId = poll.dataset.pollId;
    getPollResults(pollId).then(data => {
        const pollVotes = data.map(subList => subList[1]);
        const bar = customBarFactory(pollVotes);
        poll.appendChild(bar);

    })
});

const customBarFactory = (pollValues) => {

    const barSegmentColors = ['#36a2eb', '#ff6384', '#4bc0c0', '#ff9f40', '#ffcd56', '#c9cbcf', '#8a80b1', '#ffa07a']
    const bar = document.createElement('div');
    const totalVotesCount = pollValues.reduce((acc, curr) => acc + curr);

    bar.classList.add('custom-bar');
    const nonZeroPollValues = pollValues.filter(numberOfVotes => parseInt(numberOfVotes) > 0)

    for (let i = 0; i < nonZeroPollValues.length; i++) {
        const barSegment = document.createElement('div');
        const barSegmentWidth = (nonZeroPollValues[i] / totalVotesCount) * 100;
        barSegment.classList.add('bar-segment');
        barSegment.style.width = `${barSegmentWidth}%`;
        barSegment.style.backgroundColor = barSegmentColors[i];
        bar.appendChild(barSegment);
    }
    return bar;
}