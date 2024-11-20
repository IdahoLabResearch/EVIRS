function dischargechart(data) {

  var svg = d3.select("svg"),
      margin = {top: 20, right: 20, bottom: 100, left: 100},
      width = +svg.attr("width") - margin.left - margin.right,
      height = +svg.attr("height") - margin.top - margin.bottom;

  var x = d3.scaleBand().rangeRound([0, width]).padding(0.1),
      y = d3.scaleLinear().rangeRound([height, 0]);

  d3.selectAll("svg > *").remove();
  var g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  disPct = document.getElementById("dischargePct").value;
  disTime = document.getElementById("dischargeTime").value;
  chtDisPct = document.getElementById("chtDisPct");
  chtDisTime = document.getElementById("chtDisTime");
  chtDisPct.innerHTML = disPct + "%";
  chtDisTime.innerHTML = disTime + (disTime == 1 ? " hour" : " hours");


  // (d.discharge1hr_kw * 2.0) is used because the data used is based on 50% discharge in one hour,
  // but we need it at 100% discharge to then calculate the values based on user input of 
  // percent discharge and time
  x.domain(data.map(function(d) { return d.EV; }));
  y.domain([0, d3.max(data, function(d) { return (d.discharge1hr_kw * 2.0) * 0.01 * disPct / disTime; })]);

  g.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + height + ")")
    .call(d3.axisBottom(x))
    .selectAll("text")
      .style("text-anchor", "end")
      .attr("dx", "-.8em")
      .attr("dy", ".15em")
      .attr("transform", "rotate(-30)");

  g.append("g")
    .attr("class", "y axis")
    .call(d3.axisLeft(y).ticks(10))
    .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", margin.left+20)
      .attr("x", margin.top)
      .attr("text-anchor", "end");

  g.selectAll(".bar")
    .data(data)
    .enter().append("rect")
      .attr("class", "bar")
      .attr("x", function(d) { return x(d.EV); })
      .attr("y", function(d) { return y((d.discharge1hr_kw * 2.0) * 0.01 * disPct / disTime); })
      .attr("width", x.bandwidth())
      .attr("height", function(d) { return height - y((d.discharge1hr_kw * 2.0) * 0.01 * disPct / disTime); })
      .append("title") 
      .text((d) => `${((d.discharge1hr_kw * 2.0) * 0.01 * disPct / disTime).toFixed(1)} kW`);

  // g.append("text")
  //   .attr("transform", "translate(" + (width/2) + " ," + (height+85) + ")")
  //   .style("text-anchor", "middle")
  //   .text("Vehicle");

  g.append("text")
    .attr("transform", "rotate(-90)")
    .attr("x", -(height/2))
    .attr("y", -30)
    .style("text-anchor", "middle")
    .text("Kilowatts");

  d3.select("#d3sortbykw").on("change", sortchart);
  d3.select("#d3sortbyvehicle").on("change", sortchart);

  var sortTimeout = setTimeout(function() {
      d3.select("#d3sortbykw").property("checked", true).each(sortchart);
    }, 50);

  function sortchart() {
    clearTimeout(sortTimeout);
    this.id == "d3sortbykw" ? sortbykw = true : sortbykw = false;

    // Copy-on-write since tweens are evaluated after a delay.
    var x0 = x.domain(data.sort(sortbykw
      ? function(a, b) { return b.discharge1hr_kw - a.discharge1hr_kw; }
      : function(a, b) { return d3.ascending(a.EV, b.EV); })
      .map(function(d) { return d.EV; }))
      .copy();

    svg.selectAll(".bar").sort(function(a, b) { return x0(a.EV) - x0(b.EV); });
    var transition = svg.transition().duration(250), delay = function(d, i) { return i * 25; };
    transition.selectAll(".bar").delay(delay).attr("x", function(d) { return x0(d.EV); });
    transition.select(".x.axis").call(d3.axisBottom(x)).selectAll("g").delay(delay);
  }

  // const annotations = [
  //   { // first annotation
  //     x: margin.left,
  //     y: margin.top + 4/9 * height,
  //     dy: 0,
  //     dx: width 
  //   },
  //   { // second annotation
  //     note: {
  //       label: "discharging power > 50 kW",
  //       title: "",
  //       align: "right",
  //       wrap: 200
  //     },
  //     connector: {
  //       end: "arrow"
  //     },
  //     x: margin.left + 0.35 * width,
  //     y: margin.top + 4/9 * height,
  //     dy: -80,
  //     dx: 100
  //   }
  // ]

  // const makeAnnotations = d3.annotation()
  //   .annotations(annotations);
  // d3.select("#dischargechart")
  //   .append("g")
  //   .call(makeAnnotations)
}

