function ajax_caller(func,callback,params) {
    var xmlhttp;
    xmlhttp=new XMLHttpRequest();
    xmlhttp.onreadystatechange=function() {if (xmlhttp.readyState==4 && xmlhttp.status==200) callback(xmlhttp.responseText);}
    var url = "/ajax_map.html?func="+func;
    if(params) url+="&params="+JSON.stringify(params);
    xmlhttp.open("GET",url,true);
    xmlhttp.send();
}