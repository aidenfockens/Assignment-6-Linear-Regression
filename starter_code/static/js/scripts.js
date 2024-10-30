document.getElementById("regressionForm").addEventListener("submit", function (event) {
    event.preventDefault();

    const N = document.getElementById("N").value;
    const mu = document.getElementById("mu").value;
    const sigma2 = document.getElementById("sigma2").value;
    const S = document.getElementById("S").value;

    const formData = new FormData();
    formData.append("N", N);
    formData.append("mu", mu);
    formData.append("sigma2", sigma2);
    formData.append("S", S);

    fetch("/", {
        method: "POST",
        headers: {
            "X-Requested-With": "XMLHttpRequest"
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Clear out previous images
        document.getElementById("results").innerHTML = `
            <h2>Generated Plot</h2>
            <img id="plot1" src="${data.plot1_url}" alt="Regression Plot" style="width: 600px;">
            
            <h2>Histogram of Slopes and Intercepts</h2>
            <img id="plot2" src="${data.plot2_url}" alt="Histograms" style="width: 600px;">
            
            <p id="slopeExtreme">Proportion of slopes more extreme than calculated slope: ${(data.slope_extreme * 100).toFixed(2)}%</p>
            <p id="interceptExtreme">Proportion of intercepts more extreme than calculated intercept: ${(data.intercept_extreme * 100).toFixed(2)}%</p>
        `;
        document.getElementById("refreshButton").disabled = false;

        
    })
    .catch(error => console.error("Error:", error));
});

document.getElementById("refreshButton").addEventListener("click", function () {
    window.location.reload();
});