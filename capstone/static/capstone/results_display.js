document.addEventListener('DOMContentLoaded', () => {
    // Get quiz_id from html page
    var quiz_id = document.querySelector('#quiz_id').dataset.id;

    //Code from Django docs to handle CSRF token in Fetch calls
        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        const csrftoken = getCookie('csrftoken');

    /* GET request to retrieve quiz results*/
    fetch(`/results_displayAPI/${quiz_id}`,    {
        method: 'GET',
        credentials: 'same-origin',
        headers: {
            'X-CSRFToken': csrftoken,
        }
    })
    .then(response => response.json())
    .then(results => {

    // Set up barchart using chartjs code.
    		const data = {
    			labels: results.labels,
    			datasets: [{
    				axis: 'y',
    				label: 'Quiz Score',
    				data: results.data,
    				fill: false,
    				backgroundColor: [
    					'rgba(215, 51, 56, 1.0)',
    					'rgba(76, 129, 0, 1.0)'
    				],
    				borderColor: [
    					'rgb(215, 51, 56)',
    					'rgb(76, 129, 0)'
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
