|Python package| |Maintainability|

.. |Python package| image:: https://github.com/routable-ai/pyrai/workflows/Python%20package/badge.svg
.. |Maintainability| image:: https://api.codeclimate.com/v1/badges/66de1d6f60f75019d648/maintainability
   :target: https://codeclimate.com/repos/5ef4f3a2a5ffaf4b95013923/maintainability

pyrai: A Python library for the Routable AI API
===============================================

Introduction
------------

Pyrai makes it easy to use the Routable AI API to create, run, and visualize simulations with just 10 lines of code.

.. code:: python

    import pyrai
    import datetime
    rai = pyrai.Pyrai(api_key="API-KEY-HERE")
    fleet = rai.create_live_fleet()
    fleet.make_vehicle_online(vid=1, location=pyrai.Location(lat=42.36, lng=71.05), capacity=4)
    fleet.add_request(rid=1, pickup=pyrai.Location(42.1,71.2), dropoff=pyrai.Location(42.3,71.4), load=4)
    fleet.get_assignments()
    fleet.forward_simulate("10m")
    fleet.visualize()

Features
--------

Pyrai allows you to create, run, and visualize simulations with the
Routable AI API, right in Python.

Getting Started
^^^^^^^^^^^^^^^

Begin by importing the package and adding your API key.

.. code:: python

    import pyrai
    API_KEY = "your-api-key-here"

Once you have added your API key, you can create a fleet:

.. code:: python

    rai = pyrai.Pyrai(api_key=API_KEY)
    fleet = rai.create_sim_fleet()

You can also create a fleet directly from its API key and fleet key:

.. code:: python

    directly_created_fleet = pyrai.Fleet(api_key="api-key-here", fleet_key="fleet-key-here")

Vehicles
^^^^^^^^

Once you have a fleet, you can add, update, and remove vehicles from it:

.. code:: python

    fleet.make_vehicle_online(vid=1, location=Location(50, 7), capacity=4)
    veh = fleet.get_vehicle_info(1)

Vehicles adding, updating, and removing can be done either from the
fleet or the individual vehicles:

.. code:: python

    # These lines do the same thing
    veh.update(event=VehicleEvent.UNASSIGNED, location=Location(50,6), direction=0)
    fleet.update_vehicle(vid=1, location=Location(50, 6), direction=0, event=VehicleEvent.UNASSIGNED)




.. code:: python

    >>> {'fleet': {'api_key': 'your-api-key-here', 'fleet_key': '6b515268-6125-43b4-bd34-2ecdb112e9aa'}, 'veh_id': 1, 'location': {'lat': 50.748227, 'lng': 5.992767}, 'assigned': False, 'req_ids': [], 'events': []}



Vehicles are easy to take offline and/or remove:

.. code:: python

    veh.make_offline()
    veh.remove()

Requests
^^^^^^^^

Requests can be added, queried, and cancelled similar to vehicles.

.. code:: python

    fleet.add_request(rid=1,
                      pickup=Location(30,40),
                      dropoff=Location(40,50),
                      load=4)

.. code:: python

    req=fleet.get_request(1)

.. code:: python

    req.cancel()
    # Could also use fleet.cancel_request(rid=1)



Assignments
^^^^^^^^^^^

Once you have a fleet with requests and vehicles, you can use the API to
assign vehicles to requests.

.. code:: python

    import random
    fleet = rai.create_live_fleet()
    import random
    for v in range(20): # Add 20 random vehicles
      fleet.make_vehicle_online(v, 
          Location(50+random.gauss(0,1), 6+random.gauss(0,1)),
          4)
    for r in range(100): # Add 100 random requests
      fleet.add_request(rid=r,
                      pickup = Location(50+random.gauss(0,5), 6+random.gauss(0,5)),
                      dropoff = Location(50+random.gauss(0,5), 6+random.gauss(0,5)),
                      load = 4)
    fleet.get_assignments() # Get assignments




.. code:: python

    >>> {'vehs': [{'fleet': {'api_key': 'your-api-key-here', 'fleet_key': 'your-fleet-key-here'}, 'veh_id': 1, 'location': {'lat': 50.754699, 'lng': 5.681816}, 'assigned': True, 'req_ids': [80], 'events': [{'req_id': 80, 'location': {'lat': 50.754699, 'lng': 5.681816}, 'time': '2020-07-03T12:27:27Z', 'event': 'pickup'}, {'req_id': 80, 'location': {'lat': 51.541428, 'lng': 3.438608}, 'time': '2020-07-03T17:44:31Z', 'event': 'dropoff'}]}, {'fleet': {'api_key': 'your-api-key-here', 'fleet_key': 'your-fleet-key-here'}, 'veh_id': 17, 'location': {'lat': 50.751542, 'lng': 6.019059}, 'assigned': True, 'req_ids': [13], 'events': [{'req_id': 13, 'location': {'lat': 50.751542, 'lng': 6.019059}, 'time': '2020-07-03T12:27:27Z', 'event': 'pickup'}, {'req_id': 13, 'location': {'lat': 51.239186, 'lng': 3.42657}, 'time': '2020-07-03T18:33:33Z', 'event': 'dropoff'}]},..., {'fleet': {'api_key': 'your-api-key-here', 'fleet_key': 'your-fleet-key-here'}, 'veh_id': 3, 'location': {'lat': 50.753503, 'lng': 6.021277}, 'assigned': True, 'req_ids': [94], 'events': [{'req_id': 94, 'location': {'lat': 50.753503, 'lng': 6.021277}, 'time': '2020-07-03T12:27:27Z', 'event': 'pickup'}, {'req_id': 94, 'location': {'lat': 53.258865, 'lng': 7.267049}, 'time': '2020-07-03T20:12:17Z', 'event': 'dropoff'}]}], 'requests': [{'fleet': {'api_key': 'your-api-key-here', 'fleet_key': 'your-fleet-key-here'}, 'pickup': {'lat': 50.867703, 'lng': 6.091752}, 'dropoff': {'lat': 53.401362, 'lng': 5.25105}, 'request_time': '2020-07-03T12:26:47Z', 'req_id': 0, 'veh_id': 11, 'load': 4, 'assigned': True}, {'fleet': {'api_key': 'your-api-key-here', 'fleet_key': 'your-fleet-key-here'}, 'pickup': {'lat': 50.751542, 'lng': 6.019059}, 'dropoff': {'lat': 51.956534, 'lng': 6.823075}, 'request_time': '2020-07-03T12:26:47Z', 'req_id': 1, 'veh_id': -1, 'load': 4, 'assigned': False},..., {'fleet': {'api_key': 'your-api-key-here', 'fleet_key': 'your-fleet-key-here'}, 'pickup': {'lat': 51.302285, 'lng': 3.328629}, 'dropoff': {'lat': 50.748227, 'lng': 5.992767}, 'request_time': '2020-07-03T12:26:47Z', 'req_id': 99, 'veh_id': -1, 'load': 4, 'assigned': False}], 'notifications': []}



Forward Simulation
^^^^^^^^^^^^^^^^^^

Once you have assignments, you can forward simulate for a specified
duration

.. code:: python

    fleet.forward_simulate(duration="5m")

This updates the state of your vehicles and requests.

Visualization
^^^^^^^^^^^^^

Once you have a fleet that has accumulated events and run through a forward simulation, you can visualize the vehicles and requests:

.. code:: 

    fleet = pyrai.Fleet(api_key = "907fab5b-c35e-497f-988f-92fbb8835977", 
                  fleet_key = "8af41885-d9bf-465d-9746-e54d8147646d")
    fleet.visualize('2020-05-06T21:55:00Z',
                    '2020-05-06T22:55:00Z')




.. raw:: html

    
    <iframe
        width="100%"
        height="600"
        src="https://dashboard.routable.ai/pyraimap?start=2020-05-06T21:55:00Z&end=2020-05-06T22:55:00Z&api_key=907fab5b-c35e-497f-988f-92fbb8835977&fleet_key=8af41885-d9bf-465d-9746-e54d8147646d"
        frameborder="0"
        allowfullscreen
    ></iframe>




You can also plot various time series metrics:

.. code:: 

    fleet.plot_metrics([Metrics.PASSENGERS, Metrics.TOTAL_REQUESTS, Metrics.AVG_OCCUPANCY, Metrics.IDLE_VEHICLES], 
                      '2020-05-06T21:55:00Z',
                      '2020-05-06T22:55:00Z')



.. raw:: html

    <html>
    <head><meta charset="utf-8" /></head>
    <body>
        <div>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-AMS-MML_SVG"></script><script type="text/javascript">if (window.MathJax) {MathJax.Hub.Config({SVG: {font: "STIX-Web"}});}</script>
                    <script type="text/javascript">window.PlotlyConfig = {MathJaxConfig: 'local'};</script>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>    
                <div id="180a83a1-5c9a-4e58-b599-70b25490c5ae" class="plotly-graph-div" style="height:525px; width:100%;"></div>
                <script type="text/javascript">
    
                        window.PLOTLYENV=window.PLOTLYENV || {};
    
                    if (document.getElementById("180a83a1-5c9a-4e58-b599-70b25490c5ae")) {
                        Plotly.newPlot(
                            '180a83a1-5c9a-4e58-b599-70b25490c5ae',
                            [{"mode": "lines+markers", "name": "passengers", "type": "scatter", "x": ["2020-05-06T21:55:00Z", "2020-05-06T22:00:00Z", "2020-05-06T22:05:00Z", "2020-05-06T22:10:00Z", "2020-05-06T22:15:00Z", "2020-05-06T22:20:00Z", "2020-05-06T22:25:00Z", "2020-05-06T22:30:00Z", "2020-05-06T22:35:00Z", "2020-05-06T22:40:00Z", "2020-05-06T22:45:00Z", "2020-05-06T22:50:00Z"], "y": [2, 5, 7, 12, 20, 17, 16, 16, 13, 13, 17, 14]}, {"mode": "lines+markers", "name": "total_requests", "type": "scatter", "x": ["2020-05-06T21:55:00Z", "2020-05-06T22:00:00Z", "2020-05-06T22:05:00Z", "2020-05-06T22:10:00Z", "2020-05-06T22:15:00Z", "2020-05-06T22:20:00Z", "2020-05-06T22:25:00Z", "2020-05-06T22:30:00Z", "2020-05-06T22:35:00Z", "2020-05-06T22:40:00Z", "2020-05-06T22:45:00Z", "2020-05-06T22:50:00Z"], "y": [8, 16, 22, 36, 43, 48, 59, 65, 77, 91, 98, 112]}, {"mode": "lines+markers", "name": "avg_occupancy", "type": "scatter", "x": ["2020-05-06T21:55:00Z", "2020-05-06T22:00:00Z", "2020-05-06T22:05:00Z", "2020-05-06T22:10:00Z", "2020-05-06T22:15:00Z", "2020-05-06T22:20:00Z", "2020-05-06T22:25:00Z", "2020-05-06T22:30:00Z", "2020-05-06T22:35:00Z", "2020-05-06T22:40:00Z", "2020-05-06T22:45:00Z", "2020-05-06T22:50:00Z"], "y": [0.25, 1.625, 1.85, 2.078333333333334, 4.166666666666667, 4.466666666666667, 4.05, 4.033333333333334, 2.9333333333333327, 2.9166666666666665, 4.000000000000001, 4.133333333333333]}, {"mode": "lines+markers", "name": "idle_vehicles", "type": "scatter", "x": ["2020-05-06T21:55:00Z", "2020-05-06T22:00:00Z", "2020-05-06T22:05:00Z", "2020-05-06T22:10:00Z", "2020-05-06T22:15:00Z", "2020-05-06T22:20:00Z", "2020-05-06T22:25:00Z", "2020-05-06T22:30:00Z", "2020-05-06T22:35:00Z", "2020-05-06T22:40:00Z", "2020-05-06T22:45:00Z", "2020-05-06T22:50:00Z"], "y": [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}],
                            {"template": {"data": {"bar": [{"error_x": {"color": "#2a3f5f"}, "error_y": {"color": "#2a3f5f"}, "marker": {"line": {"color": "#E5ECF6", "width": 0.5}}, "type": "bar"}], "barpolar": [{"marker": {"line": {"color": "#E5ECF6", "width": 0.5}}, "type": "barpolar"}], "carpet": [{"aaxis": {"endlinecolor": "#2a3f5f", "gridcolor": "white", "linecolor": "white", "minorgridcolor": "white", "startlinecolor": "#2a3f5f"}, "baxis": {"endlinecolor": "#2a3f5f", "gridcolor": "white", "linecolor": "white", "minorgridcolor": "white", "startlinecolor": "#2a3f5f"}, "type": "carpet"}], "choropleth": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "choropleth"}], "contour": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "contour"}], "contourcarpet": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "contourcarpet"}], "heatmap": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "heatmap"}], "heatmapgl": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "heatmapgl"}], "histogram": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "histogram"}], "histogram2d": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "histogram2d"}], "histogram2dcontour": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "histogram2dcontour"}], "mesh3d": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "mesh3d"}], "parcoords": [{"line": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "parcoords"}], "pie": [{"automargin": true, "type": "pie"}], "scatter": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatter"}], "scatter3d": [{"line": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatter3d"}], "scattercarpet": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattercarpet"}], "scattergeo": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattergeo"}], "scattergl": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattergl"}], "scattermapbox": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattermapbox"}], "scatterpolar": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterpolar"}], "scatterpolargl": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterpolargl"}], "scatterternary": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterternary"}], "surface": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "surface"}], "table": [{"cells": {"fill": {"color": "#EBF0F8"}, "line": {"color": "white"}}, "header": {"fill": {"color": "#C8D4E3"}, "line": {"color": "white"}}, "type": "table"}]}, "layout": {"annotationdefaults": {"arrowcolor": "#2a3f5f", "arrowhead": 0, "arrowwidth": 1}, "coloraxis": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "colorscale": {"diverging": [[0, "#8e0152"], [0.1, "#c51b7d"], [0.2, "#de77ae"], [0.3, "#f1b6da"], [0.4, "#fde0ef"], [0.5, "#f7f7f7"], [0.6, "#e6f5d0"], [0.7, "#b8e186"], [0.8, "#7fbc41"], [0.9, "#4d9221"], [1, "#276419"]], "sequential": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "sequentialminus": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]]}, "colorway": ["#636efa", "#EF553B", "#00cc96", "#ab63fa", "#FFA15A", "#19d3f3", "#FF6692", "#B6E880", "#FF97FF", "#FECB52"], "font": {"color": "#2a3f5f"}, "geo": {"bgcolor": "white", "lakecolor": "white", "landcolor": "#E5ECF6", "showlakes": true, "showland": true, "subunitcolor": "white"}, "hoverlabel": {"align": "left"}, "hovermode": "closest", "mapbox": {"style": "light"}, "paper_bgcolor": "white", "plot_bgcolor": "#E5ECF6", "polar": {"angularaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "bgcolor": "#E5ECF6", "radialaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}}, "scene": {"xaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}, "yaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}, "zaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}}, "shapedefaults": {"line": {"color": "#2a3f5f"}}, "ternary": {"aaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "baxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "bgcolor": "#E5ECF6", "caxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}}, "title": {"x": 0.05}, "xaxis": {"automargin": true, "gridcolor": "white", "linecolor": "white", "ticks": "", "title": {"standoff": 15}, "zerolinecolor": "white", "zerolinewidth": 2}, "yaxis": {"automargin": true, "gridcolor": "white", "linecolor": "white", "ticks": "", "title": {"standoff": 15}, "zerolinecolor": "white", "zerolinewidth": 2}}}},
                            {"responsive": true}
                        ).then(function(){
    
    var gd = document.getElementById('180a83a1-5c9a-4e58-b599-70b25490c5ae');
    var x = new MutationObserver(function (mutations, observer) {{
            var display = window.getComputedStyle(gd).display;
            if (!display || display === 'none') {{
                console.log([gd, 'removed!']);
                Plotly.purge(gd);
                observer.disconnect();
            }}
    }});
    
    // Listen for the removal of the full notebook cells
    var notebookContainer = gd.closest('#notebook-container');
    if (notebookContainer) {{
        x.observe(notebookContainer, {childList: true});
    }}
    
    // Listen for the clearing of the current output cell
    var outputEl = gd.closest('.output');
    if (outputEl) {{
        x.observe(outputEl, {childList: true});
    }}
    
                            })
                    };
    
                </script>
            </div>
    </body>
    </html>

