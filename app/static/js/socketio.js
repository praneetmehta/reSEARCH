var socket = io.connect('http://172.16.47.29:8080');
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
	for(entry in data){
		keyarray = data[entry]['keywords']
		for(key in keyarray){
			keys+= '<div class="keyword">'+keyarray[key]['key']+'</div>'
		}
		html+='<div class="search_result"><button class="close hide hidden">x</button><h2 class="title">'+data[entry]['title']+'</h2><h4 class="auth">'+data[entry]['authors']+'</h3><h4 class="sub">'+data[entry]['subject']+'</h4><p class="doc_text">'+data[entry]['doc_text']+'</p><div class="keywords">'+keys+'</div><div class="search_similar">Similar</div></div>'
		keys = ''
	}
	$('#results_holder').empty();
	$('#results_holder').html(html);
	bind();
})