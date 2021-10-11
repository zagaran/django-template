from common.middleware.maintenance_mode_middleware import MaintenanceModeMiddleware
{%- if cookiecutter.user_action_tracking == "enabled" %}
{%- if cookiecutter.feature_annotations == "on" %}
# START_FEATURE user_action_tracking
{%- endif %}
from common.middleware.user_action_tracking import UserActionTrackingMiddleware
{%- if cookiecutter.feature_annotations == "on" %}
# END_FEATURE user_action_tracking
{%- endif %}
{%- endif %}
