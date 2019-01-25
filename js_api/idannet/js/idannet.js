// Author: Zenobia Liendo





    function  render_idann_viz(data, patient_info) {
		// ===================================================================================
                // ESI score
		// ===================================================================================
		$("#ESI").text(data.esi);
		if  (data.esi == 1){ 
			$("#esi-box").css("background-color", "red");
			}
		else if (data.esi == 2) {		       
			$("#esi-box").css("background-color", "orange");		
		} else if (data.esi == 3) {
			$("#esi-box").css("background-color", "#f4ee2c;");	
		} else if (data.esi == 4) {
			$("esi-box").css("background-color", "#d5f279;");	
		} else if (data.esi == 5) {
			$("esi-box").css("background-color", "#6cc464;");	
		}
		
		// ===================================================================================
                // co probability
		// ===================================================================================
		co_prob =  parseFloat( ( data.co).toFixed(2) );
		left_prob = 1 - co_prob
		Highcharts.chart('co_prob', {
		  exporting: { enabled: false },
		  chart: {
			plotBackgroundColor: null,
			borderWidth: 0,
			plotBorderWidth: 0,
			plotShadow: false,
			margin:  [0, 0, 0, 0]
		  },
		  title: {
			text: co_prob ,
			align: 'center',
			verticalAlign: 'middle',
			 style: {
			        fontSize: '20px',
				fontWeight: 'bold'
			},
			y: 0
		  },
		  credits: {
                        enabled: false
                    },
		  plotOptions: {

			pie: {	
			dataLabels: {
				enabled: false
			  },
			  enableMouseTracking: false,
			  startAngle: -90,
			  endAngle: 90,
			  center: ['50%', '50%'],
			  colors: ['orange','gray']
			}
		  },
		  series: [{
			type: 'pie',
			name: 'Critical Outcomes Probability',
			innerSize: '50%',
			animation: false,
			data: [ 	co_prob	  ,  left_prob]
			
		  }]
		});

		
		// ===================================================================================
                // patient info 
		// ===================================================================================
		$('#patient_info').append('<tr> <td>' + 'Age' + '</td> <td>' +  patient_info.AGE + '</td> </tr>')
		
		gender = "Female"
		if  ( patient_info.SEX == 2) {
			gender = "Male"		
		}		
		$('#patient_info').append('<tr> <td>' + 'Gender' + '</td> <td>' + gender + '</td> </tr>')
		
		
		arrived_by_ambulance = "No"
		if  ( patient_info.ARREMS == 1) {
			gender = "Yes"		
		}
		$('#patient_info').append('<tr> <td>' + 'Arrived by Ambulance?' + '</td> <td>' + arrived_by_ambulance + '</td> </tr>')		
		
		// vital signs 
		temperature = patient_info.TEMPF / 10 
		$('#patient_info').append('<tr> <td>' + 'Temperature' + '</td> <td>' + temperature + '</td> </tr>')		
		$('#patient_info').append('<tr> <td>' + 'Heart Rate' + '</td> <td>' + patient_info.PULSE + '</td> </tr>')
		$('#patient_info').append('<tr> <td>' + 'Respiratory Rate' + '</td> <td>' + patient_info.RESPR + '</td> </tr>')
		$('#patient_info').append('<tr> <td>' + 'Systolic Blood Pressure' + '</td> <td>' + patient_info.BPSYS + '</td> </tr>')
		$('#patient_info').append('<tr> <td>' + 'Pulse Oxymetry' + '</td> <td>' + patient_info.POPCT+ '</td> </tr>')
		
		//RFV		
		RFV= ""
		if  (patient_info.RFV1 != -9){
			RFV += 	patient_info.RFV1 
		}		
		if  (patient_info.RFV2 != -9){
		       if (RFV.length >0 ) {RFV += ", "}
			RFV += 	patient_info.RFV2 
		}		
		if  (patient_info.RFV3 != -9){
		       if (RFV.length >0 ) {RFV += ", "}
			RFV += 	patient_info.RFV3 
		}

		$('#patient_info').append('<tr> <td>' + 'Reason for Visit Codes' + '</td> <td>' + RFV+ '</td> </tr>')

		//other fields
		MSA = "Yes"
		if  (patient_info.MSA == 2){
			MSA = "No"
		}
		
		$('#patient_info').append('<tr> <td>' + 'Metropolitan Statistical Area' + '</td> <td>' + MSA+ '</td> </tr>')
		
		diabetes = "No"
		if  (patient_info.DIABETES == 1){
			diabetes = "Yes"
		}
		$('#patient_info').append('<tr> <td>' + 'Diabetes History' + '</td> <td>' + diabetes+ '</td> </tr>')
		
		chf = "No"
		if  (patient_info.CHF == 1){
			chf= "Yes"
		}
		$('#patient_info').append('<tr> <td>' + 'Congestive heart failure History' + '</td> <td>' +chf+ '</td> </tr>')
		
	// attention rank
        // -------------------------------------------------------------------------
		
		feature_name_list =   [] 
		attention_value_list =  [] 
		for (var i = 0; i < data.co_fi.length; i++) {
		        factor = ""
		        if  (data.co_fi[i].input_value == 0 || data.co_fi[i].input_value == null  ) {
				factor = "NOT "
			}				
			feature_name = data.co_fi[i].featureName
			if (feature_name == "arrival_model") feature_name  = "arrival_mode";
			if (feature_name == "diabetes_indicator") feature_name  = "diabetes_history";
			if (feature_name == "chf_indicator") feature_name  = "chf_history";
			factor += feature_name ;
			att_value =  parseFloat( ( data.co_fi[i].attention_weight).toFixed(4) ); 
			feature_name_list.push(factor);
			attention_value_list.push(att_value)		;
		}
		//console.log(data.co_fi)
		Highcharts.chart('attention_rank', {
			chart: {
				type: 'bar'
			},
			title: {
				text: 'Top 15 Attention levels',
				style: {
					fontWeight: 'bold',
					fontFamily: '-apple-system,BlinkMacSystemFont,"Segoe UI", Roboto'
				}
			},

			xAxis: {
				categories: feature_name_list,
				title: {
					text: null
				}
			},
			yAxis: {
				min: 0,
				title: {
					text: 'Ratio',
					align: 'high'
				},
				labels: {
					overflow: 'justify'
				}
			},
			tooltip: {
				valueSuffix: ' '
			},
			plotOptions: {
				bar: {
					dataLabels: {
						enabled: true
					}
				}
			},
		 
			credits: {
				enabled: false
			},
			series: [{
				name: 'Attention Ratio',
			        color: '#0213d1',
				data: attention_value_list
			}]
		});

		
   }; // end of function
 
$(document).ready(function(){

       $.getJSON('config.json', function( url_data ) {
	   //console.log(url_data);
	   patient_info_url = url_data.patient_info_url;
	   idannet_response_url =  url_data.idannet_response_url;   

	$.getJSON(patient_info_url, function( patient_data ) {
		patient_info = patient_data[0]	
		$.getJSON( idannet_response_url, function( data ) {
			idannet_response = data;	
			render_idann_viz(idannet_response, patient_info);
	
		})		
	})
	
	})
})	
	
/*   // console.log (idannet_response);
   
	if(window.parent.readyState!= 'complete') {
		//render_idann_viz(idannet_response, patient_info);
	//} else 	{
		$( window.parent ).on( "load", function() { 
		render_idann_viz(idannet_response, patient_info);		
		}) 	
	}


});*/
