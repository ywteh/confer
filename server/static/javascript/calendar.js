
// @param datstr string in "month/day/2-character-year" format
//               e.g., "9/22/85"
// @return Date object
var str2date = function(datestr) {
  var arr = datestr.split('/')
  var m = +arr[0],
      d = +arr[1],
      y = 2000 + +arr[2];
  return new Date(y, m, d);
}

// @param timestr of "hour:min-hour:min" format.  hour in 24hr fmt
//                e.g., "1:30-3:30"
// @return { stime: Number between 0-24, fractional for minutes,
//           etime: same as stime }
var str2times = function(timestr) {
  var arr = timestr.split('-');
  var stime = arr[0], etime = arr[1];
  var sarr = stime.split(':'),
      earr = etime.split(':');
  stime = +sarr[0] + (+sarr[1] / 60.0);
  etime = +earr[0] + (+earr[1] / 60.0);
  return {
    stime: stime,
    etime: etime
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
    var datestr = daySched.date;
    var date = str2date(datestr);
    _.each(daySched.slots, function(slot) {
      var timestr = slot.time;
      var times = str2times(timestr);
      _.each(slot.sessions, function(s) {
        var session = sessions[s.session];
        if (!session) return;
        var isect = _.intersection(session.submissions, starred);
        var key = JSON.stringify([date.toString(), times.stime, times.etime]);
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
  var mind = d3.min(schedule, function(s) { return str2date(s.date) })
  var maxd = d3.max(schedule, function(s) { return str2date(s.date) })
  var dayms = 1000 * 60 * 60 * 24;
  var diff = (maxd - mind) / dayms;

  // list of days in conference
  var days = _.times(diff+1, function(d) {
    return new Date(mind.getTime() + (d*dayms));
  });

  // arbitrarily filter hours outside of 7am - 8pm window
  var hours = _.times(24, function(d){return d;});
  hours = _.filter(hours, function(hr) { return hr >= 7 && hr < 21; })

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
      y = d3.scale.linear().domain([d3.min(hours), d3.max(hours)]).range([labelheight, h]);

  var stared_submissions = get_stared_submissions();

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
    .attr('width', labelwidth)
    .attr('y', y)
    .attr('height', y(1)-y(0))
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
    .text(function(d){ return d.toDateString(); })//return d.getMonth() + "-" + d.getDate() + "-" + d.getYear();})
    

  // Render a rectangle for each hour in the conference
  cal.append('g').classed('cal-hours', true).selectAll('.slot')
      .data(allSlots)
    .enter().append('rect')
      .classed("slot", true)
      .attr("x", function(d){return x(d.day)})
      .attr("y", function(d){return y(d.hour)})
      .attr('width', x.rangeBand())
      .attr('height', y(1)-y(0))

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
    me.style("fill", "rgb(112, 169, 218)")
  })

  stars.on("mouseout", function(d) {
    var par = d3.select($(this).parent().get(0))
    var me = d3.select(this);
    me.style("fill", 'steelblue')
    par.selectAll("text").remove()
  })
        

}