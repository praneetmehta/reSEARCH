var socket = io.connect('http://0.0.0.0:8080');
socket.on('connect', function() {
    socket.emit('connection', {
        data: '1 User just connected'
    });
});

socket.on('update_suggestions', function(data){
	$('#suggestions').empty();
	query_list = $('#query_text').val().split(' ');
	query = query_list.slice(0,query_list.length - 1).join(' ');
	for(i in data){
		value = ''
		if(query != '' && query != ' '){
			value = query.trim()+' '+data[i]['suggestion'].trim();
		}
		else{
			value = data[i]['suggestion'];
		}
		$('#suggestions').append('<option value="'+value.trim()+'">');
	}
});

$('#query_text').on('keyup', function() {
    if (this.value.length > 0) {
    	query_list = $('#query_text').val().split(' ');
    	query = query_list[query_list.length - 1];
        socket.emit('typing', {
            data: query
        });
    }
});

function submit_query(){
	query = $('#query_text').val();
	socket.emit('query_submit', {
		data:query
	});
}

socket.on('update_results', function(data){
	html = ''
	keys = ''
	for(entry in data.slice(0,data.length - 1)){
		link = data[entry]['link']
		keyarray = data[entry]['keywords']
		for(key in keyarray){
			keys+= '<div class="keyword">'+keyarray[key]['key']+'</div>'
		}
		html+='<div class="search_result"><button class="close hide hidden">x</button><h2 class="title">'+data[entry]['title']+'</h2><h4 class="auth">'+data[entry]['authors']+'</h3><h4 class="sub">'+data[entry]['subject']+'</h4><p class="doc_text">'+data[entry]['doc_text']+'</p><div class="keywords">'+keys+'</div><div class="download"><a href='+link+' download><img src="static/img/download.png" style="width:100%; height:100%"></a></div><div class="search_similar">Similar</div></div>'
		keys = ''
	}
	display_time_results(data[data.length-1]);
	$('#results_holder').empty();
	$('#results_holder').html(html);
	bind();
})