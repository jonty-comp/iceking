<html>
  <head>
    <style>
      .loading {
        margin: 0 auto;
        width: 30px;
        height: 30px;
        border: 8px solid #000;
        border-right-color: transparent;
        border-radius: 50%;
        -webkit-animation-name:             rotate; 
        -webkit-animation-duration:         1s; 
        -webkit-animation-iteration-count:  infinite;
        -webkit-animation-timing-function: linear;
      }

      @-webkit-keyframes rotate {
        from {
          -webkit-transform: rotate(0deg);
        }
        to { 
          -webkit-transform: rotate(360deg);
        }
      }
    </style>
    <!--Load the AJAX API-->
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript" src="//ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
    <script type="text/javascript">
    
    // Load the Visualization API and the piechart package.
    google.load('visualization', '1', {'packages':['corechart']});
      
    // Set a callback to run when the Google Visualization API is loaded.
    google.setOnLoadCallback(drawChart);
      
    function drawChart() {
      if(<?if(isset($_REQUEST["start"])) echo(1); else echo(0) ?>) {
        $.ajax({
          url: "api/graph/stats/1/<?php echo($_REQUEST["start"]); ?>/<?php echo($_REQUEST["end"]); ?>/<?php echo(isset($_REQUEST["granularity"])? $_REQUEST["granularity"] : 86400) ?>",
          dataType:"json",
          success: function(data) {          
            // Create our data table out of JSON data loaded from server.
            var data = new google.visualization.DataTable(data);

            // Instantiate and draw our chart, passing in some options.
            var chart = new google.visualization.<?php echo($_REQUEST["type"]); ?>Chart(document.getElementById('chart'));
            chart.draw(data, {width: 1200, height: 768});
          }
        });

        $.ajax({
          url: "api/info/stats/1/<?php echo($_REQUEST["start"]); ?>/<?php echo($_REQUEST["end"]); ?>",
          dataType:"json",
          success: function(data) {
            var sizes = ['', 'K', 'M', 'G', 'T'];
            var i = parseInt(Math.floor(Math.log(data.bytes) / Math.log(1024)));
            bytes = Math.round(data.bytes / Math.pow(1024, i), 2) + ' ' + sizes[i];
            html="<strong>Total Hours:</strong> "+data.hours+"<br /><strong>Total Data:</strong> "+bytes+"B<br/><strong>Connections:</strong> "+data.connections+"<br/><strong>Unique Listeners:</strong> "+data.unique+"<br/>";

            $('#data').html(html);
          }
        });
      }
    }

    </script>
  </head>

  <body>
    <form action="" method="GET">
      <label for="start">Start:</label>
      <input type="date" name="start" id="start" value="<?php echo($_REQUEST["start"]); ?>">
      <label for="end">End:</label>
      <input type="date" name="end" id="end" value="<?php echo($_REQUEST["end"]); ?>">
      <label for="granularity">Granularity:</label>
      <select name="granularity" id="granularity">
        <option value="3600" <?php if($_REQUEST["granularity"] == "3600") echo(" selected"); ?>>1 Hour</option>
        <option value="86400" <?php if($_REQUEST["granularity"] == "86400") echo(" selected"); ?>>1 Day</option>
        <option value="604800" <?php if($_REQUEST["granularity"] == "604800") echo(" selected"); ?>>1 Week</option>
      </select>
      <label for="type">Type:</label>
      <select name="type" id="type">
        <option value="Line" <?php if($_REQUEST["type"] == "Line") echo(" selected"); ?>>Line</option>
        <option value="Column" <?php if($_REQUEST["type"] == "Column") echo(" selected"); ?>>Bar</option>
      </select>
      <button type="submit">Go</button>
    </form>
    <?php if(isset($_REQUEST["start"])) { ?>
    <div id="data"><div class="loading"></div></div>
    <div id="chart"><div class="loading"></div></div>
    <?php } ?>
  </body>
</html>