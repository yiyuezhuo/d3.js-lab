

box_max_width=300;
box_height=30;
box_count=11;

var svg=d3.select('svg').attr('height',box_count*box_height).attr('width',box_max_width);


endog_format=[
	{key:'L1',min:0,max:10000},
	{key:'L2',min:0,max:10000},
	{key:'N',min:0,max:1000},
	{key:'P',min:0,max:0.02},
	{key:'W',min:0,max:100},
	{key:'c',min:0,max:100000},
	{key:'f',min:0,max:1000},
	{key:'h',min:0,max:1000},
	{key:'i',min:0,max:20000},
	{key:'r',min:0,max:1},
	{key:'y',min:0,max:100000}
]

var scale={};
endog_format.forEach(function(d){
	scale[d.key]=d3.scale.linear().domain([d.min,d.max]).range([0,box_max_width]);
});

function formatData(jsonData){
	var rl=[];
	endog_format.forEach(function(d){
		var obj={};
		obj['key']=d.key;
		obj['value']=jsonData[d.key];
		rl.push(obj)
	})
	return rl;
}

function updateBar(data){
	var rects=svg.selectAll('rect').data(data);
	rects.enter().append('rect')
		.attr('x',0).attr('y',function(d,i){return i*box_height;})
		.attr('height',box_height).attr('width',function(d,i){return scale[d.key](d.value)});
	rects.transition()
		.attr('width',function(d,i){return scale[d.key](d.value)});
}



d3.select('#getResult').on('click',function(){
	var data={};
	['g','t','kbar','M'].forEach(function(d){
		data[d]=document.getElementsByName(d)[0].value
	});
	
	var send_content=JSON.stringify(data);
	//var send_content='g=100&t=100&kbar=100&M=100';
	
	d3.json('/solve')
		.header("Content-Type", "application/x-www-form-urlencoded")
		.post(send_content, function(error,data){
		if (data){
			myjson=data;
			d3.select('#messageBar').data(['后台数据载入完成，前端载入完成']).text(function(d,i){return d});
			d3.select('input').data(['吼啊']).enter().append('input').attr('value',function(d,i){
				return d;
			});
			
			updateBar(formatData(data));
		}
		else{
			console.log('get json fail');
		}
	});

})

d3.select('#load').on('click',function(){
	var xhr=d3.xhr('/load');
	d3.select('#load').style('display','none');
	d3.select('#messageBar').data(['后台数据载入完成，未在前端载入']).text(function(d,i){return d});
	xhr.get();
});
