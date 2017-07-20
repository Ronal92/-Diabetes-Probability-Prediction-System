$(function(){
	$('#btnSignUp').click(function(){

		$.ajax({
			url:'/signUp',
			type: 'GET',
			success: function(response){
				console.log(response);
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});


