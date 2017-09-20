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
	});

	$('.keyword').click(function(evt){
		evt.stopPropagation();
		value = $(this).text();
		$('#query_text').val(value);
		socket.emit('query_submit', {
			data:value
		});
	});
	$('.search_similar').click(function(evt){
		ele = $(this)
		evt.stopPropagation();
		value = '';
		keys = ele.parent().find('div.keywords').children().each(function(){
			value+= $(this).text()+ ' ';
		});

		$('#query_text').val(value);
		console.log(value);
		socket.emit('query_submit', {
			data:value
		});
	})
}

$('form').submit(function(e){
	return false
});

$('#submit_query').click(function(){
	submit_query();
});

bind();