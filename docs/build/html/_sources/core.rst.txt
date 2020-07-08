Core
====

Defaults
--------
.. autoclass:: pyrai.api.Defaults
    :members:

.. py:data:: Defaults.BASE_URL
    :type: Defaults
    :value: "https://api.routable.ai"
.. py:data:: Defaults.VISUALIZATION_URL
    :type: Defaults
    :value: "https://dashboard.routable.ai/pyraimap?start={start}&end={end}&api_key={api_key}&fleet_key={fleet_key}"

Pyrai 
-----
.. autoclass:: pyrai.api.Pyrai
    :members:

Fleets
------
.. autoclass:: pyrai.api.Fleet
    :members:

Locations
---------
.. autoclass:: pyrai.api.Location
    :members:

Vehicles
--------
.. autoclass:: pyrai.api.Vehicle
    :members:

Events
^^^^^^
.. autoclass:: pyrai.api.Event
    :members:

VehicleEvents
^^^^^^^^^^^^^
.. autoclass:: pyrai.api.VehicleEvent
    :members:

.. py:data:: VehicleEvent.PICKUP
    :type: VehicleEvent
    :value: "pickup"

.. py:data:: VehicleEvent.DROPOFF
    :type: VehicleEvent
    :value: "dropoff"

.. py:data:: VehicleEvent.PROGRESS
    :type: VehicleEvent
    :value: "progress"

.. py:data:: VehicleEvent.UNASSIGNED
    :type: VehicleEvent
    :value: "unassigned"

Requests
--------
.. autoclass:: pyrai.api.Request
    :members:

Assignments
-----------
.. autoclass:: pyrai.api.VehicleAssignments
    :members:

Notifications
^^^^^^^^^^^^^
.. autoclass:: pyrai.api.Notification
    :members:

NotificationData
""""""""""""""""
.. autoclass:: pyrai.api.NotificationData
    :members:

Responses
---------
.. autoclass:: pyrai.api.StatusResponse
    :members:

.. autoclass:: pyrai.api.StatusError
    :members:

Metrics
-------
.. autoclass:: pyrai.api.Metrics
    :members:

.. py:data:: Metrics.TIME
    :type: Metrics
    :value: "time"

.. py:data:: Metrics.PASSENGERS
    :type: Metrics
    :value: "passengers"

.. py:data:: Metrics.WAITING_REQUESTS
    :type: Metrics
    :value: "waiting_requests"
    
.. py:data:: Metrics.ACTIVE_REQUESTS
    :type: Metrics
    :value: "active_requests"
    
.. py:data:: Metrics.DROPPED_REQUESTS
    :type: Metrics
    :value: "dropped_requests"
    
.. py:data:: Metrics.CANCELED_REQUESTS
    :type: Metrics
    :value: "canceled_requests"
    
.. py:data:: Metrics.TOTAL_REQUESTS
    :type: Metrics
    :value: "total_requests"
    
.. py:data:: Metrics.ASSIGNED_VEHICLES
    :type: Metrics
    :value: "assigned_vehicles"
    
.. py:data:: Metrics.IDLE_VEHICLES
    :type: Metrics
    :value: "idle_vehicles"
    
.. py:data:: Metrics.REBALANCING_VEHICLES
    :type: Metrics
    :value: "rebalancing_vehicles"
    
.. py:data:: Metrics.OFFLINE_VEHICLES
    :type: Metrics
    :value: "offline_vehicles"
    
.. py:data:: Metrics.AVG_WAIT
    :type: Metrics
    :value: "avg_wait"
    
.. py:data:: Metrics.AVG_DELAY
    :type: Metrics
    :value: "avg_delay"
    
.. py:data:: Metrics.AVG_OCCUPANCY
    :type: Metrics
    :value: "avg_occupancy"
    
.. py:data:: Metrics.SERVICE_RATE
    :type: Metrics
    :value: "service_rate"
    