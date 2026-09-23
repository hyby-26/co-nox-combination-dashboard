/* Hover highlight for figures built with theme.enable_hover_highlight() (layout.meta.hoverHighlight).
   - Bar traces: the hovered bar turns the highlight color.
   - Line traces: a crosshair spans every subplot, and each other subplot gets a dot + value
     at the same x, so one date can be read across all sensors at once.
   Highlight marks are layout shapes/annotations tagged with TAG, so they're cheap to draw
   (relayout, no data recalculation) and easy to strip back out. They're placed in axis-domain
   coordinates ('x domain'/'y domain'), not data coordinates: data-referenced marks join
   autorange, so a value label near the right edge would stretch the x-axis, shift the hovered
   point, and make Plotly's rehover fire plotly_unhover — wiping the crosshair just drawn. */
(function () {
  var TAG = 'hover-highlight';

  function cssVar(name) {
    return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  }

  function highlightColor(gd) {
    var meta = gd.layout && gd.layout.meta;
    return meta && meta.hoverHighlight;
  }

  function withoutTagged(items) {
    return (items || []).filter(function (item) { return item.name !== TAG; });
  }

  // Matches the hovertemplate precision (%{y:.2f}) set in components/timeseries.py.
  function formatValue(v) {
    return v.toFixed(2);
  }

  // 'x2' -> 'x2 domain' ref and its fullLayout axis ('xaxis2').
  function domainRef(ref) {
    return ref + ' domain';
  }

  function axisOf(gd, ref) {
    return gd._fullLayout[ref.charAt(0) + 'axis' + ref.slice(1)];
  }

  // Fraction of the axis length (0 = left/bottom, 1 = right/top) for data value v.
  function toDomain(ax, v) {
    var frac = ax.l2p(ax.d2l(v)) / ax._length;
    return ax._id.charAt(0) === 'y' ? 1 - frac : frac;
  }

  function inDomain(frac) {
    return frac >= 0 && frac <= 1;
  }

  function resetBar(gd) {
    var state = gd.__hoverHighlightBar;
    if (!state) return;
    gd.__hoverHighlightBar = null;
    Plotly.restyle(gd, { 'marker.color': [state.base] }, [state.trace]);
  }

  function highlightBar(gd, pt, color) {
    var state = gd.__hoverHighlightBar;
    if (state && state.trace !== pt.curveNumber) {
      resetBar(gd);
      state = null;
    }
    var base = state ? state.base : pt.data.marker.color;
    var colors = new Array(gd.calcdata[pt.curveNumber].length).fill(base);
    colors[pt.pointNumber] = color;
    gd.__hoverHighlightBar = { trace: pt.curveNumber, base: base };
    Plotly.restyle(gd, { 'marker.color': [colors] }, [pt.curveNumber]);
  }

  function highlightX(gd, pt, color) {
    var surface = cssVar('--surface');
    var text = cssVar('--text');
    var xref = pt.fullData.xaxis;
    var x = toDomain(axisOf(gd, xref), pt.x);
    var shapes = [{
      name: TAG, type: 'line', layer: 'above',
      xref: domainRef(xref), yref: 'paper', x0: x, x1: x, y0: 0, y1: 1,
      line: { color: color, width: 1 },
    }];
    var annotations = [];
    gd._fullData.forEach(function (trace) {
      if (trace.type !== 'scatter' && trace.type !== 'scattergl') return;
      var y = trace.y[pt.pointNumber];
      if (y === null || y === undefined || isNaN(y)) return;
      // Domain refs aren't hidden when off-axis like data refs are, so skip those ourselves.
      var ty = toDomain(axisOf(gd, trace.yaxis), y);
      if (!inDomain(ty)) return;
      var tx = domainRef(trace.xaxis);
      var yref = domainRef(trace.yaxis);
      shapes.push({
        name: TAG, type: 'circle', layer: 'above',
        xref: tx, yref: yref, xsizemode: 'pixel', ysizemode: 'pixel',
        xanchor: x, yanchor: ty, x0: -5, x1: 5, y0: -5, y1: 5,
        fillcolor: color, line: { color: surface, width: 2 },
      });
      // The hovered subplot already shows its value in the hover label.
      if (trace.index === pt.curveNumber) return;
      annotations.push({
        name: TAG, xref: tx, yref: yref, x: x, y: ty,
        text: formatValue(y), showarrow: false, xanchor: 'left', yanchor: 'bottom',
        xshift: 6, yshift: 2, font: { color: text, size: 11 },
      });
    });
    Plotly.relayout(gd, {
      shapes: withoutTagged(gd.layout.shapes).concat(shapes),
      annotations: withoutTagged(gd.layout.annotations).concat(annotations),
    });
  }

  function clearX(gd) {
    var shapes = gd.layout.shapes || [];
    if (!shapes.some(function (s) { return s.name === TAG; })) return;
    Plotly.relayout(gd, {
      shapes: withoutTagged(shapes),
      annotations: withoutTagged(gd.layout.annotations),
    });
  }

  function bind(gd) {
    if (gd.__hoverHighlightBound || typeof gd.on !== 'function') return;
    gd.__hoverHighlightBound = true;
    var pending = null;
    var frame = null;

    // Coalesce rapid hover events into one redraw per animation frame.
    gd.on('plotly_hover', function (e) {
      var color = highlightColor(gd);
      var pt = e.points && e.points[0];
      if (!color || !pt) return;
      pending = pt;
      if (frame !== null) return;
      frame = requestAnimationFrame(function () {
        var p = pending;
        frame = null;
        pending = null;
        if (p.data.type === 'bar') highlightBar(gd, p, color);
        else if (p.data.type === 'scatter' || p.data.type === 'scattergl') highlightX(gd, p, color);
      });
    });
    gd.on('plotly_unhover', function () {
      if (!highlightColor(gd)) return;
      // Drop a queued highlight so it can't land after the pointer has left.
      if (frame !== null) cancelAnimationFrame(frame);
      frame = null;
      pending = null;
      resetBar(gd);
      clearX(gd);
    });
  }

  function bindAll() {
    document.querySelectorAll('.js-plotly-plot').forEach(bind);
  }

  // dcc.Graph elements come and go with tab switches, so watch for new ones.
  var scheduled = false;
  new MutationObserver(function () {
    if (scheduled) return;
    scheduled = true;
    requestAnimationFrame(function () {
      scheduled = false;
      bindAll();
    });
  }).observe(document.documentElement, { childList: true, subtree: true });
})();
