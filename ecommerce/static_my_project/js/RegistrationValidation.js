$(document).ready(function () {
	$('#reg_form').bootstrapValidator({
			// To use feedback icons, ensure that you use Bootstrap v3.1.0 or later
			feedbackIcons: {
				valid: 'glyphicon glyphicon-ok',
				invalid: 'glyphicon glyphicon-remove',
				validating: 'glyphicon glyphicon-refresh'
			},
			fields: {
				first_Name: {
					validators: {
						stringLength: {
							min: 2,
						},
						notEmpty: {
							message: 'First Name Required'
						}
					}
				},
				last_Name: {
					validators: {
						stringLength: {
							min: 2,
						},
						notEmpty: {
							message: 'Last Name is Required'
						}
					}
				},
 				email: {
					validators: {
						notEmpty: {
							message: 'Please supply your email address'
						},
						emailAddress: {
							message: 'Please supply a valid email address'
						}
					}
				},
 				password: {
					validators: {
						identical: {
							field: 'confirmPassword',
							message: 'Confirm your password below - type same password please'
						},
            notEmpty: {
							message: 'Please supply a valid Password'
						}
					}
				},
				confirmPassword: {
					validators: {
						identical: {
							field: 'password',
							message: 'The password and its confirm are not the same'
						},
            notEmpty: {
							message: 'Please Confirm the Password'
						}
 					}
				},
 			}
		})
 		.on('success.form.bv', function (e) {
			$('#success_message').slideDown({
				opacity: "show"
			}, "slow")
			$('#reg_form').data('bootstrapValidator').resetForm();
 			// Prevent form submission
			e.preventDefault();
 			// Get the form instance
			var $form = $(e.target);
 			// Get the BootstrapValidator instance
			var bv = $form.data('bootstrapValidator');
 			// Use Ajax to submit form data
			$.post($form.attr('action'), $form.serialize(), function (result) {
				console.log(result);
			}, 'json');
		});
});