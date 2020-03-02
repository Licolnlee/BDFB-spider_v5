[ADT 3]
! Checksum: vXO2skD37egAcrKzRVhe1A
! Version: 20190821
! Title: 过滤增强脚本
! Homepage: http://www.adtchrome.com/extension/adt-videolist.html
! Match: http
! Begin: --

//remove baidu search ad
var _countAA = 0
function doBBBd(){
    var alla = document.getElementsByTagName('a')
    for(var i = 0; i < alla.length; i++){
        if(/baidu.com\/(baidu.php\?url=|adrc.php\?t)/.test(alla[i].href)){
            var _temp = alla[i].parentElement, loop = 0
            while(loop < 5){
                _temp = _temp.parentElement
                loop++
                if(_temp.parentElement.id == 'content_left'){
                    _temp.remove()
                    break
                }
            }
        }
    }
    
    if(_countAA++ < 20){
        setTimeout(doBBBd, 500)
    }
    
}
doBBBd()
document.addEventListener('keyup', function(){_countAA-=10;doBBBd()}, false)
document.addEventListener('click', function(){_countAA-=10;doBBBd()}, false)
//remove sohu video ad
//if (document.URL.indexOf("tv.sohu.com") >= 0){
//    if (document.cookie.indexOf("fee_status=true")==-1){document.cookie='fee_status=true'};
//}

//remove 56.com video ad
//if (document.URL.indexOf("56.com") >= 0){
//    if (document.cookie.indexOf("fee_status=true")==-1){document.cookie='fee_status=true'};
//}