$(window).load(function() {
	resizeWindow();
});

$(window).on('resize', resizeWindow);

function resizeWindow() {
	$('#wrapper').css('height', $(window).height() - 10);
	$('img').each(function() {
		$(this).css('height', $(this).parents('.feed-element').height() * 0.8);
	});
}
