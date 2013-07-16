$(window).load(function() {
	resizeWindow();
});

$(window).on('resize', resizeWindow);

function resizeWindow() {
	$('#wrapper').css('height', $('body').height() - 10);
	app.render();
}
