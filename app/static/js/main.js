function bind(){
	$('.search_result').click(function(){
		$("html, body").animate({ scrollTop: 0 }, "slow");
		if(!$(this).hasClass('clicked')){
			console.log('class');
			ele = $(this);
			ele.siblings().addClass('hide');
			ele.siblings().addClass('hidden');
			setTimeout(function(){
				ele.addClass('clicked');
				ele.find('.close').removeClass('hide hidden');
				ele.find('p').css({'display':'block'});
			},300);	
		}
	});
	$('.close').click(function(evt){
		evt.stopPropagation();
		ele = $(this);
		console.log(ele);
		par = ele.parent()
		par.removeClass('clicked');
		par.siblings().removeClass('hide');
		setTimeout(function(){
			ele.addClass('hide hidden');
			par.siblings().removeClass('hide hidden');
			par.removeClass('clicked');
			par.removeClass('hide hidden');
			par.find('p').css({'display':'none'});
		},300);
	})
}

$('form').submit(function(e){
	return false
});

$('#submit_query').click(function(){
	submit_query();
});

bind();