$(document).ready(function(){  
  function cli(item){
    var tpl = '<li><div class="comment-box clearfix" id="comment_'+item.id+'"><div class="comment-avatar"><img src="'+item.head+'"></div><div class="comment-info"><p class="comment-user">'+item.author+'</p><p class="comment-time">'+item.date+'</p><div><p class="comment-content">'+item.content+'</p></div><div class="comment-action"><span data-id="'+item.id+'" data-dir="inc">UP('+item.upnum+')</span> | <span data-id="'+item.id+'" data-dir="dec">DOWN('+item.downnum+')</span></div></div></div></li>';
    return tpl;
  }
  $("#comment-submit").click(function(){
    if(validateComment()){
      var params = {'author':$("#name-input").val(), 'email': $("#email-input").val(), 'website': $("#website-input").val(), 'content': $("#comment-input").val(), 'post_id': $("input[name=post_id]").val()};
      $.post("/comment/add",params,function(data){
        console.log(data);
        if(data.status == 1){
          params.id = data.cid ;
          params.downnum = params.upnum = 0 ;
          var div = document.createElement("div");
          div.innerHTML = cli(params);
          document.querySelector("#comments-list ol").appendChild(div.firstChild);
        }else{
          alert(data.msg);
        }
      });
    }
    return false;
  });


  $.get('/comment?id='+$("input[name=post_id]").val(),function(data){
    var len = data.data.length;
    var html = '<h3>'+len+' comments</h3>';
    html += '<ol>';
    for(var i=0;i<len;i++){
      html += cli(data.data[i])
    }
    html += '</ol>';
    setTimeout(function(){document.getElementById("comments-list").innerHTML = html},5000) ;
  })
});

function validateComment(){
  var isValidated = true;
  if($("#name-input").val().trim() == ""){
    $("#name-error").removeClass("unshown");
    isValidated = false;
  }else{
    $("#name-error").addClass("unshown");
  }
  if($("#email-input").val().trim() == ""){
    $("#email-error").removeClass("unshown");
    isValidated = false;
  }else{
     if(!$("#email-input").val().match(/^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/)){
       $("#email-error").removeClass("unshown");
       isValidated = false;
     }else{
      $("#email-error").addClass("unshown");
      //document.cookie = "email="+$("#email-input").val().trim();
     }
  }
  if($("#comment-input").val().trim() == ""){
    $("#comment-error").removeClass("unshown");
    isValidated = false;
  }else{
    $("#comment-error").addClass("unshown");
  }
  return isValidated;
}

(function(window,undefined){
	$("#comments-list").delegate(".comment-action span","click",function(){
		var self = this;
		var cid = this.dataset.id;
		var oldvalue = parseInt(this.innerHTML.match(/\((-?\d+)\)/)[1]);
		var dir = this.dataset.dir ;
		var newvalue = oldvalue + 1;
		
		$.post("/comment/vote", {'cid':cid, 'dir':dir}, function(data){
			if(data.status == -1)
				console.log("Errors:"+data.msg);
			else if(data.status == 0)
				console.log("Warning:"+data.msg);
			else {				
				self.innerHTML = self.innerHTML.replace(/\d+/,newvalue);
				console.log("Success:"+data.msg);		
			}
		});
	});
	$(".comment-action span[data-dir=inc]").each(function(i,item){
		var num = parseInt(item.innerHTML.match(/\((\d+)\)/)[1]);
		if(num > 5){
			$(item).parent().prev().get(0).style.backgroundColor = "#ffffcc";
		}
	});
})(window,undefined)
