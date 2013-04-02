$(document).ready(function(){
  $("#comment-submit").click(function(){
    return validateComment();
  });
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
	$(".comment-action span").click(function(){
		var cid = this.dataset.id;
		var oldvalue = parseInt(this.innerHTML.match(/\((\d+)\)/)[1]);
		var dir = this.dataset.dir ;
		var newvalue = oldvalue + 1;
		this.innerHTML = this.innerHTML.replace(/\d+/,newvalue);
		
		$.post("/comment/vote", {'cid':cid, 'dir':dir}, function(data){
			if(data.status == -1)
				console.log("Errors:"+data.msg);
			else
				console.log("Success:"+data.msg);		
		});
	});
	$(".comment-action span[data-dir=inc]").each(function(i,item){
		var num = parseInt(item.innerHTML.match(/\((\d+)\)/)[1]);
		if(num > 5){
			$(item).parents(".comment-box").get(0).style.backgroundColor = "#ffffcc";
		}
	});
})(window,undefined)
