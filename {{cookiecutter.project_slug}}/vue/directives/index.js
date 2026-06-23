{%- if cookiecutter.vue == "enabled" %}
{%- if cookiecutter.feature_annotations == "on" %}
// START_FEATURE vue
{%- endif %}
const modules = import.meta.glob("./*.js", { eager: true })
const components = {}

for (const path in modules) {
  // Extract the file name without extension
  const name = path.match(/\.\/(.*)\.js$/)[1]
  components[name] = modules[path].default
}

export default components
{%- if cookiecutter.feature_annotations == "on" %}
// END_FEATURE vue
{%- endif %}
{%- endif %}
