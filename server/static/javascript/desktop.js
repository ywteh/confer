/**
@author: Anant Bhardwaj
@date: Feb 12, 2012

All front-end magic happen through this code.
*/

//check for cache update

window.applicationCache.addEventListener('updateready', function(){
        window.applicationCache.swapCache();
        window.location.reload();
}, false);


// try to first load the data from localStorage 

/* Global Data */
var entities = JSON.parse(localStorage.getItem('entities'))
var sessions = JSON.parse(localStorage.getItem('sessions'))
var codes = JSON.parse(localStorage.getItem('codes'))
var offline_recs = JSON.parse(localStorage.getItem('offline_recs'))
var session_codes = JSON.parse(localStorage.getItem('session_codes'))
var acm_links = JSON.parse(localStorage.getItem('acm_links'))


/* Private Data */
var login_id = localStorage.getItem('login_id')
var login_name = localStorage.getItem('login_name')
var starred = JSON.parse(localStorage.getItem('starred'))
var s_starred = JSON.parse(localStorage.getItem('s_starred'))
var own_papers = JSON.parse(localStorage.getItem('own_papers'))
var recommended = JSON.parse(localStorage.getItem('recommended'))
var user_recs = JSON.parse(localStorage.getItem('user_recs'))




// contact the server if required
if(entities == null 
    || sessions == null 
    || codes == null 
    || session_codes == null
    || offline_recs == null
    || acm_links == null
    ){
    enable_alert('Downloading data for offline use. It might take some time.')
    console.log('contacting server')
    $.ajax({
        type: 'GET',
        async: false,
        url: '/data', 
        success: function(res) {

            if(res.error){
                 console.log('data/error')
                 window.location.href = '/login'            
            }      
            console.log('clearing local_storage')
            localStorage.clear()

            if(res.login_id != null){
                login_id = res.login_id
                localStorage.setItem('login_id', login_id)
            }

            if(res.login_name != null){
                login_name = res.login_name
                localStorage.setItem('login_name', login_name)
            }

            if(res.entities != null){
                entities = res.entities
                localStorage.setItem('entities', JSON.stringify(entities))
            }
            if(res.sessions != null){
                sessions = res.sessions
                localStorage.setItem('sessions', JSON.stringify(sessions))
            }
            if(res.recs != null){
                recommended = res.recs
                localStorage.setItem('recommended', JSON.stringify(recommended))
            }

            if(res.likes != null){
                starred  = res.likes
                localStorage.setItem('starred', JSON.stringify(starred))
            }


            if(res.s_likes != null){
                s_starred  = res.s_likes
                localStorage.setItem('s_starred', JSON.stringify(s_starred))
            }

            if(res.own_papers != null){
                own_papers = res.own_papers
                localStorage.setItem('own_papers', JSON.stringify(own_papers))
            }

            if(res.codes != null){
                codes = JSON.parse(res.codes)            
                localStorage.setItem('codes', res.codes)
            }

            if(res.session_codes!= null){
                session_codes = JSON.parse(res.session_codes)
                localStorage.setItem('session_codes', res.session_codes)
            }

            if(res.offline_recs!= null){
                offline_recs = JSON.parse(res.offline_recs)
                localStorage.setItem('offline_recs', res.offline_recs)
            }

            if(res.user_recs!= null){
                user_recs = res.user_recs
                localStorage.setItem('user_recs', JSON.stringify(res.user_recs))
            }

            if(res.acm_links!= null){
                acm_links = res.acm_links
                localStorage.setItem('acm_links', res.acm_links)
            }

            enable_alert('This device is ready for offline use.')

        }
    });
    
}


function refresh(_async_){
    if(!navigator.onLine){
        return
    }
    $.ajax({
        type: 'GET',
        async: _async_,
        url: '/refresh', 
        success: function(res) {
            if(!res.error){
                console.log("synced")               
                
                if(res.login_id!=null){
                    login_id = res.login_id
                    localStorage.setItem('login_id', login_id)
                }
                if(res.login_name != null){
                    login_name = res.login_name
                    localStorage.setItem('login_name', login_name)
                }
                if(res.recs!=null){
                    recommended = res.recs
                    localStorage.setItem('recommended', JSON.stringify(recommended))
                }
                if(res.likes != null){
                    starred = res.likes
                    localStorage.setItem('starred', JSON.stringify(starred))
                }
                if(res.s_likes != null){
                    s_starred = res.s_likes
                    localStorage.setItem('s_starred', JSON.stringify(s_starred))
                }
                if(res.user_recs != null){
                    user_recs = res.user_recs
                    localStorage.setItem('user_recs', JSON.stringify(user_recs))
                }
            }else{
                console.log('refresh/error')
                window.location.href = '/login'
            }
        }
    });
}


setInterval('refresh();', 60*1000)

refresh(false)

/* data structure for pending stars */

function refresh_pending(){
    var star_pending = JSON.parse(localStorage.getItem('star_pending'))
    var unstar_pending = JSON.parse(localStorage.getItem('unstar_pending'))
    var s_star_pending = JSON.parse(localStorage.getItem('s_star_pending'))
    var s_unstar_pending = JSON.parse(localStorage.getItem('s_unstar_pending'))

    if(star_pending == null){
        star_pending = []
        localStorage.setItem('star_pending', JSON.stringify(star_pending))
    }

    if(unstar_pending == null){
        unstar_pending = []
        localStorage.setItem('unstar_pending', JSON.stringify(unstar_pending))
    }

    if(s_star_pending == null){
        s_star_pending = []
        localStorage.setItem('s_star_pending', JSON.stringify(s_star_pending))
    }

    if(s_unstar_pending == null){
        s_unstar_pending = []
        localStorage.setItem('s_unstar_pending', JSON.stringify(s_unstar_pending))
    }
}


refresh_pending()




window.addEventListener("online", function() {
    enable_alert('You are online. Syncing new data with the server.')
    sync()
    refresh()
}, true);

 
window.addEventListener("offline", function() {
    enable_alert('You are offline. Any activities on this device would be synced when you come online.')
}, true);


function log(page){
    $.ajax({
        type:'GET',
        url:'/log/'+page, 
    });

}


function sync(){
    var star_pending = JSON.parse(localStorage.getItem('star_pending'))
    var unstar_pending = JSON.parse(localStorage.getItem('unstar_pending'))
    var s_star_pending = JSON.parse(localStorage.getItem('s_star_pending'))
    var s_unstar_pending = JSON.parse(localStorage.getItem('s_unstar_pending'))

    $.ajax({
        type:'POST',
        url:'/like/star',
        async: false, 
        data:{'papers': JSON.stringify(star_pending), 'session': JSON.stringify(s_star_pending)}, 
        success: function(res) {
            //console.log(res)
            recommended = res.recs
            starred = res.likes
            s_starred = res.s_likes
            if(recommended!=null)
                localStorage.setItem('recommended', JSON.stringify(recommended))
            if(starred!= null)
                localStorage.setItem('starred', JSON.stringify(starred))
            if(s_starred!=null)
                localStorage.setItem('s_starred', JSON.stringify(s_starred))

            star_pending = []    
            s_star_pending = []
            localStorage.setItem('star_pending', JSON.stringify(star_pending))
            localStorage.setItem('s_star_pending', JSON.stringify(s_star_pending))
    
        }
    });

    $.ajax({
        type:'POST',
        url:'/like/unstar',
        async: false, 
        data:{'papers': JSON.stringify(unstar_pending), 'session': JSON.stringify(s_unstar_pending)}, 
        success: function(res) {
            //console.log(res)
            recommended = res.recs
            starred = res.likes
            s_starred = res.s_likes
            if(recommended!=null)
                localStorage.setItem('recommended', JSON.stringify(recommended))
            if(starred!=null)
                localStorage.setItem('starred', JSON.stringify(starred))
            if(s_starred!=null)
                localStorage.setItem('s_starred', JSON.stringify(s_starred))
            unstar_pending = []
            s_unstar_pending = []
            localStorage.setItem('unstar_pending', JSON.stringify(unstar_pending))    
            localStorage.setItem('s_unstar_pending', JSON.stringify(s_unstar_pending))
        }
    });

    
}


// codes without video preview
var codeBlackList = [
  "KOP","PHN","NDL","LDJ","PQS","PLP","PLL","CYU","LRA","PQV","NNG","PMF","PSS","PSR","NEK","PKY",
  "PKS","PFS","PLJ","TRN","PBR","YQT","PKZ","PDS","PFR","SRJ","PHF","TUU","TZC","AZG","CZS","PQE",
  "GYU","GDG","NMX","PAK","YHY","PQQ","LLC","NPP","TXL","CZS","TLQ","GFL","TAU","NKQ","PTS","PKL",
  "GXS","SIA","PTU","PAE","PRH","PGG","LBR","PQZ","PTN","NGR","PEH","PGV","TGN","PSJ","PMY","NGN",
  "PQC","PPM","PCB","SRC","PDM","PSP","GZX","PKJ","PBM","PHR","SDC","CMU","LPA","PRN","GHQ","TEC",
  "PMR","PCD","NJT","AXZ","PEB","LSU","PMM","PMV","SGC","CMU","NHL","KSP","PKV","YYP","NFM","PTT",
  "NCK","PQG","KCL"
];

function detect_mobile() { 
 if(navigator.userAgent.match(/Android/i)
 || navigator.userAgent.match(/webOS/i)
 || navigator.userAgent.match(/iPhone/i)
 || navigator.userAgent.match(/iPad/i)
 || navigator.userAgent.match(/iPod/i)
 || navigator.userAgent.match(/BlackBerry/i)
 || navigator.userAgent.match(/Windows Phone/i)
 ){
    return true;
  } else {
    return false;
  }
}


jQuery.fn.highlight = function(pat) {
 function innerHighlight(node, pat) {
  var skip = 0;
  if (node.nodeType == 3) {
   var pos = node.data.toUpperCase().indexOf(pat);
   if (pos >= 0) {
    var spannode = document.createElement('span');
    spannode.className = 'text-highlight';
    var middlebit = node.splitText(pos);
    var endbit = middlebit.splitText(pat.length);
    var middleclone = middlebit.cloneNode(true);
    spannode.appendChild(middleclone);
    middlebit.parentNode.replaceChild(spannode, middlebit);
    skip = 1;
   }
  }
  else if (node.nodeType == 1 && node.childNodes && !/(script|style)/i.test(node.tagName)) {
   for (var i = 0; i < node.childNodes.length; ++i) {
    i += innerHighlight(node.childNodes[i], pat);
   }
  }
  return skip;
 }
 return this.each(function() {
  innerHighlight(this, pat.toUpperCase());
 });
};

jQuery.fn.removeHighlight = function() {
 return this.find("span.text-highlight").each(function() {
  this.parentNode.firstChild.nodeName;
  with (this.parentNode) {
   replaceChild(this.firstChild, this);
   normalize();
  }
 }).end();
};



function get_params() {
    var vars = [], hash;
    var hashes = window.location.href.slice(
    window.location.href.indexOf('?') + 1).split('&');
    for (var i = 0; i < hashes.length; i++) {
        hash = hashes[i].split('=');
        vars.push(hash[0]);
        vars[hash[0]] = hash[1];
    }
    return vars;
}


function get_hash() {
    if(window.location.href.indexOf('#') != -1)
        return window.location.href.slice(window.location.href.indexOf('#') + 1)
    else
        return window.location.href
}





Object.size = function(obj) {
    var size = 0, key;
    for (key in obj) {
        if (obj.hasOwnProperty(key)) size++;
    }
    return size;
};




function exists(recs, id){
    for(var r in recs){
        if(recs[r].id == id)
            return true
    }
    return false
}





function bind_events(){
    $("#headlink-right .mobile-nav").on('click',
        function(event){
          event.stopPropagation();
          $("#headlink-right a").toggleClass("toggle-nav");
        });
    $("#back-top a").click(function(){
      window.scrollTo(0,0);
    });

    $('.collapsible').off('click')
    $('.collapsible').on('click',
        function(event){
            event.stopPropagation();
            var target = $(this).attr("data")
            //console.log(target)
            $('#'+ target).toggle();
            if($('#'+target).is(':visible')){
                //$(this).find('.arrow').html('▾');
                $(this).find('.arrow').removeClass("arrow-right").addClass("arrow-down");
            }else{
                //$(this).find('.arrow').html('▸');
                $(this).find('.arrow').removeClass("arrow-down").addClass("arrow-right");
            }
        });

    $('.session-collapsible').off('click')
    $('.session-collapsible').on('click',
        function(event){
            enable_loading("opening a session...");
            event.stopPropagation();
            var s = $(this).parents('div.session:first')
            s.find('.paper-container').toggle();
            if(s.find('.paper-container').is(':visible')){
                s.find('.arrow').removeClass("arrow-right").addClass("arrow-down");
            }else{
                s.find('.arrow').removeClass("arrow-down").addClass("arrow-right");
            }
            disable_loading();
        });

    $('input:text').addClass('default-search-text')
    $('input:text').each(function(){
        if($(this).attr("title") == null || $(this).attr("title") == ''){
            $(this).attr("title", 'Enter paper titles, authors, or keywords')
        }
    });

  
    $(".default-search-text").focus(
        function() {
        if ($(this).val() == $(this).attr("title")) {
            $(this).removeClass("default-search-text-active");
            $(this).val("");
        }
    });



    
    $(".default-search-text").blur(
        function() {
        if ($(this).val() == "") {
            $(this).addClass("default-search-text-active");
            $(this).val($(this).attr("title"));
        }
    });

    $('input:text').each(function(){
        if( $(this).val() == '' || $(this).val() == $(this).attr("title")){
            $(this).blur()
        }else{
            $(this).focus()
        }
    });

    $("#refresh_recommendations").off('click')
    $("#refresh_recommendations").on('click', function(event){
        event.stopImmediatePropagation();

        refresh_recommendations()
    })

    $("#export_bibtex").off('click')
    $("#export_bibtex").on('click', function(event){
        event.stopImmediatePropagation();
    })

    $('.acm-icon').off('click')
    $('.acm-icon').on('click', function(){
        log('acm_link_' + $(this).attr('data'))
    })
    
    if(detect_mobile()){
        $("body").addClass("touch-device");
        /*

        var needs_scroll_update = false;
        $(document).scroll(function(){
            if(needs_scroll_update) {
                setTimeout(function() {
                    $("body").css("height", "+=1").css("height", "-=1");
                }, 0);
            }
        });
        $("input:text").live("focus", function(e) {
            needs_scroll_update = true;
        });

        $("input:text").live("blur", function(e) {
            needs_scroll_update = false;
        });

        */

        $('#search_papers').keyup(function(event){
            var str = $(this).val()
            if(str==""){
                reset_all_papers()
                $('#show_papers').show();
            }else{
                $('#show_papers').hide();
            }
            
        });


        $('#search_session').keyup(function(event){
            var str = $(this).val()
            if(str==""){
                reset_sessions()
                apply_filters()
            }
        });

        $('#search_sessions_btn').off('click')
        $('#search_sessions_btn').on('click', function(event){
                var str = $('#search_session').val()
                delay('simple_search_session("'+str+'");', 0);
            });


        $('#search_papers_btn').off('click')
        $('#search_papers_btn').on('click', function(event){
            var str = $('#search_papers').val()
            delay('simple_search_papers("'+str+'");', 0);
        });

        
    }else{
        $("body").addClass("no-touch-device");
        $('#search_session').keyup(function(event){
            var str = $(this).val()
            delay('search_session("'+str+'");', 300);
        });


        $('#search_papers').keyup(function(event){
            var str = $(this).val()
            if(str==""){
                $('#show_papers').show();
            }else{
                $('#show_papers').hide();
            }
            delay('search_papers("'+str+'");', 300);
        });
        

        $('#search_sessions_btn').off('click')
        $('#search_sessions_btn').on('click', function(event){
                var str = $('#search_session').val()
                delay('search_session("'+str+'");', 0);
            });


        $('#search_papers_btn').off('click')
        $('#search_papers_btn').on('click', function(event){
            var str = $('#search_papers').val()
            delay('search_papers("'+str+'");', 0);
        });
        

    }
    
   

    

    $('#show_likes').on('click', function(){
        if($("#likes tr:visible").length > 2){
                $("#likes tr:gt(1)").hide()
                $("#show_likes").html('Show All')
        }else{
                $("#likes tr").show()
                $("#show_likes").html('Show Less')
        }
        update_likes_count();         
    });
    

    $('#show_recs').on('click', function(){
        var n = $('#recs tr:visible').length
        if((n+5) < $("#recs tr").length){
            $('#recs tr:lt('+(n+5)+')').show()               
        }else{
            $("#recs tr").show()
            $("#show_recs").hide()
        }
        update_recs_count();         
    });
    

    $('#show_papers').on('click', function(){
        var n = $('#all_papers tr:visible').length
        if((n+25) < $("#all_papers tr").length){
            $('#all_papers tr:lt('+(n+25)+')').show()               
        }else{
            $("#all_papers tr").show()
            $("#show_papers").hide()
        }
        update_papers_count();         
    });

    $('#show_filters').on('click', function(){
      if ($(this).hasClass("expanded")){
        $(".more-filters").hide();
        $(this).text("Show More Filters");
        $(this).removeClass("expanded");
      } else {
        $(".more-filters").show();
        $(this).text("Show Less Filters");
        $(this).addClass("expanded");
      }

    });

    $('.send_tweet').on('click', function(event){
        event.stopPropagation();
        var id = $(this).parents("tr.paper").first().attr("data");
        var url = "http://mychi.csail.mit.edu/paper#" + id;
        //var title = $(this).siblings("a").text();
        var title = entities[id].title;
        var message = "Looking forward to seeing \"" + remove_special_chars(title) + "\""; 
        window.open ("https://twitter.com/share?" + 
            "url=" + encodeURIComponent(url) + 
            "&counturl=" + encodeURIComponent(url) +
            "&text=" + encodeURIComponent(message) + 
            "&hashtags=" + encodeURIComponent('chi2013') + 
            "&via=" + encodeURIComponent('mychi2013'), 
            "twitter", "width=500,height=300");
    });

    $('.send_session_tweet').on('click', function(event){
        event.stopPropagation();
        var id = $(this).parents(".session").first().attr("data");
        var url = document.location;
        //var title = $(this).siblings(".session-title").text();
        var title = sessions[id].s_title;
        var message = "Looking forward to seeing \"" + remove_special_chars(title) + "\" " + sessions[id].date + " | " + sessions[id].time + " | " + sessions[id].room;
        window.open ("https://twitter.com/share?" + 
            //"url=" + encodeURIComponent(url) + 
            //"&counturl=" + encodeURIComponent(url) +
            "&text=" + encodeURIComponent(message) + 
            "&hashtags=" + encodeURIComponent('chi2013') + 
            "&via=" + encodeURIComponent('mychi2013'), 
            "twitter", "width=500,height=300");
    });

    $('.send_email').on('click', function(event){
        event.stopPropagation();
        var id = $(this).parents("tr.paper").first().attr("data");
        var url = "http://mychi.csail.mit.edu/paper#" + id;
        var title = remove_special_chars(entities[id].title);
        var message = "Hi there!\n\nI found this interesting paper at CHI 2013 that you may be interested in:\n"
          + title + "\n" + url;
        var link = "mailto:";
        //var link = "<a id='email-link' href='mailto:";
        link += "?to=&subject=" + encodeURIComponent("Paper at CHI2013: " + title);
        link += "&body=" + encodeURIComponent(message);
        //var link = $(link); 
        //link.appendTo("#page");
        //$("#email-link").trigger("click");//.remove();
        window.location.href = link;
    });


    $('.send_session_email').on('click', function(event){
        event.stopPropagation();
        var id = $(this).parents(".session").first().attr("data");
        var url = document.location;
        var title = remove_special_chars(sessions[id].s_title);
        var message = "Hi there!\n\nI found this interesting session at CHI 2013 that you may be interested in:\n"
          + title + "\n" + url + "\n" + sessions[id].date + " | " + sessions[id].time + " | " + sessions[id].room;
        var link = "mailto:";
        //var link = "<a id='email-link' href='mailto:";
        link += "?to=&subject=" + encodeURIComponent("Session at CHI2013: " + title);
        link += "&body=" + encodeURIComponent(message);
        //var link = $(link); 
        //link.appendTo("#page");
        //$("#email-link").trigger("click");//.remove();
        window.location.href = link;
    });
}



var delay = (function(){
  var timer = 0;
  return function(callback, ms){
    clearTimeout (timer);
    timer = setTimeout(callback, ms);
  };
})();




function search_session(str){
    //$('.filter').removeClass('active')
    //$('.f_all').addClass('active')
    reset_sessions()
    apply_filters()
    if(str=="" || str == $('#search_session').attr("title")){        
        return
    }
    var regex_str = ''
    var words = str.split(' ')
    for (var i=0;i<words.length; i++){
        regex_str += '(?=.*\\b'+words[i]+'.*\\b)'
    }
    var s =  new RegExp(regex_str , 'i')
    $('.session:visible').each(function(){
        $(this).parent().prev().hide()
    });

      
    $('.session:visible').each(function(){
        if(s.test($(this).text())){
            $(this).show()   
            var p = $(this).attr("data")
            $("#"+p).show()
            $(this).find('.arrow').removeClass("arrow-right").addClass("arrow-down");
            $(this).highlight(str);
            //$(this).text().indexOf(str)        
        }else{
            $(this).hide()
            var p = $(this).attr("data")
            $("#"+p).hide()
            $(this).find('.arrow').removeClass("arrow-down").addClass("arrow-right");

        }

    });

    $('.session:visible').each(function(){
        $(this).parent().prev().show()
        
    });
    
    update_sessions_count(); 
    
}


function simple_search_session(str){

    reset_sessions()
    apply_filters()
    if(str=="" || str == $('#search_session').attr("title")){        
        return
    }
    
    $('.session:visible').each(function(){
        $(this).parent().prev().hide()
    });

       
    $('.session').each(function(){
        if($(this).text().toLowerCase().indexOf(str.toLowerCase())!=-1){
            $(this).show()            
        }else{
            $(this).hide()
        }

    });

    $('.session:visible').each(function(){
        $(this).parent().prev().show()
        $('.session .paper').show()
    });
    update_sessions_count(); 
    
}

function search_papers(str){
    if(str==""){
        reset_all_papers()
        return
    }
    var regex_str = ''
    var words = str.split(' ')
    for (var i=0;i<words.length; i++){
        regex_str += '(?=.*\\b'+words[i]+'.*\\b)'
    }
    var s =  new RegExp(regex_str , 'i')
    
    //console.log(s)
       
    $('#all_papers .paper').each(function(){
        if(s.test($(this).text())){
            $(this).show()
            
        }else{
            $(this).hide()
        }

    });
    
    
    update_papers_visible_count(); 
}


function simple_search_papers(str){
   
       
    $('#all_papers .paper').each(function(){
        if($(this).text().toLowerCase().indexOf(str.toLowerCase())!= -1){
            $(this).show()
            
        }else{
            $(this).hide()
        }

    });
    

   

    update_papers_visible_count(); 
}




function refresh_recommendations(){
    populate_recs(recommended)
    update_recs(recommended)
}








function remove_special_chars(str){
    if (str == null || str == "null")
      return "";
    var result = str;
    result = result.replace(/¬/g, "-"); 
    result = result.replace(/×/g, "x"); 
    result = result.replace(/–/g, "-"); 
    result = result.replace(/‘/g, "'"); 
    result = result.replace(/’/g, "'"); 
    result = result.replace(/“/g, "\""); 
    result = result.replace(/”/g, "\""); 
    result = result.replace(/\\"/g, "\""); 
    result = result.replace(/â€”/g, "-");
    result = result.replace(/â€"/g, "-");
    result = result.replace(/â€˜/g, "'");
    result = result.replace(/â€œ/g, "\"");
    result = result.replace(/â€/g, "\"");
    result = result.replace(/Ã©/g, "é");
    result = result.replace(/\\u2013/g, "-");
    result = result.replace(/\\u00ac/g, "-");
    result = result.replace(/\\u2014/g, "-");
    result = result.replace(/\\u2018/g, "'");
    result = result.replace(/\\u2019/g, "'");
    result = result.replace(/\\u2022/g, "*");
    result = result.replace(/\\u201c/g, "\"");
    result = result.replace(/\\u201d/g, "\"");
    result = result.replace(/â€™/g, "'");
    result = result.replace(/â€“/g, "-");
    result = result.replace(/™/g, "(TM)"); 
    result = result.replace(/\\\//g, "/"); 
    result = result.replace(/\\/g, ""); 
    result = result.replace(/\\ \\/g, ""); 
    return result;
}




function format_venue(venue){
  if (venue == "paper")
    return "Paper";
  if (venue == "SIG")
    return "SIG Meeting";
  if (venue == "altchi")
    return "alt.chi";
  if (venue == "course")
    return "Course";
  if (venue == "casestudy")
    return "Case Study";
  if (venue == "panel")
    return "Panel";
  return venue;
}





function get_communities(s){
    var communities = []
    if (s.communities){
        communities = s.communities
    }
    for(var i in s.submissions){
        s_communities = entities[s.submissions[i]].communities
        for(var j in s_communities){
            if(communities.indexOf(s_communities[j]) == -1){
                communities.push(s_communities[j])
            }
        }
    }
    return communities.join(' ');

}

function get_short_session_info_of_paper(id){
  var result = "";
  var session = sessions[entities[id].session];
  var date = "";
  if (session.date == "Monday")
    date = "Mon";
  if (typeof session !== "undefined"){
    result += session.date.substring(0,3) + " " + session.time.substr(0,5) + " | " + session.room + " | " + session.s_title;
  }
  return result;
}

function get_session_info_of_paper(id){
  var result = "";
  var session = sessions[entities[id].session];
  if (typeof session !== "undefined"){
    result += session.date + " | " + session.time + " | " + session.room + " | " + session.s_title;
  }
  return result;
}


function get_paper_subtype(id){
    var subtype = "";
    if (typeof entities[id] !== "undefined" && entities[id].subtype != "")
      subtype = entities[id].subtype;
    else if (id.indexOf("tochi") > -1)
      subtype = "TOCHI";
    else {
      var session = sessions[entities[id].session];
      if (typeof session !== "undefined")
        subtype = format_venue(session.venue);
    }
    return "- " + subtype;
}

function codeExists(code){
  // if the given code has no video preview return false
  if ($.inArray(code, codeBlackList) > -1)
    return false;
  return true;

}


function select_paper(id){
    if(window.location.pathname == '/paper'){
        window.location.hash = "#" + id;
        window.location.reload(false);
    }else{
        window.location.href = '/paper#'+id
    }
    window.scrollTo(0,0)
}

function isMyPaper(id){
  if ($.inArray(id, own_papers) > -1)
    return true;
  return false;
}


function get_paper_html(id){
    if(entities[id] == null)
        return ''
    var communities = get_communities(entities[id]);
    var raw_html = '<tr data= "' + id + '" class="clickable paper ' + id
    if(exists(recommended, id)){
        raw_html += ' recommended'
    }
    if(starred.indexOf(id) >= 0){
        raw_html += ' highlight'
    }
    if(entities[id].hm){
        raw_html += ' p_hm'
    }
    if(entities[id].award){
        raw_html += ' p_award'
    }
    if(communities != "")
      raw_html += ' communities'
    raw_html += '">'
      
    raw_html += '<td class="metadata">'   
    if(starred.indexOf(id) < 0){
        raw_html += '<div class="star star-open p_star" data="'+ id + '" onclick="handle_star(event);">'        
    }else{
        raw_html += '<div class="star star-filled p_star" data="'+ id + '" onclick="handle_star(event);">'       
    }
    raw_html += '</div>'
    
    raw_html += '</td>'
    
    raw_html += '<td class="content">'    
    raw_html += '<ul>'

    raw_html += '<li class="paper-title"><h3><span class="link" onclick=select_paper("'+id+'")>'+remove_special_chars(entities[id].title) +'</span>'
    raw_html += '<span class="paper-subtype">' + ' ' + get_paper_subtype(id) + '</span>'
    if(acm_links[id]!=null){
        var url = acm_links[id]['url']
        raw_html += '<a href="' + url +'" target="_blank"><span class="acm-icon" data="'+ id + '"></span></a>'
    }
    raw_html += '<span class="paper-code">' +  ' ' + codes['code'][id] + '</span>'
    //raw_html += '<span class="paper-session">' + get_short_session_info_of_paper(id) + '</span>'
    /*
    if (codeExists(codes['code'][id]))
      raw_html += '<span class="video-url"><a href="http://chischedule.org/2013/'+codes['code'][id]+'" target="_blank"><span class="play-icon"></span></a></span>'
    
    */
    
    
    raw_html += '<span class="send_tweet"></span>'
    raw_html += '<span class="send_email"></span>'
    raw_html += '</h3>'
    raw_html += '</li>'


    raw_html += '<li class="paper-authors">'
    for(author in entities[id].authors){
        if(entities[id].authors[author] != null){
            raw_html += ' ' + entities[id].authors[author].givenName + ' ' + entities[id].authors[author].familyName + '&nbsp;&nbsp;&nbsp;&nbsp;'
        }
    }
    raw_html += '</li>'
      
    raw_html += '<li class="paper-icons"><span class="award-icon"></span><span class="hm-icon"></span>'
    if (isMyPaper(id))
      raw_html += '<span class="own-icon">my paper</span>'
    raw_html += '<span class="rec-icon">recommended</span>'
    if (communities != ""){
      $.each(entities[id].communities, function(i, v){
        raw_html += '<span class="community-icon ' + v + '">' + v + '</span>'
      });
    }
    raw_html += '</li>'
    if (entities[id].c_and_b == "null")
      raw_html += '<li class="paper-cb">'+ remove_special_chars(entities[id].abstract) + '</li>'
    else
      raw_html += '<li class="paper-cb">'+ remove_special_chars(entities[id].c_and_b) + '</li>'
        
    raw_html += '<li class="paper-keywords">' + remove_special_chars(entities[id].keywords) + '</li>'
    raw_html += '</ul>'
    raw_html += '</td>'
    
    raw_html += '</tr>'

    return raw_html
}


function getSpecialSessionCode(id){
  var special_session_codes = {"s300":"LRA",
  "s302":"SIA",
  "s325":"IWC",
  "s305":"SRC",
  "s301":"LPA",
  "s306":"SDC",
  "s307":"SGC"};
  return special_session_codes[id];
}




function get_session_html(id){
    var communities = get_communities(sessions[id]);
    var communities_class = (communities == "") ? "" : " communities";
    var award=''
    if(sessions[id].award || sessions[id].hm){
        award = 's_awardhm'
    }
    if(sessions[id].award){
        award += ' s_award'
    }
    if(sessions[id].award || sessions[id].hm){
        award += ' s_hm'
    }
    var raw_html = '<div class="session ' + id + ' ' + sessions[id].date + ' t' + sessions[id].time.substr(0,2) + ' '
              + sessions[id].venue + ' ' + sessions[id].personas.substr(0,2) + ' '
              + communities_class + ' ' + communities + ' ' + award + '" data="' + id + '">'
    raw_html += '<table class="session-container session-collapsible" data="' + id + '"><tr class="clickable">'
    
    raw_html += '<td class="metadata">'     
    //raw_html += '<div class="ui-state-default ui-corner-all s_star" data="'+ id + '" onclick="handle_session_star(event);">'
    raw_html += '<div class="star star-open s_star" data="'+ id + '" onclick="handle_session_star(event);">'
    //raw_html += '<span class="ui-icon ui-icon-star"></span>'
    raw_html += '</div>'        
    raw_html += '</td>'
    
    raw_html += '<td class="content">'  
    raw_html += '<ul>'
    raw_html += '<li><h3><span class="arrow arrow-right"></span> <span class="session-title">'+ remove_special_chars(sessions[id].s_title) + '</span>'
   
    var s_code = session_codes['id'][id];
    if (typeof s_code !== "undefined" && typeof codes['code'][s_code] !== "undefined"){
      raw_html += '<span class="session-code">' + codes['code'][s_code] + '</span>'
      //if (codeExists(codes['code'][s_code]))
      //  raw_html += '<span class="video-url"><a href="http://chischedule.org/2013/'+codes['code'][s_code]+'" target="_blank"><span class="play-icon"></span></a></span>'
    } else if (sessions[id].venue == "panel" || sessions[id].venue == "course" || sessions[id].venue == "SIG"){
      var p_id = sessions[id].submissions[0];
      if (typeof p_id !== "undefined"){
        raw_html += '<span class="session-code">' +  ' ' + codes['code'][p_id] + '</span>'
        /*
        if (codeExists(codes['code'][p_id]))
          raw_html += '<span class="video-url"><a href="http://chischedule.org/2013/'+codes['code'][p_id]+'" target="_blank"><span class="play-icon"></span></a></span>'
        */
      }
    } else if (typeof getSpecialSessionCode(id) !== "undefined"){
      var code = getSpecialSessionCode(id);
      if (typeof code !== "undefined"){
        raw_html += '<span class="session-code">' +  ' ' + code + '</span>'
        /*
        if (codeExists(code))
          raw_html += '<span class="video-url"><a href="http://chischedule.org/2013/'+code+'" target="_blank"><span class="play-icon"></span></a></span>'
        */
      }
    }
    raw_html += '<span class="send_session_tweet"></span>'
    raw_html += '<span class="send_session_email"></span>'
    raw_html += '</h3></li>'
    raw_html += '<li class="session-icons"><span class="award-icon"></span><span class="hm-icon"></span><span class="rec-icon">recommended</span>'

    if (communities != ""){
      $.each(sessions[id].communities, function(i, v){
        raw_html += '<span class="community-icon ' + v + '">' + v + '</span>'
      });
    }
    
    raw_html += '</li>';
    raw_html += '<li class="session-info"><span class="session-venue">' + format_venue(sessions[id].venue) + '</span> <span class="session-room">Room: ' + sessions[id].room + '</span></li>'
    raw_html += '</ul>'

    
    raw_html += '<div class="timeline">'
    var size = sessions[id].submissions.length
    var weight = []
    var sum = 0
    for(i=0; i<size; i++){
        if(entities[sessions[id].submissions[i]].subtype == 'Note'){
            weight[i] = 0.5
        }else{
            weight[i] = 1.0
        }
        sum += weight[i]
    }
    
    for(var i=0; i< size; i++){
        var w = 100*(weight[i]/sum)
        raw_html += '<div style="width:' + w + '%;"></div>'
    }
    raw_html += '</div>'
    raw_html += '</td>'
    
    raw_html += '</tr>'
    raw_html += '</table>'
    raw_html += '<table id="' +id +'" class="paper-container" style="display:none; padding-left:20px;">'
    for(var i in sessions[id].submissions){        
        raw_html += get_paper_html(sessions[id].submissions[i]);        
    }
    raw_html += '</table>'
    raw_html += '</div>'
    return raw_html
}



function get_selected_paper_html(id){
    if(entities[id] == null)
      return null
    var communities = get_communities(entities[id]);


    raw_html += '<tbody>'
    var raw_html = '<tr data= "' + id + '" class="paper ' + id
    if(exists(recommended, id)){
        raw_html += ' recommended'
    }
    if(starred.indexOf(id) >= 0){
        raw_html += ' highlight'
    }
    if(entities[id].hm){
        raw_html += ' p_hm'
    }
    if(entities[id].award){
        raw_html += ' p_award'
    }
    if(communities != ""){
      raw_html += ' communities';
    }
    raw_html += '">'


    raw_html += '<td class="metadata">'   
    if(starred.indexOf(id) == -1){
        raw_html += '<div class="star star-open p_star" data="'+ id + '" onclick="handle_star(event);">'        
    }else{
        raw_html += '<div class="star star-filled p_star" data="'+ id + '" onclick="handle_star(event);">'       
    }
    raw_html += '</div>'
    
    raw_html += '</td>'
    
    raw_html += '<td class="content">'    
    raw_html += '<ul>'



    raw_html += '<h3>' + remove_special_chars(entities[id].title) 
    raw_html += '<span class="paper-subtype">' + get_paper_subtype(id) + '</span>'
    if(acm_links[id]!=null){
        var url = acm_links[id]['url']
        raw_html += '<a href="' + url +'" target="_blank"><span class="acm-icon" data="'+ id + '"></span></a>'
    }
    raw_html += '<span class="paper-code">' + codes['code'][id] + '</span>'
    /*
    if (codeExists(codes['code'][id]))
      raw_html += '<span class="video-url"><a href="http://chischedule.org/2013/'+codes['code'][id]+'" target="_blank"><span class="play-icon"></span></a></span>'
    */
    raw_html += '<span class="send_tweet"></span>'
    raw_html += '<span class="send_email"></span>'
    raw_html += '</h3>';

    raw_html += '<li class="paper-authors">'
    for(var author in entities[id].authors){
        if(entities[id].authors[author] != null){
          //console.log(entities[id]);
            //raw_html += entities[id].authors[author].givenName + ' ' + entities[id].authors[author].familyName + '&nbsp;&nbsp;&nbsp;&nbsp;'
            raw_html += '<span class="author"><span class="author-name">' 
                    + entities[id].authors[author].givenName + ' ' + entities[id].authors[author].familyName 
                    + '</span>';
            var affiliation = entities[id].authors[author].primary; 
            if (typeof affiliation !== "undefined" && affiliation != null && typeof affiliation.institution !== "undefined" && affiliation.institution != null && typeof affiliation.country !== "undefined" 
&& affiliation.country != null)
            raw_html += '<span class="author-affiliation">'
                    + affiliation.institution + ', ' + affiliation.country 
                    + '</span>';
            raw_html += '</span>';
        }
    }
    raw_html += '</li>'
    
    raw_html += '<li class="paper-icons"><span class="award-icon"></span><span class="hm-icon"></span>'
    if (isMyPaper(id))
      raw_html += '<span class="own-icon">my paper</span>'
    raw_html += '<span class="rec-icon">recommended</span>'
    if (communities != ""){
      $.each(entities[id].communities, function(i, v){
        raw_html += '<span class="community-icon ' + v + '">' + v + '</span>'
      });
    }
    raw_html += '</li>'
    raw_html += '<li class="paper-selected-session">' + get_session_info_of_paper(id) + '</li>'
    raw_html += '<hr />'
    raw_html += '<li>' + remove_special_chars(entities[id].abstract) + '</li>'
    raw_html += '<li class="paper-keywords">' + remove_special_chars(entities[id].keywords) + '</li>'
    raw_html += '</ul>'
    raw_html += '</td>'
    raw_html += '</tr>'
    raw_html += '</tbody>'
    raw_html += '</table>'
    return raw_html
}




function place_session(s){
    if(s.hasClass('Monday')){
        if(s.hasClass('t09')){
            $("#Mondayt09").append(s)
            $("#Mondayt09").prev().show()
        }else if(s.hasClass('t11')){
            $("#Mondayt11").append(s)
            $("#Mondayt11").prev().show()
        }else if(s.hasClass('t14')){
            $("#Mondayt14").append(s)
            $("#Mondayt14").prev().show()
        }else if(s.hasClass('t16')){
            $("#Mondayt16").append(s)
            $("#Mondayt16").prev().show()
        }

    }else if(s.hasClass('Tuesday')){
        if(s.hasClass('t09')){
            $("#Tuesdayt09").append(s)
            $("#Tuesdayt09").prev().show()
        }else if(s.hasClass('t11')){
            $("#Tuesdayt11").append(s)
            $("#Tuesdayt11").prev().show()
        }else if(s.hasClass('t14')){
            $("#Tuesdayt14").append(s)
            $("#Tuesdayt14").prev().show()
        }else if(s.hasClass('t16')){
            $("#Tuesdayt16").append(s)
            $("#Tuesdayt16").prev().show()
        }

    }else if(s.hasClass('Wednesday')){
        if(s.hasClass('t09')){
            $("#Wednesdayt09").append(s)
            $("#Wednesdayt09").prev().show()
        }else if(s.hasClass('t11')){
            $("#Wednesdayt11").append(s)
            $("#Wednesdayt11").prev().show()
        }else if(s.hasClass('t14')){
            $("#Wednesdayt14").append(s)
            $("#Wednesdayt14").prev().show()
        }else if(s.hasClass('t16')){
            $("#Wednesdayt16").append(s)
            $("#Wednesdayt16").prev().show()
        }

    }else if(s.hasClass('Thursday')){
        if(s.hasClass('t09')){
            $("#Thursdayt09").append(s)
            $("#Thursdayt09").prev().show()
        }else if(s.hasClass('t11')){
            $("#Thursdayt11").append(s)
            $("#Thursdayt11").prev().show()
        }else if(s.hasClass('t14')){
            $("#Thursdayt14").append(s)
            $("#Thursdayt14").prev().show()
        }else if(s.hasClass('t16')){
            $("#Thursdayt16").append(s)
            $("#Thursdayt16").prev().show()
        }

    }
}


function update_session_view(){
    $( ".session" ).each(function(s_index) {
        var session = $(this)
        $(this).find('.paper-container').find('.star').each(function(p_index){
            if($(this).hasClass('star-filled')){
                session.find('.timeline').children("div").eq(p_index).addClass("filled_yellow");
            }else{
                session.find('.timeline').children("div").eq(p_index).removeClass("filled_yellow");                  
            }
                        

        });

        $(this).find('.paper-container tr').each(function(p_index){
            if($(this).hasClass('recommended')){
                session.addClass('p_recommended')
                session.find('.timeline').children("div").eq(p_index).addClass("filled_blue");
            }else{                
                session.find('.timeline').children("div").eq(p_index).removeClass("filled_blue");
            }               

        });

        
        
        if($(this).find('.paper-container').find('.recommended').length > 0){
            $(this).find('.session-container').find('tr').addClass('recommended')
            session.addClass('s_recommended')
        }else{
            $(this).find('.session-container').find('tr').removeClass('recommended')
            session.removeClass('s_recommended')
        }
       
        if($(this).find('.paper-container').find('.star-filled').length > 0){
              $(this).find('.session-container').find('.star').removeClass('star-open').addClass('star-filled')
              $(this).find('.session-container').find('tr').addClass('highlight')
              session.addClass('s_starred')
        }else{
            $(this).find('.session-container').find('.star').removeClass('star-filled').addClass('star-open')
            $(this).find('.session-container').find('tr').removeClass('highlight')
            session.removeClass('s_starred')
        }
        
    });
    
    for(var s in s_starred){
        $('.session.'+s_starred[s]).find('.session-container').find('.star').removeClass('star-open').addClass('star-filled')
        $('.session.'+s_starred[s]).addClass('s_starred')
    }

    update_sessions_count();
}


function update_recs(){
      $('.paper').removeClass('recommended')
      for(var r in recommended){
            $('.'+recommended[r].id).each(function(){
                $(this).addClass('recommended')
            });
      }

}


function add_pending_unstar(paper_id){
    var star_pending = JSON.parse(localStorage.getItem('star_pending'))
    var unstar_pending = JSON.parse(localStorage.getItem('unstar_pending'))
    var i =  star_pending.indexOf(paper_id)
    if( i == -1){
        unstar_pending.push(paper_id)
    }else{
        star_pending.splice(i, 1)
    }
    localStorage.setItem('star_pending', JSON.stringify(star_pending))
    localStorage.setItem('unstar_pending', JSON.stringify(unstar_pending))
}



function add_pending_star(paper_id){
    var star_pending = JSON.parse(localStorage.getItem('star_pending'))
    var unstar_pending = JSON.parse(localStorage.getItem('unstar_pending'))
    var i =  unstar_pending.indexOf(paper_id)
    if( i == -1){
        star_pending.push(paper_id)
    }else{
        unstar_pending.splice(i, 1)
    }
    localStorage.setItem('star_pending', JSON.stringify(star_pending))
    localStorage.setItem('unstar_pending', JSON.stringify(unstar_pending))
}



function add_pending_s_unstar(session_id){
    var s_star_pending = JSON.parse(localStorage.getItem('s_star_pending'))
    var s_unstar_pending = JSON.parse(localStorage.getItem('s_unstar_pending'))
    var i =  s_star_pending.indexOf(session_id)
    if( i == -1){
        s_unstar_pending.push(session_id)
    }else{
        s_star_pending.splice(i, 1)
    }
    localStorage.setItem('s_star_pending', JSON.stringify(s_star_pending))
    localStorage.setItem('s_unstar_pending', JSON.stringify(s_unstar_pending))
}



function add_pending_s_star(session_id){
    var s_star_pending = JSON.parse(localStorage.getItem('s_star_pending'))
    var s_unstar_pending = JSON.parse(localStorage.getItem('s_unstar_pending'))
    var i =  s_unstar_pending.indexOf(session_id)
    if( i == -1){
        s_star_pending.push(session_id)
    }else{
        s_unstar_pending.splice(i, 1)
    }
    localStorage.setItem('s_star_pending', JSON.stringify(s_star_pending))
    localStorage.setItem('s_unstar_pending', JSON.stringify(s_unstar_pending))
}




function handle_session_star(event){
    enable_alert("updating information..."); 
    event.stopPropagation();
    var obj = $(event.target).parents("td:first").find('.s_star')
    var session_id = obj.attr("data")
    var papers = sessions[session_id]['submissions']
    //console.log(papers)
    if(obj.hasClass('star-filled')){
        $('.'+obj.attr('data')).each(function(){
            $(this).find('.p_star').removeClass('star-filled').addClass('star-open')
            $(this).find('.paper').removeClass('highlight')
        })
        if(!navigator.onLine){
            enable_alert("You unliked a session. You are not online -- updating information locally.");
            for(var paper_id in papers){
                var i =  starred.indexOf(papers[paper_id])
                starred.splice(i, 1)
                add_pending_unstar(papers[paper_id])
            }
            var s_id = s_starred.indexOf(session_id)
            s_starred.splice(s_id, 1)
            add_pending_s_unstar(session_id)
            localStorage.setItem('starred', JSON.stringify(starred))
            localStorage.setItem('s_starred', JSON.stringify(s_starred))
            update_session_view()
            apply_filters()
        }else{
            $.post('/like/unstar', {'papers': JSON.stringify(papers), 'session': JSON.stringify([session_id])}, function(res) {
                for(var paper_id in papers){
                    var i =  starred.indexOf(papers[paper_id])
                    starred.splice(i, 1)                    
                }
                var s_id = s_starred.indexOf(session_id)
                s_starred.splice(s_id, 1)
                $('.'+obj.attr('data')).each(function(){
                    $(this).find('.p_star').removeClass('star-filled').addClass('star-open')
                    $(this).find('.paper').removeClass('highlight')
                })
                starred = res.likes
                s_starred = res.s_likes
                recommended = res.recs
                localStorage.setItem('starred', JSON.stringify(starred))
                localStorage.setItem('s_starred', JSON.stringify(s_starred))
                localStorage.setItem('recommended', JSON.stringify(recommended))
                update_recs()
                update_session_view()
                apply_filters()
            })
            .done(function(){
                enable_alert("You unliked a session.");
            });
        }
       
    }else{
        $('.'+obj.attr('data')).each(function(){
            $(this).find('.p_star').removeClass('star-open').addClass('star-filled')
            $(this).find('.paper').addClass('highlight')
            update_session_view()
            apply_filters()
        })
        if(!navigator.onLine){
            enable_alert("You liked a session. You are not online -- updating information locally.");
            for(var paper_id in papers){
                starred.push(papers[paper_id])
                add_pending_star(papers[paper_id])
            }
            s_starred.push(session_id)
            add_pending_s_star(session_id)
            localStorage.setItem('starred', JSON.stringify(starred))
            localStorage.setItem('s_starred', JSON.stringify(s_starred))
        }else{
            $.post('/like/star', {'papers': JSON.stringify(papers), 'session': JSON.stringify([session_id])}, function(res) {
                for(var paper_id in papers){
                    starred.push(papers[paper_id])
                }
                s_starred.push(session_id)
                $('.'+obj.attr('data')).each(function(){
                    $(this).find('.p_star').removeClass('star-open').addClass('star-filled')
                    $(this).find('.paper').addClass('highlight')
                })
                starred = res.likes
                s_starred = res.s_likes
                recommended = res.recs
                localStorage.setItem('starred', JSON.stringify(starred))
                localStorage.setItem('s_starred', JSON.stringify(s_starred))
                localStorage.setItem('recommended', JSON.stringify(recommended))
                update_recs()
                update_session_view()
                apply_filters()
            })
            .done(function(){
                enable_alert("You liked a session.");
            });
        }
        
    }
    


}



function handle_star(event){ 
    //$("#refresh_recommendations").show();
    enable_alert("updating information..."); 
    var obj = $(event.target).parents("td:first").find('.p_star')
    var paper_id = obj.attr("data")
    //console.log($(window).scrollTop(), $(event.target).parents("td:first").position().top);
    var position_old = $(event.target).parents("td:first").position().top;
    var position_delta = 0;
    //$(event.target).parents("tr").effect("highlight", {}, 5000);
    if(obj.hasClass('star-filled')){
        $('.'+obj.attr('data')).each(function(){
            $(this).find('.p_star').removeClass('star-filled').addClass('star-open')
            $(this).removeClass('highlight')
        })
        if(!navigator.onLine){
            enable_alert("You unliked a paper. You are not online -- updating information locally.");
            var i =  starred.indexOf(paper_id)
            starred.splice(i, 1)
            add_pending_unstar(paper_id)
            populate_likes(starred)
            localStorage.setItem('starred', JSON.stringify(starred))
        }else{
            $.post('/like/unstar', {'papers': JSON.stringify([paper_id])}, function(res) {
              if(res.res[paper_id] == 'unstar'){
                $('.'+obj.attr('data')).each(function(){
                    $(this).find('.p_star').removeClass('star-filled').addClass('star-open')
                    $(this).removeClass('highlight')
                })

                var i =  starred.indexOf(paper_id)
                starred.splice(i, 1)
                populate_likes(starred)
                recommended = res.recs
                localStorage.setItem('starred', JSON.stringify(starred))
                localStorage.setItem('s_starred', JSON.stringify(s_starred))
                localStorage.setItem('recommended', JSON.stringify(recommended))
                
                if($("#recs tr").length == 0){
                    populate_recs(recommended)
                }else{
                    append_recs()
                }
                update_recs()
                update_session_view()
              }
            })
            .done(function(){
                //console.log($(window).scrollTop(), $(event.target).parents("td:first").position().top);
                enable_alert("You unliked a paper.");
                var scroll_current = $(window).scrollTop();
                position_delta = $(event.target).parents("td:first").position().top - position_old;
                if (position_delta != 0)
                  $('html, body').scrollTop(scroll_current + position_delta);
            });
        }
    }else{
        $('.'+obj.attr('data')).each(function(){
            $(this).find('.p_star').removeClass('star-open').addClass('star-filled')
            $(this).addClass('highlight')
        })
        if(!navigator.onLine){
            enable_alert("You liked a paper. You are not online -- updating information locally.");
            starred.push(paper_id)
            add_pending_star(paper_id)
            populate_likes(starred)
            localStorage.setItem('starred', JSON.stringify(starred))
        }else{
            $.post('/like/star', {'papers': JSON.stringify([paper_id])}, function(res) {
              if(res.res[paper_id] == 'star'){
                $('.'+obj.attr('data')).each(function(){
                    $(this).find('.p_star').removeClass('star-open').addClass('star-filled')
                    $(this).addClass('highlight')
                })
                starred.push(paper_id)
                populate_likes(starred)
                recommended = res.recs
                localStorage.setItem('starred', JSON.stringify(starred))
                localStorage.setItem('s_starred', JSON.stringify(s_starred))
                localStorage.setItem('recommended', JSON.stringify(recommended))
                
                if($("#recs tr").length == 0){
                    populate_recs(recommended)
                }else{            
                    append_recs()
                }
                update_recs()
                update_session_view()
                
              }
            })

            .done(function(){
                //console.log($(window).scrollTop(), $(event.target).parents("td:first").position().top);
                enable_alert("You liked a paper.");
                var scroll_current = $(window).scrollTop();
                position_delta = $(event.target).parents("td:first").position().top - position_old;
                if (position_delta != 0)
                  $('html, body').scrollTop(scroll_current + position_delta);
            });
        }



    }
}



function load_paper(){
    var paper_id = get_hash()
    console.log(paper_id)
    var selected_paper_html = get_selected_paper_html(paper_id)
    $('#selected_paper').find('.form').html(selected_paper_html)
    $('#similar_papers').html('')
    var recs = offline_recs[paper_id]
    var raw_html = ''
    for(var i = 0; i< recs.length; i++){
        raw_html += get_paper_html(recs[i].id)            
    } 
    $('#similar_papers').html(raw_html)     
} 




function load_similar_people(){
    var raw_html = ''
    if(user_recs == null)
        return
    for(var i = 0; i< user_recs.length; i++){
        raw_html += '<tr class="paper"><td class="metadata"></td><td class="content">' 
        if(user_recs[i].email)
            raw_html += '<h3>' + '<a href="mailto:'+user_recs[i].email+'">' + user_recs[i].email + '</a></h3>'
        if(user_recs[i].given_name && user_recs[i].family_name)
            raw_html += '<h4>' + user_recs[i].given_name + ' ' + user_recs[i].family_name + '</h4>'
        if(user_recs[i].inst)
            raw_html += user_recs[i].inst + '<br />'
        if(user_recs[i].dept)
            raw_html += '' + user_recs[i].dept + '<br />'
        if(user_recs[i].country)
            raw_html += '' + user_recs[i].country + '<br />'
        raw_html += '</td></tr>'           
    } 
    $('#similar_people').html(raw_html)     
} 



function update_papers_count(){
    setTimeout('update_papers_count_async();', 0)
}

function update_papers_count_async(){
    $("#papers_toggle .count").text("(" + $("#all_papers tr").length + ")");  
}

function update_papers_visible_count(){
    setTimeout('update_papers_visible_count_async();', 0)
}

function update_papers_visible_count_async(){
    $("#papers_toggle .count").text("(" + $("#all_papers tr:visible").length + ")");  
}

function update_recs_count(){
    setTimeout('update_recs_count_async();', 0)
}

function update_recs_count_async(){
    $("#recs_toggle .count").text("(" + $("#recs tr:visible").length + ")");  
}

function update_likes_count(){
    setTimeout('update_likes_count_async();', 0)
}

function update_likes_count_async(){
    $("#likes_toggle .count").text("(" + $("#likes tr").length + ")");  
}

function update_sessions_count(){
    setTimeout('update_sessions_count_async();', 0)
}

function update_sessions_count_async(){
    if ($("#program .session").length == $("#program .session:visible").length)
      $("#search-results .count").text("all");
    else
      $("#search-results .count").text($("#program .session:visible").length);  
}



function reset_all_papers(){
    $("#all_papers tr").show()
    $("#all_papers tr:gt(24)").hide()  

    if($("#all_papers tr:visible").length == $("#all_papers tr").length){
        $('#show_papers').hide();
    }else{
        $('#show_papers').show();
    }         
    update_papers_count();
}


function reset_sessions(){
    $('.session').show()
    $('.session').removeHighlight()
    $('.session-timeslot').each(function(){
        $(this).prev().hide()
    });  

    $('.session').each(function(){
        $(this).parent().prev().show()
        var p = $(this).attr("data")
        $("#"+p).hide()
        $(this).find('.arrow').removeClass("arrow-down").addClass("arrow-right");
        
    });
    update_sessions_count(); 
}


function populate_papers(){
    var raw_html = ''       
    for(var e in entities){
        raw_html += get_paper_html(e)
    }
    $("#all_papers").html(raw_html)
    $("#all_papers tr:gt(24)").hide()  

    if($("#all_papers tr:visible").length == $("#all_papers tr").length){
        $('#show_papers').hide();
    }else{
        $('#show_papers').show();
    }         
    update_papers_count();
}


function populate_recs(){  
    var raw_html = ''   
    for(var r in recommended){
        raw_html += get_paper_html(recommended[r].id)
    }
    $("#recs").html(raw_html)

    $("#recs tr:gt(4)").hide()  

    if($("#recs tr:visible").length == $("#recs tr").length){
        $('#show_recs').hide();
    }else{
        $('#show_recs').show();
    }         
      
   update_recs_count(); 
}


function append_recs(){  
    var visible_recs = []
    $("#recs tr:visible").each(function(){
        var d = $(this).attr("data")
        visible_recs.push(d)
    })
    //console.log(visible_recs)
    var n = $("#recs tr:visible").length
    $("#recs tr:hidden").remove()  
    var raw_html = ''
    for(var r in recommended){
        //console.log(visible_recs, recommended[r].id)
        if(visible_recs.indexOf(recommended[r].id) == -1){
            //console.log('not exists')
            raw_html += get_paper_html(recommended[r].id)
        }
    }
    $("#recs").append($(raw_html))
    $("#recs tr:gt("+(n-1)+")").hide() 
    if($("#recs tr:visible").length == $("#recs tr").length){
        $('#show_recs').hide();
    }else{
        $('#show_recs').show();
    }   

    
}



function populate_likes(){  
    var raw_html = '' 
    for(var i = starred.length; i>=0 ; i--){
       raw_html += get_paper_html(starred[i])
    }
    $("#likes").html(raw_html)
    if($("#likes tr").length <= 2){
        $('#show_likes').hide();
    }else{
         $('#show_likes').show()
        if($('#show_likes').html() == 'Show All'){
            $("#likes tr:gt(1)").hide()           
        }
    }  
  update_likes_count();
}


function populate_sessions(){
    $(".session-timeslot").html("")
    $('.session-timeslot').each(function(){
        $(this).prev().hide()
    }); 
    for(var s in sessions){
        var raw_html = get_session_html(s)
        var row = $(raw_html)
        place_session(row)
    }
    update_session_view()
}



function apply_filters(){
    var day_classes = '.'+$('.day.active').attr("data")
    var time_classes = '.'+$('.time.active').attr("data")
    var personas_classes = '.'+$('.persona.active').attr("data")
    var venues_classes = '.'+$('.venue.active').attr("data")
    var communities_classes = '.'+$('.community.active').attr("data")
    var papers_classes = '.'+$('.p_session.active').attr("data")
    /*
    console.log(day_classes)
    console.log(time_classes)
    console.log(venues_classes)
    console.log(personas_classes)
    console.log(papers_classes)
    */

    var select_class = $('.session')
    if(day_classes != '.all'){
        select_class = select_class.filter(day_classes)
    }
    
    if(time_classes!='.all'){               
        select_class = select_class.filter(time_classes)                
    }

    if(personas_classes!='.all'){               
        select_class = select_class.filter(personas_classes)                
    }

    if(venues_classes!='.all'){             
        select_class = select_class.filter(venues_classes)              
    }
    if(communities_classes!='.all'){             
        select_class = select_class.filter(communities_classes)              
    }

    if(papers_classes!='.all'){             
        select_class = select_class.filter(papers_classes)              
    }
   $('.session').hide();
   $('.session-timeslot').each(function(){
        $(this).prev().hide()
    });

   select_class.show();
   select_class.each(function(){
        $(this).parent().prev().show()
    });

   update_sessions_count(); 
}



function setup_filters(){
    $('.filter').off('click')
    $('.filter').on('click', function(){       
        //enable_loading("applying filter...");
        //$("#search_session").val("")
        //$("#search_session").blur()
        //reset_sessions()
        var attr = $(this).attr("type")
        $('.'+attr).removeClass('active')

        $(this).addClass('active')
        $('#search_sessions_btn').click()
        
    });
}



function enable_loading(msg){
  $("body .modal .message").text(msg);
  $("body").addClass("loading");
}



function disable_loading(){
  $("body").removeClass("loading");
}



function enable_alert(msg){
  $("body .alert .message").text(msg);
  $("body").addClass("notice");
  setTimeout(function(){
    $("body").removeClass("notice");
  }, 3000);
}
