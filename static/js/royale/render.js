$(window).load(function() {
	resizeWindow(true);
});

$(window).on('resize', resizeWindow);

function resizeWindow(firstLoad) {
	$('#wrapper').css('height', $('body').height() - 10);
	app.render(firstLoad === true ? false : true);
}
