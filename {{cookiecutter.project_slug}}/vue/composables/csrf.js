{%- if cookiecutter.vue == "enabled" %}
{%- if cookiecutter.feature_annotations == "on" %}
// START_FEATURE vue
{%- endif %}
import { onMounted, ref } from "vue"

export function useCSRF() {
  const csrf = ref(null)
  onMounted(() => {
    csrf.value = window.csrfmiddlewaretoken
  })
  return { csrf }
}
{%- if cookiecutter.feature_annotations == "on" %}
// END_FEATURE vue
{%- endif %}
{%- endif %}
