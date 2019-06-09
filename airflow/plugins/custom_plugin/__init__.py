from airflow.plugins_manager import AirflowPlugin
from custom_plugin.operators.extended_http_operator import ExtendedHttpOperator

"""
Includes Operators that extends the base airflow classes with our own requirements
"""
class CustomPlugin(AirflowPlugin):
  name = "custom_plugin"
  operators = [ExtendedHttpOperator]