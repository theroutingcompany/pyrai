from dateutil.parser import isoparse
from pyrai.dispatcher.structures.metrics import Metrics
from pyrai.dispatcher.structures.endpoints import Endpoints
import plotly.graph_objects as go
from pyrai.helpers import to_rfc3339
import requests

def plot_metrics(self, metrics, start_time=None, end_time=None):
    """
    Plots time series metrics.

    Args:
        metrics (list[Metrics]): A list of metrics to plot.
        start_time (datetime.datetime or str): The start time, either as a datetime.datetime object or an ISO string. Set to the fleet creation time if not set. Defaults to None.
        end_time (datetime.datetime or str): The end time, either as a datetime.datetime object or an ISO string. Set to the latest API call time if not set. Defaults to None.

    Returns:
        Plotly.Figure: A figure that graphs the metrics
            over the time interval.
    """
    if start_time is None:
        start_time = self.start_time
    
    if end_time is None:
        end_time = self.end_time

    if isinstance(start_time, str):
        start_time = isoparse(start_time)

    if isinstance(end_time, str):
        end_time = isoparse(end_time)

    url = self.build_url(Endpoints.GRAPHQL)
    query = Metrics.QUERY.format(
        api_key = self.api_key,
        fleet_key = self.fleet_key,
        start_time = to_rfc3339(start_time),
        end_time = to_rfc3339(end_time)
    )
    r = requests.post(url, json={"query": query})
    resp = r.json()
    data = resp['data']['live_fleets'][0]['metrics']
    x = [met[Metrics.TIME] for met in data]
    figure = go.Figure()
    for metric in metrics:
        figure.add_trace(go.Scatter(x=x, y=[met[metric] for met in data],
                    mode='lines+markers',
                    name=metric))
    return figure