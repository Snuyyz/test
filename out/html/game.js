(function() {
  var game;
  var ui;

  var DateOptions = {hour: 'numeric',
                 minute: 'numeric',
                 second: 'numeric',
                 year: 'numeric',
                 month: 'short',
                 day: 'numeric' };

  var main = function(dendryUI) {
    ui = dendryUI;
    game = ui.game;

    // Add your custom code here.
  };

  var TITLE = "Social Democracy: An Alternate History America 2014-2026" + "_" + "Autumn Chen";

  // the url is a link to game.json
  // test url: https://aucchen.github.io/social_democracy_mods/v0.1.json
  window.loadMod = function(url) {
      ui.loadGame(url);
  };

  window.showStats = function() {
    if (window.dendryUI.dendryEngine.state.sceneId.startsWith('library')) {
        window.dendryUI.dendryEngine.goToScene('backSpecialScene');
    } else {
        window.dendryUI.dendryEngine.goToScene('library');
    }
  };
  
  window.showMods = function() {
    window.hideOptions();
    if (window.dendryUI.dendryEngine.state.sceneId.startsWith('mod_loader')) {
        window.dendryUI.dendryEngine.goToScene('backSpecialScene');
    } else {
        window.dendryUI.dendryEngine.goToScene('mod_loader');
    }
  };
  
  window.showOptions = function() {
      var save_element = document.getElementById('options');
      window.populateOptions();
      save_element.style.display = "block";
      if (!save_element.onclick) {
          save_element.onclick = function(evt) {
              var target = evt.target;
              var save_element = document.getElementById('options');
              if (target == save_element) {
                  window.hideOptions();
              }
          };
      }
  };

  window.hideOptions = function() {
      var save_element = document.getElementById('options');
      save_element.style.display = "none";
  };

  window.disableBg = function() {
      window.dendryUI.disable_bg = true;
      document.body.style.backgroundImage = 'none';
      window.dendryUI.saveSettings();
  };

  window.enableBg = function() {
      window.dendryUI.disable_bg = false;
      window.dendryUI.setBg(window.dendryUI.dendryEngine.state.bg);
      window.dendryUI.saveSettings();
  };

  window.disableAnimate = function() {
      window.dendryUI.animate = false;
      window.dendryUI.saveSettings();
  };

  window.enableAnimate = function() {
      window.dendryUI.animate = true;
      window.dendryUI.saveSettings();
  };

  window.disableAnimateBg = function() {
      window.dendryUI.animate_bg = false;
      window.dendryUI.saveSettings();
  };

  window.enableAnimateBg = function() {
      window.dendryUI.animate_bg = true;
      window.dendryUI.saveSettings();
  };

  window.disableAudio = function() {
      window.dendryUI.toggle_audio(false);
      window.dendryUI.saveSettings();
  };

  window.enableAudio = function() {
      window.dendryUI.toggle_audio(true);
      window.dendryUI.saveSettings();
  };

  window.enableImages = function() {
    window.dendryUI.show_portraits = true;
    window.dendryUI.saveSettings();
   };

  window.disableImages = function() {
    window.dendryUI.show_portraits = false;
    window.dendryUI.saveSettings();
};

window.enableLightMode = function() {
    window.dendryUI.dark_mode = false;
    document.body.classList.remove('dark-mode');
    window.dendryUI.saveSettings();
};
window.enableDarkMode = function() {
    window.dendryUI.dark_mode = true;
    document.body.classList.add('dark-mode');
    window.dendryUI.saveSettings();
};

window.enableGrayMode = function() {
    window.dendryUI.gray_mode = true;
    document.body.classList.add('gray-mode');
    window.dendryUI.saveSettings();
};
window.disableGrayMode = function() {
    window.dendryUI.gray_mode = false;
    document.body.classList.remove('gray-mode');
    window.dendryUI.saveSettings();
};

  // populates the checkboxes in the options view
  window.populateOptions = function() {
    var disable_bg = window.dendryUI.disable_bg;
    var animate = window.dendryUI.animate;
    var disable_audio = window.dendryUI.disable_audio;
    var show_portraits = window.dendryUI.show_portraits;
    if (disable_bg) {
        $('#backgrounds_no')[0].checked = true;
    } else {
        $('#backgrounds_yes')[0].checked = true;
    }
    if (animate) {
        $('#animate_yes')[0].checked = true;
    } else {
        $('#animate_no')[0].checked = true;
    }
    if (disable_audio) {
        $('#audio_no')[0].checked = true;
    } else {
        $('#audio_yes')[0].checked = true;
    }
    if (show_portraits) {
        $('#images_yes')[0].checked = true;
    } else {
        $('#images_no')[0].checked = true;
    }
    if (window.dendryUI.dark_mode) {
        $('#dark_mode')[0].checked = true;
    } else {
        $('#light_mode')[0].checked = true;
    }
    if (window.dendryUI.gray_mode) {
        $('#gray_on')[0].checked = true;
    } else {
        $('#gray_no')[0].checked = true;
    }
  };

  
  // This function allows you to modify the text before it's displayed.
  // E.g. wrapping chat-like messages in spans.
  window.displayText = function(text) {
      return text;
  };

  // This function allows you to do something in response to signals.
  window.handleSignal = function(signal, event, scene_id) {
  };
  
  // This function runs on a new page. Right now, this auto-saves.
  window.onNewPage = function() {
    var scene = window.dendryUI.dendryEngine.state.sceneId;
    if (scene != 'root' && !window.justLoaded) {
        window.dendryUI.autosave();
    }
    if (window.justLoaded) {
        window.justLoaded = false;
    }
  };

  window.updateSidebar = function() {
      $('#qualities').empty();
      var scene = dendryUI.game.scenes[window.statusTab];
      dendryUI.dendryEngine._runActions(scene.onArrival);
      var displayContent = dendryUI.dendryEngine._makeDisplayContent(scene.content, true);
      $('#qualities').append(dendryUI.contentToHTML.convert(displayContent));
  };

  window.updateSidebarRight = function() {
    $('#qualities_right').empty();
    var scene = dendryUI.game.scenes[window.statusTabRight];
    dendryUI.dendryEngine._runActions(scene.onArrival);
    var displayContent = dendryUI.dendryEngine._makeDisplayContent(scene.content, true);
    $('#qualities_right').append(dendryUI.contentToHTML.convert(displayContent));
};

  window.changeTab = function(newTab, tabId, isRight) {
      if (tabId == 'poll_tab' && (dendryUI.dendryEngine.state.qualities.historical_mode || dendryUI.dendryEngine.state.qualities.rubicon)) {
          if (dendryUI.dendryEngine.state.qualities.historical_mode && !dendryUI.dendryEngine.state.qualities.rubicon) window.alert('Polls are not available in historical mode.');
          if (dendryUI.dendryEngine.state.qualities.rubicon) window.alert('Polls are not available after crossing the rubicon.');
          return;
      }
      var tabButton = document.getElementById(tabId);
      var tabButtons = document.getElementsByClassName('tab_button');
      for (i = 0; i < tabButtons.length; i++) {
        tabButtons[i].className = tabButtons[i].className.replace(' active', '');
      }
      tabButton.className += ' active';
      if (isRight) {
        window.statusTabRight = newTab;
        window.updateSidebarRight();
        } else {
          window.statusTab = newTab;
          window.updateSidebar();
    }
  };

  // ---------------------------------------------------------------------
  // Election result charts (House / Senate hemicycles, Electoral College).
  // Scenes emit <div class="sd-chart" data-chart="house|senate|ec" ...>
  // placeholders; they are filled in here after the content is displayed.
  // ---------------------------------------------------------------------
  var SD_DEM = '#1a5fb4';
  var SD_GOP = '#c01c28';

  var CHAMBERS = {
      house:  {name: 'House of Representatives', total: 435, majority: 218},
      senate: {name: 'Senate', total: 100, majority: 51}
  };

  // keep order in sync with SD.bloc_names in tools/sd_lib.js
  var EC_BLOCS = [
      {name: 'Blue-core states', ev: 230},
      {name: 'Industrial Midwest', ev: 44},
      {name: 'Florida / Ohio / Iowa', ev: 53},
      {name: 'Sun Belt', ev: 49},
      {name: 'Red-core states', ev: 162}
  ];

  function chartWidth(el) {
      var w = el.getBoundingClientRect().width || el.offsetWidth || 480;
      return Math.max(240, Math.min(520, Math.floor(w)));
  }

  function svgText(parent, cls, x, y, txt) {
      return parent.append('text').attr('class', cls)
          .attr('x', x).attr('y', y).attr('text-anchor', 'middle').text(txt);
  }

  function renderChamber(el, kind) {
      var cfg = CHAMBERS[kind];
      var dem = Math.max(0, Math.min(cfg.total, Math.round(parseFloat(el.getAttribute('data-dem')))));
      if (isNaN(dem)) { return; }
      var gop = cfg.total - dem;
      var prev = parseFloat(el.getAttribute('data-prev'));
      var w = chartWidth(el);

      var title = d3.select(el).append('div').attr('class', 'sd-chart-title').text(cfg.name);

      var svg = d3.select(el).append('svg')
          .attr('class', 'sd-svg')
          .attr('role', 'img')
          .attr('aria-label', cfg.name + ': Democrats ' + dem + ', Republicans ' + gop)
          .attr('width', w).attr('height', Math.ceil(w / 2) + 4);

      // d3.parliament breaks on zero-seat parties, so only pass non-empty ones
      var parties = [];
      if (dem > 0) { parties.push({id: 'dem', name: 'Democrats', color: SD_DEM, seats: dem}); }
      if (gop > 0) { parties.push({id: 'gop', name: 'Republicans', color: SD_GOP, seats: gop}); }

      // a fresh instance per chart: the library caches width in its closure
      var parliament = d3.parliament().width(w).innerRadiusCoef(0.4);
      parliament.enter.fromCenter(false).smallToBig(true);
      parliament.update.animate(false);
      svg.datum(parties).call(parliament);

      // a 50-50 Senate is decided by the vice president, so keep it neutral
      var tied = (kind === 'senate' && dem === 50);
      var demWins = dem >= cfg.majority;
      var cx = w / 2, base = w / 2;
      svgText(svg, 'sd-center-num ' + (tied ? '' : (demWins ? 'sd-d' : 'sd-r')), cx, base - 30, dem + ' \u2013 ' + gop);
      svgText(svg, 'sd-center-sub', cx, base - 10, cfg.majority + ' for majority' + (kind === 'senate' ? ' (50 + VP)' : ''));

      var cap = d3.select(el).append('div').attr('class', 'sd-chart-caption');
      cap.append('span').attr('class', 'sd-d').text('\u25CF Democrats ' + dem);
      cap.append('span').text('   ');
      cap.append('span').attr('class', 'sd-r').text('\u25CF Republicans ' + gop);
      if (!isNaN(prev)) {
          var diff = dem - prev;
          var txt = diff === 0 ? 'no change in Democratic seats' :
              (diff > 0 ? '+' : '\u2212') + Math.abs(diff) + ' Democratic seats vs. outgoing Congress (' + prev + ')';
          d3.select(el).append('div').attr('class', 'sd-chart-caption sd-muted').text(txt);
      }
  }

  function shadeFor(demWon, margin) {
      var a = Math.abs(margin);
      if (demWon) { return a < 3 ? '#7fb0ea' : (a < 8 ? '#3f82d6' : SD_DEM); }
      return a < 3 ? '#e8868d' : (a < 8 ? '#d9505b' : SD_GOP);
  }

  function renderEC(el) {
      var margins = (el.getAttribute('data-margins') || '').split(',').map(parseFloat);
      var wins = (el.getAttribute('data-wins') || '').split(',').map(function (x) { return parseInt(x, 10) === 1; });
      if (margins.length !== EC_BLOCS.length || margins.some(isNaN)) { return; }

      var blocs = EC_BLOCS.map(function (b, i) {
          return {name: b.name, ev: b.ev, margin: margins[i], dem: wins[i]};
      });
      var demEV = d3.sum(blocs.filter(function (b) { return b.dem; }), function (b) { return b.ev; });
      var gopEV = 538 - demEV;

      // most Democratic on the left, most Republican on the right
      var ordered = blocs.slice().sort(function (a, b) {
          if (a.dem !== b.dem) { return a.dem ? -1 : 1; }
          return a.dem ? (b.margin - a.margin) : (a.margin - b.margin);
      });

      var w = chartWidth(el), barH = 34, top = 26, h = top + barH + 22;
      var x = d3.scaleLinear().domain([0, 538]).range([0, w]);

      d3.select(el).append('div').attr('class', 'sd-chart-title').text('Electoral College');

      var svg = d3.select(el).append('svg').attr('class', 'sd-svg')
          .attr('role', 'img')
          .attr('aria-label', 'Electoral College: Democrats ' + demEV + ', Republicans ' + gopEV)
          .attr('width', w).attr('height', h);

      var acc = 0;
      ordered.forEach(function (b) {
          var g = svg.append('g');
          g.append('rect').attr('x', x(acc)).attr('y', top).attr('width', Math.max(0, x(b.ev) - 1))
              .attr('height', barH).attr('fill', shadeFor(b.dem, b.margin));
          if (x(b.ev) > 26) {
              svgText(g, 'sd-ec-ev', x(acc) + x(b.ev) / 2, top + barH / 2 + 5, b.ev);
          }
          acc += b.ev;
      });

      // 270 line
      svg.append('line').attr('class', 'sd-ec-line').attr('x1', x(270)).attr('x2', x(270))
          .attr('y1', top - 6).attr('y2', top + barH + 6);
      svg.append('text').attr('class', 'sd-center-sub').attr('x', x(270)).attr('y', top + barH + 18)
          .attr('text-anchor', 'middle').text('270 to win');

      svg.append('text').attr('class', 'sd-ec-total sd-d').attr('x', 0).attr('y', 16)
          .attr('text-anchor', 'start').text('Democrats ' + demEV);
      svg.append('text').attr('class', 'sd-ec-total sd-r').attr('x', w).attr('y', 16)
          .attr('text-anchor', 'end').text('Republicans ' + gopEV);

      // per-bloc table (readable without relying on colour alone)
      var tbl = d3.select(el).append('table').attr('class', 'sd-ec-table');
      var rows = tbl.selectAll('tr').data(blocs).enter().append('tr');
      rows.append('td').append('span').attr('class', 'sd-swatch')
          .style('background', function (b) { return shadeFor(b.dem, b.margin); });
      rows.append('td').text(function (b) { return b.name; });
      rows.append('td').attr('class', 'sd-num').text(function (b) { return b.ev + ' EV'; });
      rows.append('td').attr('class', function (b) { return 'sd-num ' + (b.dem ? 'sd-d' : 'sd-r'); })
          .text(function (b) {
              var m = Math.abs(b.margin).toFixed(1);
              return (b.dem ? 'D' : 'R') + ' won' + (b.margin === 0 ? '' : ' (' + (b.margin > 0 ? 'D+' : 'R+') + m + ')');
          });
  }

  window.renderElectionCharts = function () {
      if (typeof d3 === 'undefined' || !d3.parliament) { return; }
      var nodes = document.querySelectorAll('#content .sd-chart');
      for (var i = 0; i < nodes.length; i++) {
          var el = nodes[i];
          if (el.getAttribute('data-rendered')) { continue; }
          el.setAttribute('data-rendered', '1');
          try {
              var kind = el.getAttribute('data-chart');
              if (kind === 'house' || kind === 'senate') { renderChamber(el, kind); }
              else if (kind === 'ec') { renderEC(el); }
          } catch (e) {
              console.error('chart render failed', e);
          }
      }
  };

  window.onDisplayContent = function() {
      window.updateSidebar();
      window.updateSidebarRight();
      window.renderElectionCharts();
  };

  window.toggleDem = function toggleDemographicTable() {
      const resultsDiv = document.getElementById('results');
      // Toggle display between 'none' and 'block'
      if (resultsDiv.style.display === 'none' || resultsDiv.style.display === '') {
          resultsDiv.style.display = 'block'; // or 'table' for the table specifically
      } else {
          resultsDiv.style.display = 'none';
      }
  };
  window.toggleGraph = function toggleGraph() {
      const svgElement = document.getElementById('party_support_history');
      if (svgElement.style.display === 'none' || svgElement.style.display === '') {
          svgElement.style.display = 'block';
      } else {
          svgElement.style.display = 'none';
      }
  };
  window.toggleElectionGraph = function toggleElectionGraph() {
      const svgElement = document.getElementById('election_history');
      if (svgElement.style.display === 'none' || svgElement.style.display === '') {
          svgElement.style.display = 'block';
      } else {
          svgElement.style.display = 'none';
      }
  };
  window.toggleNews = function toggleNews() {
      const elements = document.querySelectorAll('.rightnews');
      const elements2 = document.querySelectorAll('.other');
      const button = document.getElementById('news_tab');

      if (!button) {
          console.error('Button with id "news_tab" not found.');
          return;
      }

      elements.forEach(function (element) {
          if (element.style.display !== 'block') {
              element.style.display = 'block';
              button.innerHTML = "View Other News";
          } else {
              element.style.display = 'none';
              button.innerHTML = "View Right-Wing News";
          }
      });

      elements2.forEach(function (element) {
          if (element.style.display !== 'none') {
              element.style.display = 'none';
          } else {
              element.style.display = 'block';
          }
      });

      button.style.backgroundColor = '#dddddd';
  };

  /*
   * This function copied from the code for Infinite Space Battle Simulator
   *
   * quality - a number between max and min
   * qualityName - the name of the quality
   * max and min - numbers
   * colors - if true/1, will use some color scheme - green to yellow to red for high to low
   * */
  window.generateBar = function(quality, qualityName, max, min, colors) {
      var bar = document.createElement('div');
      bar.className = 'bar';
      var value = document.createElement('div');
      value.className = 'barValue';
      var width = (quality - min)/(max - min);
      if (width > 1) {
          width = 1;
      } else if (width < 0) {
          width = 0;
      }
      value.style.width = Math.round(width*100) + '%';
      if (colors) {
          value.style.backgroundColor = window.probToColor(width*100);
      }
      bar.textContent = qualityName + ': ' + quality;
      if (colors) {
          bar.textContent += '/' + max;
      }
      bar.appendChild(value);
      return bar;
  };


  window.justLoaded = true;
  window.statusTab = "status";
  window.statusTabRight = "status_right";
  window.dendryModifyUI = main;
  console.log("Modifying stats: see dendryUI.dendryEngine.state.qualities");

  window.onload = function() {
    window.dendryUI.loadSettings({show_portraits: true});
    if (window.dendryUI.dark_mode) {
        document.body.classList.add('dark-mode');
    }
    if (window.dendryUI.gray_mode) {
        document.body.classList.add('gray-mode');
    }
    window.pinnedCardsDescription = "Advisor cards - actions are only usable once per 6 months.";
    window.statusTab = "status";
    window.updateSidebar();
    window.statusTabRight = "status_right";
    window.updateSidebarRight();
  };

}());
