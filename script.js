function init() {
    updateClock();
    renderGrid();
    setInterval(updateClock, 1000 * 60); // Update clock every minute
    // Check for day change occasionally to re-render grid if needed
    setInterval(() => {
        const now = new Date();
        if (now.getHours() === 0 && now.getMinutes() === 0) {
            renderGrid();
        }
    }, 1000 * 60);
}

function updateClock() {
    const now = new Date();
    const clockEl = document.getElementById('clock');
    const dateEl = document.getElementById('date');

    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    
    clockEl.textContent = `${hours}:${minutes}`;
    
    const options = { weekday: 'short', month: 'short', day: 'numeric' };
    dateEl.textContent = now.toLocaleDateString('en-US', options);
}

function isLeapYear(year) {
    return (year % 4 === 0 && year % 100 !== 0) || (year % 400 === 0);
}

function getDayOfYear(date) {
    const start = new Date(date.getFullYear(), 0, 0);
    const diff = date - start;
    const oneDay = 1000 * 60 * 60 * 24;
    return Math.floor(diff / oneDay);
}

function renderGrid() {
    const gridEl = document.getElementById('day-grid');
    const daysLeftEl = document.getElementById('days-left');
    const percentEl = document.getElementById('percent-complete');

    gridEl.innerHTML = ''; // Clear existing

    const now = new Date();
    const currentYear = now.getFullYear();
    const totalDays = isLeapYear(currentYear) ? 366 : 365;
    const currentDay = getDayOfYear(now);

    // Update Stats
    const daysLeft = totalDays - currentDay;
    const percent = ((currentDay / totalDays) * 100).toFixed(1);

    daysLeftEl.textContent = daysLeft;
    percentEl.textContent = `${percent}%`;

    // Render Circles
    for (let i = 1; i <= totalDays; i++) {
        const circle = document.createElement('div');
        circle.classList.add('day-circle');

        if (i < currentDay) {
            circle.classList.add('filled');
        } else if (i === currentDay) {
            circle.classList.add('current');
        }
        
        // Optional: add tooltips or interactions
        circle.title = `Day ${i}`;
        
        gridEl.appendChild(circle);
    }
}

document.addEventListener('DOMContentLoaded', init);
