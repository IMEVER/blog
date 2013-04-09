// core.js
//   core js file
// 2013-02-01, Rhett
var CM = {
	self : this ,
    $     : function(sel,ele){
        if(ele !== undefined)
            return ele.querySelectorAll(sel);
         else
            return document.querySelectorAll(sel);
    },
	refresh : function(){
		window.location = window.location ;
	},
	ajax : (function(){
			var xmlhttp = new XMLHttpRequest();
			var get = function(url,func){
				xmlhttp.onreadystatechange = function(){
					if (xmlhttp.readyState == 4 && xmlhttp.status==200)
					{
						func(JSON.parse(xmlhttp.responseText)) ;
					}					
				};
				xmlhttp.open( "GET", url, false);
				xmlhttp.send(null);				
			};
			var post = function(url,data,func){
				xmlhttp.onreadystatechange = function(){
					if (xmlhttp.readyState == 4 && xmlhttp.status==200)
					{
						console.log(xmlhttp.responseText) ;
						console.log(JSON.parse(xmlhttp.responseText)) ;
					}
				};
				xmlhttp.open( "POST", url, false);//同步
				//xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
				xmlhttp.send(data);
			};
			return {get:get,post:post};
	})() ,
	mask : function(){
		var mask = null ;
		function init(){
			if(mask === null){
				mask = document.createElement("div");
				mask.className = "mask";
				mask.style.position = "absolute";
				var p = document.createElement("p");
				p.textContent = "数据加载中......";
				mask.appendChild(p);
				document.body.appendChild(mask);
			}
			return ;
		}
		function show(){
			init();			
			mask.style.display = "block";			
		}
		function hide(){
			if(mask) mask.style.display = "none";						
		}
		return {show:show,hide:hide};
	}(),
	cookie : function(){
		var getCookieVal = function (offset) {
			var endstr = document.cookie.indexOf(";", offset);
			if (endstr == -1)
				endstr = document.cookie.length;
			return unescape(document.cookie.substring(offset, endstr));
		} ;        
        var getcookie = function (name) {
			var arg = name + "=";
			var alen = arg.length;
			var clen = document.cookie.length;
			var i = 0;
			var j = 0;
			while (i < clen) {
				j = i + alen;
				if (document.cookie.substring(i, j) == arg)
					return getCookieVal(j);
				i = document.cookie.indexOf(" ", i) + 1;
				if (i === 0)
					break;
			}
			return '';
		};
        var getCookie = function (b){var a=document.cookie.match(new RegExp("(^| )"+b+"=([^;]*)(;|$)"));return a?unescape(a[2]):null;};
		var setcookie = function (name, val, day) {
			var expires = '';
			day = day === undefined ? 3 : day ;
			var exp = new Date();
			exp.setTime(exp.getTime() + day * 24 * 60 * 60 * 1000);
			expires = ";expires=" + exp.toGMTString();

			document.cookie = name + "=" + escape(val) + expires ;
		} ;
		var cookie = function(){
			if(arguments.length>1){
				return setcookie(arguments[0],arguments[1]);
			}else if(arguments.length == 1){
				return getcookie(arguments[0]);
			}else{
				return false ;
			}
		};
		return cookie ;
	}(),
	fade : function(ele1,ele2){
		ele1.style.opacity = 0 ;
		ele1.style.display = "none";
		
		ele2.style.opacity = 0 ;
		ele2.style.display = "block";
		setTimeout(function(){ele2.style.opacity=1;},100);
	},
	tips : function(){
		var tipele = document.createElement("div");
		tipele.className = "tip";
		var p = document.createElement("p");
		tipele.appendChild(p);
		
		function init(){
			if(document.querySelector(".tip"))
				return ;
			document.body.appendChild(tipele);			
		}
		
		function success(obj){
			init();
            var msg ;
            if(typeof obj === "object")
                msg = obj.msg ;
            else if(typeof obj === "string")
                msg = obj ;
            else
                msg = "回答正确，下一题" ;
            
			p.innerHTML = msg ;
			tipele.style.display = "block";
			tipele.style.left = document.body.offsetWidth/2 - tipele.offsetWidth/2 + "px";
			setTimeout(function(){tipele.style.opacity=1;},100);
		}
		function error(obj){
			init();
            
            var msg ;
            if(typeof obj === "object")
                msg = obj.msg ;
            else if(typeof obj === "string")
                msg = obj ;
            else
                msg = "回答错误，下一题" ;            
            
			p.innerHTML = msg ;
			tipele.style.display = "block";
			tipele.style.left = document.body.offsetWidth/2 - tipele.offsetWidth/2 + "px";
			setTimeout(function(){tipele.style.opacity=1;},100);
		}
		function hide(){
			if(document.querySelector(".tip")){
				tipele.style.opacity=0 ;
				setTimeout(function(){tipele.style.display = "none";},1000);
			}
		}
		return {success:success,error:error,hide:hide};
	}(),
	init : function (){
	},
	loading:function(){
		function loading(canvas,options){
			this.canvas = canvas;
			if(options){
				this.radius = options.radius||12;
				this.circleLineWidth = options.circleLineWidth||4;
				this.circleColor = options.circleColor||'lightgray';
				this.dotColor = options.dotColor||'gray';
			}else{      
				this.radius = 12;
				this.circelLineWidth = 4;
				this.circleColor = 'lightgray';
				this.dotColor = 'gray';
			}
		};

		loading.prototype = {
			show:function (){
				var canvas = this.canvas;
				if(!canvas.getContext)	return ;
				if(canvas.__loading)	return ;
				canvas.__loading = this;
				var ctx = canvas.getContext('2d');
				var radius = this.radius;      
				var rotators = [{angle:0,radius:1.5},{angle:3/radius,radius:2},{angle:7/radius,radius:2.5},{angle:12/radius,radius:3}];      
				var me = this;
				canvas.loadingInterval = setInterval(function(){
					ctx.clearRect(0,0,canvas.width,canvas.height);         
					var lineWidth = me.circleLineWidth;
					//var center = {x:canvas.width/2 - radius,y:canvas.height/2-radius};          
					var center = {x:canvas.width/2, y:canvas.height/2};
					ctx.beginPath();
					ctx.lineWidth = lineWidth;
					ctx.strokeStyle = me.circleColor;
					ctx.arc(center.x,center.y,radius,0,Math.PI*2);
					ctx.closePath();
					ctx.stroke();
					for(var i=0;i<rotators.length;i++){
			  	  		var rotatorAngle = rotators[i].currentAngle||rotators[i].angle;
		  				//在圆圈上面画小圆
		  				var rotatorCenter = {x:center.x-(radius)*Math.cos(rotatorAngle) ,y:center.y-(radius)*Math.sin(rotatorAngle)};
						var rotatorRadius = rotators[i].radius;
						ctx.beginPath();
						ctx.fillStyle = me.dotColor;
						ctx.arc(rotatorCenter.x,rotatorCenter.y,rotatorRadius,0,Math.PI*2);
						ctx.closePath();
						ctx.fill();
						rotators[i].currentAngle = rotatorAngle+4/radius;
					}
				},50);
			},
			hide:function(){
				var canvas = this.canvas;
				canvas.__loading = false;
				if(canvas.loadingInterval){
					window.clearInterval(canvas.loadingInterval);
				}
				var ctx = canvas.getContext('2d');
				if(ctx)ctx.clearRect(0,0,canvas.width,canvas.height);
			} 
		};
		return loading;
	}()
};
