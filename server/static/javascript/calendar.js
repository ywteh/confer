// Assumptions
//
// schedule.slots.time as consistent format e.g., "1:30-4:00"
//
var str2hour = function(str) {
  if (/^\d+$/.test(str)) 
    return +str;
  var arr = str.split(':');
  var time = +arr[0] + (+arr[1] / 60.0);
  return time;
}


var str2time = function(str) {
  if (/pm$/.test(str)) {
    var hr = str2hour(str.substr(0,str.length-2));
    if (hr == 12) hr = 0;
    return [hr, 'pm'];
  } else if (/am$/.test(str)) {
    var hr = str2hour(str.substr(0,str.length-2))
    return [hr, 'am'];
  } else if (/^\d+:\d+$/.test(str)) {
    var time = str2hour(str);
    if (time > 12) 
      return [time-12, 'pm'];
    return [time, 'am'];
  } else if (/^\d+$/.test(str)) {
    return [+str, null];
  } else {
    return null;
  }
}


// @param timestr of "hour:min-hour:min" format.  hour in 24hr fmt
//                e.g., "1:30-3:30"
// @return { stime: Number between 0-24, fractional for minutes,
//           etime: same as stime }
var str2times = function(timestr) {
  var arr = timestr.split('-');
  var stime = str2time(arr[0]),
      etime = str2time(arr[1]);
  if (!stime || !etime || (!stime[1] && !etime[1])) {
    console.log("could not parse time: " + timestr);
    return null;
  }
  if (!stime[1]) {
    stime[1] = etime[1];
  }

  var shour = stime[0];
  if (stime[1] == 'pm') shour += 12;
  var ehour = etime[0];
  if (etime[1] == 'pm') ehour += 12;
  return {
    stime: shour,
    etime: ehour
  }
}

var fmtHour = function(hr) {
  if (hr == 0) {
    return "12 am";
  } else if (hr == 12) {
    return "noon";
  } else if (hr < 12) {
    return hr + " am";
  } else {
    return (hr - 12) + " pm";
  }
}


// create a list of sessions that contain starred talks.  
// @return array of 
//    ids: id of the talks in the session that have been starred
//    day: Date object of the day
//    stime: float representing time e.g., 8.5 == 8:30am
//    etime: 
var get_stared_submissions = function() {
  var staredslots = {};
  _.each(schedule, function(daySched) {
    var date = daySched.date;
    _.each(daySched.slots, function(slot) {
      var timestr = slot.time;
      var times = str2times(timestr);
      _.each(slot.sessions, function(s) {
        var session = sessions[s.session];
        if (!session) return;
        var isect = _.intersection(session.submissions, starred);
        var key = JSON.stringify([date, times.stime, times.etime]);
        if (isect.length > 0) {
          if (!(key in staredslots)) {
            staredslots[key] = { 
              ids: [], 
              day: date, 
              stime: times.stime, 
              etime: times.etime
            };
          }
          staredslots[key].ids.push.apply(staredslots[key].ids, isect)
        }
      })
      
    });
  })
  return _.values(staredslots);
}

//
// re-render calendar
//
var update_cal = function() {
  var stared_submissions = get_stared_submissions();
  var days = _.map(schedule, function(s) { return s.date; })
  var hours = _.times(24, function(d){return d;});

  // arbitrarily filter hours outside of 7am - 8pm window
  hours = _.filter(hours, function(hr) { return hr >= 7 && hr < 21; });
  var minhour = d3.min(hours),
      maxhour = d3.max(hours);

  // create a slot for each day/hour in the conference
  var allSlots = [];
  _.each(days, function(day) {
    _.each(hours, function(hour) { 
      allSlots.push({day: day, hour: hour})
    })
  });

  var labelwidth = 70,
      labelheight = 20,
      h = hours.length * labelheight,
      w = $("#schedule").width(), 
      x = d3.scale.ordinal().domain(days).rangeBands([labelwidth, w], 0, 0),
      y = d3.scale.linear().domain([minhour, maxhour]).range([labelheight, h]);

  // render calendar
  var cal = d3.select("#calendar")
    .attr('width', w)
    .attr('height', h);

  // render left labels
  var leftLabels = cal.append('g').classed('cal-left-label', true).selectAll("g")
      .data(hours)
    .enter().append("g")
  leftLabels.append("rect")
    .attr("x", 0)
    .attr('y', y)
    .attr('width', labelwidth)
    .attr('height', y(minhour+1)-y(minhour))
  leftLabels.append("text")
    .attr("transform", function(d) { return "translate(0, "+y(d)+")"})
    .attr('dy', '1.1em')
    .attr('dx', labelwidth-10)
    .attr('text-anchor', 'end')
    .text(fmtHour)
    

  // render top labels
  var topLabels = cal.append("g").classed("cal-top-label", true).selectAll("rect")
      .data(days)
    .enter()
  topLabels.append("rect")
    .attr('x', x)
    .attr('y', 0)
    .attr('width', x.rangeBand())
    .attr('height', labelheight)
  topLabels.append("text")
    .attr("transform", function(d) { return "translate("+x(d) + ", 0)"})
    .attr('dy', '1.1em')
    .attr('dx', x.rangeBand()/2)
    .attr('text-anchor', 'middle')
    .text(String)
    

  // Render a rectangle for each hour in the conference
  cal.append('g').classed('cal-hours', true).selectAll('.slot')
      .data(allSlots)
    .enter().append('rect')
      .classed("slot", true)
      .attr("x", function(d){return x(d.day)})
      .attr("y", function(d){return y(d.hour)})
      .attr('width', x.rangeBand())
      .attr('height', y(minhour+1)-y(minhour))


  // Render a rectangle for each session that contains starred talks
  var stars = cal.append('g').classed('cal-stars', true).selectAll('.cal-star')
      .data(stared_submissions)
    .enter().append('rect')
      .classed('cal-star', true)
      .attr('x', function(d) { return x(d.day)+1 })
      .attr('y', function(d) { return y(d.stime)+1 })
      .attr('height', function(d) { return y(d.etime)-y(d.stime)-2 })
      .attr('width', x.rangeBand()-2)

  stars.on('mouseover', function(d) {
    var par = d3.select($(this).parent().get(0))
    var me = d3.select(this)
    // this is not quite right, because 
    var text = d.ids.length + " talks"
    par.append('text')
      .attr("transform", "translate("+x(d.day) + "," + y(d.stime)+")")
      .attr("dy", "1.2em")
      .attr("dx", 5)
      .text(text)
    me.style("fill", "rgb(46, 120, 182)");
  })

  stars.on("mouseout", function(d) {
    var par = d3.select($(this).parent().get(0))
    var me = d3.select(this);
    me.style("fill", 'steelblue')
    par.selectAll("text").remove()
  })
        

}