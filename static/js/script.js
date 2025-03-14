document.getElementById("questionForm").addEventListener("submit", function(event) {
    event.preventDefault();

    const formData = new FormData(this);
    let answers = [];
    let yesCount = 0;
    let total = 0;

    formData.forEach((value) => {
        answers.push(value);
        if (value === "yes") yesCount++;
        total++;
    });

    let yesPercentage = ((yesCount / total) * 100).toFixed(2);
    let noPercentage = (100 - yesPercentage).toFixed(2);

    document.getElementById("result").innerHTML = `
        <h3>Results:</h3>
        <p>Yes: ${yesPercentage}%</p>
        <p>No: ${noPercentage}%</p>
    `;

    // Store response in localStorage (for admin panel)
    let storedResponses = JSON.parse(localStorage.getItem("responses")) || [];
    storedResponses.push(answers);
    localStorage.setItem("responses", JSON.stringify(storedResponses));

    this.reset();
});
