document.addEventListener('DOMContentLoaded', () => {

    var data_display = document.querySelector('#data_display').dataset.display;


    // Set up
    		const labels = ['TestUser1', 'TestUser2'];
    		const data = {
    			labels: labels,
    			datasets: [{
    				axis: 'y',
    				label: 'Quiz Score',
    				data: [8, 10],
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


})
