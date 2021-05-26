document.addEventListener('DOMContentLoaded', () => {
    // Get quiz_id from html page
    var quiz_id = document.querySelector('#quiz_id').dataset.id;

    /* GET request to retrieve quiz results*/
    fetch(`/results_displayAPI/${quiz_id}`,    {
        method: 'GET'
    })
    .then(response => response.json())
    .then(results => {

    // Set up barchart using chartjs code.
    		// const labels = ['TestUser1', 'TestUser2'];
    		const data = {
    			labels: results.labels,
    			datasets: [{
    				axis: 'y',
    				label: 'Quiz Score',
    				data: results.data,
    				fill: false,
    				backgroundColor: [
    					'rgba(255, 99, 132, 1.0)',
    					'rgba(255, 159,64, 1.0)'
    				],
    				borderColor: [
    					'rgb(255, 99, 132)',
    					'rgb(255, 159, 64)'
    				],
    				borderWidth: 1
    				}]
    			};


    	// Config
    		const config = {
    			type: 'bar',
    			data,
    			options: {
    				indexAxis: 'y',
    				plugins: {
    					title: {
    						display: true,
    						text: 'Quiz Scores'
    					}
    				}
    			}
    		};

        // Create chart
    		var barChart = new Chart(
    			document.getElementById('barChart'),
    			config
    		);

    });
})
