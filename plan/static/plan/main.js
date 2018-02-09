function graph() {
    var trace1 = {
        x: xcoord,
        y: ycoord,
        type: 'bar',
        text: cap,
    marker: {
        color: 'rgb(188,25,19)'
    }
    };
    console.log(xcoord);
    var data = [trace1];

    var layout = {
        title: '',
        font: {
            family: 'Raleway, snas-serif'
        },
        showlegend: false,
        xaxis: {
            tickangle: -45
        },
        yaxis: {
            zeroline: false,
            gridwidth: 2
        },
        bargap: 0.05
    };

    Plotly.newPlot('tester', data, layout);
};

window.addEventListener('load', graph);
window.addEventListener('resize', graph);
