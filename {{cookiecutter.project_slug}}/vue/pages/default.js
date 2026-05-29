{%- if cookiecutter.vue == "enabled" %}
{%- if cookiecutter.feature_annotations == "on" %}
// START_FEATURE vue
{%- endif %}
import { createApp } from "vue"
import MainVueApp from "../main"

createApp({}).use(MainVueApp).mount("#app")
{%- if cookiecutter.feature_annotations == "on" %}
// END_FEATURE vue
{%- endif %}
{%- endif %}
