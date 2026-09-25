const modules = import.meta.glob("./**/*.vue", { eager: true })
const components = {}

for (const path in modules) {
  // Register each component by its file name, regardless of subdirectory
  const name = path.match(/([^/]*)\.vue$/)[1]
  components[name] = modules[path].default
}

export default components
