# How To Use This Template

1. Reset the git history to start your project.
```
# reset the git history
rm -rf .git
git init
git branch -M main
git add .
git commit -m "init"
git remote add origin [REMOTE_URL]
git push -u origin main
```
2. Decide which optional features you'd like to use.


# Included Optional Features

There are a number of optional features that are present in this template.  You will be prompted for whether to include each one as part of running `cookiecutter`.

## `feature_annotations` (off by default)

If you turn feature annotations on, the code for each optional feature will be bracketed by comments such as
`# START_FEATURE feature_name` and `# END_FEATURE feature_name`.


## `reference_examples` (on by default)
If you turn on reference examples, the codebase will have a number of reference examples.  These are all marked with one of the following comments:

```
# TODO: delete me; this is just a reference example
// TODO: delete me; this is just a reference example
{# TODO: delete me; this is just a reference example #}
```


## Django messages integration with Bootstrap (`bootstrap_messages`)


## Crispy Forms integration (`crispy_forms`)


## Debug Toolbar integration (`debug_toolbar`)


## Django-React integration, aka Djangre (`django_react`)

### Files

The following files and folders are only needed if `django_react` is a desired feature in your app and can be safely
deleted from projects which do not leverage the feature.

- `nwb.config.js`
- `package.json`
- `webpack-stats.json`
- `config/webpack_loader.py`
- `src/`

### Additional Setup

When using this feature, make sure to install the Node.js requirements using the manager of your choice
(either `npm install` or `yarn install` will work) before proceeding with development.

### Special Consideration for Running

For development on localhost when using Django-React, you should run the following command in a separate terminal to
your standard `runserver` command.

```
nwb serve --no-vendor  # Note: refer to the nwb docs on when to use --no-vendor vs not
```

If you have configured everything correctly, you should see each command complete and notify you
that the project is ready to be viewed.

- If you include `nwb` as a dependency, you can use the locally-installed `nwb` by running `node_modules/.bin/nwb serve --no-vendor` instead of relying on a globally installed `nwb`.

### Adding a new React component

In this paradigm, React components are compiled and injected into the standard Django template. This means we can take
advantage of the built-in templating functionality of Django and, with a bit of elbow grease, use the power of React to
make those templates responsive.

`django-react-loader` uses the same basic pattern for any component:

1. First, ensure that the library is loaded in your template: `{% load django_react_components %}`
2. Next, ensure that you have rendered the React runtime bundle: `{% render_bundle 'runtime' %}`
   - Note that you only have to do this once per page where React components will be used.
3. Finally, load your React component on the page. `{% react_component 'Component' %}`
    - You can add any number of props as named keywords, e.g. `{% react_component 'Home' id='home' prop1=value_from_context %}`
    - You can also choose to pass props as an object instead of individual kwargs, e.g. `{% react_component 'Hello' id='hello' props=sample_props %}`.

### Preparing for deployment

The preferred option for deployment is to add the below compilation step to the deployment configuration rather than
building it locally. However, if you wish to build the app locally:

- run `nwb build --no-vendor`. This will generate or replace a `webpack_bundles` folder in your `/static` folder
  populated with the compiled React components. This then allows `collectstatic` to collect these static assets and
  make them available via the usual static assets pipeline set up in the deploy configuration.

### Other notes

- If you use `nwb serve` in your local development environment, you may see a persistent XHR error in the console -- a
request by the app to something like `http://localhost:8000/sockjs-node/info?t=123456789`. This is normal and will
  not appear on production or otherwise affect the function of your app. It is an artifact of the context bending we are
  doing by placing a React component outside the context of its expected Node environment.

- Note that calling `nwb build` does not remove existing compiled data from your static folder -- it may be worth deleting
`/static/webpack_bundles` before running a build for a deploy, as otherwise your package may become heavier than it
needs to be.
   - If you find that the number of files collected by `python manage.py collectstatic` continues to grow, this may be
    a sign that you should consider deleting the generated files and the `staticfiles` directory and starting with a
     fresh `python manage.py collectstatic`. This is another reason to prefer adding a compilation step to your deployment
     pipeline rather than running it locally.

## AWS SES integration (`django_ses`)


## Third-party authentication integrations (`django_social`)


## AWS S3 (or other cloud blob storage) integration (`django_storages`)

## Docker integration (`docker`)


## Elastic Beanstalk deployment (`elastic_beanstalk`)

As a default for web applications, we strongly recommend using Elastic Beanstalk.

To create a new deployment, [set up your local AWS credentials](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-profiles.html) e.g. ~/.aws/config,

Set desired parameters `.elasticbeanstalk/eb-create-environment.yml`

Use [eb-create-environment](https://github.com/zagaran/eb-create-environment/):
```
eb-create-environment --config .elasticbeanstalk/eb-create-environment.yml
```

To update an existing deployment
```
eb deploy [ENVIRONMENT_NAME]
```

To SSH into a deployment

Use [eb-ssm](https://github.com/zagaran/eb-ssm/):
```
eb-ssm [ENVIRONMENT_NAME]
```

## Pre-commit hooks (`pre_commit`)
You can configure pre-commit with `.pre-commit-config.yaml`

See https://pre-commit.com/hooks.html for more hook options.

To run style checks and desired formatters:
```
pre-commit run --all-files
```
If wish to install pre-commit as a pre-commit git hook, you can run (optional):
```
pre-commit install
```


## Sass compilation (`sass_bootstrap`)

Use this feature to enable Sass processing and Bootstrap styling.

While you can just include Bootstrap's styling/js via a CDN, using this feature allows you to customize Bootstrap to the
style guide of your project, as well as define custom styling in a cleaner and more maintainable way (compared to plain
CSS). The Bootstrap part of this integration could be swapped out for any other frontend styling framework that also
uses Sass, but there really is no reason to write vanilla CSS.

In local development, you can simply write scss files and include them using `sass_tags` and your stylesheets should
automatically recompile in reload. This also works seamlessly with `collectstatic` for deploys.

Note: If you aren't already using npm to install bootstrap, you can alternatively clone the contents of Bootstrap's sass
files directly into your static directory and change your references to point there. There is currently no good way to
install Bootstrap source code using just python.

### Production notes

In development, `.scss` files are compiled on the fly. However, when deploying, these files must be manually generated
using `python manage.py compilescss`. Also note that if your styles folder is in a directory that's collected with
`collectstatic`, you should add the `--ignore *.scss` flag to avoid exposing the raw `.scss` files as staticfiles.


## Security settings (`security_settings`)
These are the recommended security settings. [Explanations for all Django settings can be found here](https://docs.djangoproject.com/en/3.2/ref/settings/). Please pay particular note to what are appropriate cookie and subdomain settings for your application.

## Sentry integration (`sentry`)


## User Action Tracking (`user_action_tracking`)

This feature tracks all URLs accessed by users (along with the status code and user agent) in a table called `UserAction`.
This can be useful for debugging, for analytics, or for auditing.  There is a setting `USER_TRACKING_EXEMPT_ROUTES` where
you can add the names of routes that should be excluded from action tracking because they would not be useful
(for example, if your site has a keep_alive route that the frontend regulalry hits automatically).  Note that only
actions by authenticated users are tracked.

# Optional Settings

`MAINTENANCE_MODE`: Set this flag on a server environment to stop all user requests to the site, such as when you need to make substantial server updates or run a complex database migration.
