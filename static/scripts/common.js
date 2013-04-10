(function(window,undefined){
  window.addEventListener("load",function(){
    $.get("/article/recommend",function(data){
      console.log(data)
      var ul = document.querySelector(".recommendList");
      var child ;
      while(child=ul.firstChild)
        ul.removeChild(child)

      if(data.status == 1){
        for(var i=0,len=data.data.length;i<len;i++){
          var li = document.createElement("li");
          var a = document.createElement("a")
          a.href = "/article?id=" + data.data[i].id ;
          a.textContent = data.data[i].title;
          li.appendChild(a);
          ul.appendChild(li)
        }
      }else{
        var li = document.createElement("li");
        li.textContent = "Errors:" + data.msg ;
        ul.appendChild(li)
      }
    })
  });
})(window,undefined)
