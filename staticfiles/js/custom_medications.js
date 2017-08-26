$(document).ready(function(){

	$('label[for="id_completionDate"]').hide()
	$('#id_completionDate').hide()
	$('label[for="id_completionRx"]').hide()
	$('#id_completionRx').hide()
	$('label[for="id_completionMedication"]').hide()
	$('#id_completionMedication').hide()
	$('#id_medicationResident').hide()
	$('label[for="id_medicationResident"]').hide()
	$('label[for="id_medicationTimeSchedule"]').hide()
	$('#id_medicationTimeSchedule').hide()
	$('label[for="id_medicationTimeSchedule2"]').hide()
	$('#id_medicationTimeSchedule2').hide()
	$('label[for="id_medicationTimeSchedule3"]').hide()
	$('#id_medicationTimeSchedule3').hide()
	$('label[for="id_medicationTimeSchedule4"]').hide()
	$('#id_medicationTimeSchedule4').hide()
	$('label[for="id_medicationTimeSchedule5"]').hide()
	$('#id_medicationTimeSchedule5').hide()
	$('label[for="id_medicationTimeSchedule6"]').hide()
	$('#id_medicationTimeSchedule6').hide()



	$('#id_medicationDistribution').change(function(){
		var selectedValue = $(this).val();

		if(selectedValue === '1'){
		$('#id_medicationTimeSchedule').show()
		$('#id_medicationTimeSchedule2').hide()
		$('#id_medicationTimeSchedule3').hide()
		$('#id_medicationTimeSchedule4').hide()
		$('#id_medicationTimeSchedule5').hide()
		$('#id_medicationTimeSchedule6').hide()

	}
	else if(selectedValue ==='2'){
		$('#id_medicationTimeSchedule').show()
		$('#id_medicationTimeSchedule2').show()
		$('#id_medicationTimeSchedule3').hide()
		$('#id_medicationTimeSchedule4').hide()
		$('#id_medicationTimeSchedule5').hide()
		$('#id_medicationTimeSchedule6').hide()
	}
		else if(selectedValue ==='3'){
		$('#id_medicationTimeSchedule').show()
		$('#id_medicationTimeSchedule2').show()
		$('#id_medicationTimeSchedule3').show()
		$('#id_medicationTimeSchedule4').hide()
		$('#id_medicationTimeSchedule5').hide()
		$('#id_medicationTimeSchedule6').hide()
	}

	else if(selectedValue ==='4'){
		$('#id_medicationTimeSchedule').show()
		$('#id_medicationTimeSchedule2').show()
		$('#id_medicationTimeSchedule3').show()
		$('#id_medicationTimeSchedule4').show()
		$('#id_medicationTimeSchedule5').hide()
		$('#id_medicationTimeSchedule6').hide()
	}

	else if(selectedValue ==='5'){
		$('#id_medicationTimeSchedule').show()
		$('#id_medicationTimeSchedule2').show()
		$('#id_medicationTimeSchedule3').show()
		$('#id_medicationTimeSchedule4').show()
		$('#id_medicationTimeSchedule5').show()
		$('#id_medicationTimeSchedule6').hide()
	}

	else if(selectedValue ==='6'){
		$('#id_medicationTimeSchedule').show()
		$('#id_medicationTimeSchedule2').show()
		$('#id_medicationTimeSchedule3').show()
		$('#id_medicationTimeSchedule4').show()
		$('#id_medicationTimeSchedule5').show()
		$('#id_medicationTimeSchedule6').show()
	}




	})

$("form").submit(function() {
    $(this).submit(function() {
        return false;
    });
    return true;
});

})
