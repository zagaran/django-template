# How To Use This Template

This template is a [cookiecutter](https://github.com/cookiecutter/cookiecutter) template.  Create a project from it using the following:
```
pip install "cookiecutter>=1.7.0"
cookiecutter https://github.com/zagaran/django-template
```

The cookiecutter command will give you an interactive prompt to choose which optional features to inlcude (see below)

Once you have cloned the project, [create a virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment)

Then run the following:

```
pip install pip-tools
pip-compile requirements.in --upgrade
pip-compile requirements-dev.in --upgrade
pip install -r requirements-dev.txt
cp config/.env.example config/.env
python manage.py makemigrations

# If using the `elastic_beanstalk` feature
git add --chmod=+x -- .platform///*.sh

# Then see the generated README in your new project for the rest of the local setup instructions
```

If you have an existing project, you can see a project based on this template here: https://github.com/zagaran/sample-django-app

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

The reference examples also include the `app/` Django app (a sample model, dashboard, and CRUD views). When reference
examples are off, `app/` is not generated.


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
- `react/`

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
  - Note that calling `nwb build` does not remove existing compiled data from your static folder. If you are building 
  static assets locally and committing them to the repo rather than implementing a deploy compilation step, it is import 
  to delete `/static/webpack_bundles` (in addition to wherever your existing static files are, e.g. 
  `/staticfiles/webpack_bundles`) before running another build, as even without code changes NWB will generate new 
  compiled JS files without removing the old ones. If you have implemented a `collecstatic` step in your deployment,
  ensure that existing webpack bundles are deleted before the new assets are generated by NWB.

### Other notes

- If you use `nwb serve` in your local development environment, you may see a persistent XHR error in the console -- a
request by the app to something like `http://localhost:8000/sockjs-node/info?t=123456789`. This is normal and will
not appear on production or otherwise effect the function of your app - it is because the React components are being
served by the browser in a different environment than the React components expect to be in.


## AWS SES integration (`django_ses`)


## Third-party authentication integrations (`django_social`)


## AWS S3 (or other cloud blob storage) integration (`django_storages`)

## Direct file uploads (`direct_upload`)

This feature lets users upload files from the browser directly to S3 (via presigned URLs), rather than streaming the
file through the Django server. It requires the `django_storages`, `vue`, and `reference_examples` features
(`Attachment` and the upload views live in the reference `app/`); generation fails if any of them is disabled.

### What's included

- `common.models.UploadFile`: an abstract model with a `file` field, upload/deletion timestamps, and helpers
  (`download_file`, `view_file`) that return a response for downloading or viewing the file inline. It has no foreign
  keys; subclasses decide how files are attached to other data.
- `app.models.Attachment`: a concrete `UploadFile` owned by a user, used by the reference examples.
- `app.fields.DirectUploadFileField`: a form field (a `ModelMultipleChoiceField`) that renders an upload dashboard, so
  users can upload new files and select existing ones in a normal Django form. It accepts `allowed_file_types`,
  `max_number_of_files`, and `max_file_size` (in bytes).
- Upload views and URLs in `app/views.py` and `app/urls.py`, plus the `AttachmentSerializer` in `app/serializers.py`.
- The `FileUploadDashboard` and `FileUploadDirect` Vue components in `vue/components/direct_upload/`, built on
  [Uppy](https://uppy.io/).
- `common/utils/file_utils.py`: file name and presigned URL helpers.

### How an upload works

1. The client POSTs the file name to `attachments/upload-start/`. This creates an `Attachment` and returns an upload URL
   and an upload-complete URL.
2. The client uploads the file to the upload URL. On servers this is a presigned S3 `PUT` URL. On localhost, files are
   stored with `FileSystemStorage` and the upload URL is a Django view that saves the streamed file.
3. The client POSTs to the upload-complete URL, which marks the attachment complete. It can also pass a `relations`
   JSON object (e.g. `{"sample_objects": "<id>"}`) to link the attachment to other objects. An invalid relation or pk
   returns a 400 response.

Attachments whose upload never completes are ignored by the dashboard and form field.

### Usage

```python
from app.fields import DirectUploadFileField
from app.models import Attachment


class MyForm(forms.ModelForm):
    attachments = DirectUploadFileField(
        queryset=Attachment.objects.filter(deleted_on=None),
        allowed_file_types=["pdf", "docx"],
        max_file_size=10 * 1024 * 1024,
        required=False,
    )
```

### S3 setup

The browser uploads straight to the bucket, so the bucket needs a CORS rule that allows `PUT` from your site's origin
and exposes the `ETag` header. For example:

```json
[
  {
    "AllowedHeaders": ["*"],
    "AllowedMethods": ["PUT"],
    "AllowedOrigins": ["https://your-domain.example.com"],
    "ExposeHeaders": ["ETag"]
  }
]
```

## Docker integration (`docker`)


## Elastic Beanstalk deployment (`elastic_beanstalk`)

As a default for web applications, we recommend using Elastic Beanstalk.

To create a new deployment, [set up your local AWS credentials](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-profiles.html) e.g. ~/.aws/config,

Ensure shell files in the `.platform` directory are executable according to git.
You can check if they are executable via `git ls-files -s .platform`;
you should see `100755` before any shell files in the output of this command.
If you see `100644` before any of your shell files,
run `git add --chmod=+x -- .platform/*/*/*.sh` to make them executable.

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

## ECS deployment (`ecs`)

An alternative deployment strategy is to use ECS (Elastic Container Service). This feature provides ECS deployment 
support using terraform to provision AWS resources. It is not valid to enable both elastic beanstalk and ECS, or to 
enable ECS without enabling docker. See the project readme for deployment details. The deployment will include both a 
web and worker server if celery is enabled, and a web server only if disabled. The ECS configuration without celery 
enabled has not been extensively tested, so tweaks may be needed.

## Celery (`celery`)

Celery is a framework for running asynchronous and scheduled tasks. Note: This feature has only been tested with ECS 
deployments enabled. If enabled, the ECS deployment will include a worker server and redis queue.

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

## Vue.js (`vue`)

This feature adds [Vue 3](https://vuejs.org/), built with [Vite](https://vite.dev/). Vue components are used directly
in Django templates, rather than in a separate single-page app.

### Files

- `vite.config.js`: the build config. Output goes to `static/js/dist/`.
- `vue/pages/`: each `.js` file here is a build entrypoint. The base template loads `pages/default.js` by default; to
  use a different entrypoint on a page, override the `bottom_javascript` block.
- `vue/components/` and `vue/directives/`: every component (including those in subdirectories) and directive here is
  registered globally by `vue/main.js`, using its file name.
- `vue/composables/`: shared helpers, such as `useFetch` (which adds the CSRF token to POST requests).
- `common/templatetags/vue.py`: template filters (`{% load vue %}`), including `jsonify` for passing context data to
  component props, e.g. `:files="{{ attachments|jsonify }}"`.

### How it works

`pages/default.js` mounts a Vue app on the `#app` element in `base_templates/base.html`, which wraps the `body` block.
This means the whole page body is compiled as a Vue template, so any registered component can be used in any template.

Because the page body is a Vue template, never render user-supplied content inside `#app` that could contain Vue
template syntax (e.g. `{{ }}`) without wrapping it in an element with `v-pre`.

### Running

Install Node dependencies with `npm install`, then:

```
npm run vue-dev    # Build in development mode and rebuild on changes
npm run vue-build  # Production build
```

Run the production build before `collectstatic` when deploying. If `docker` is enabled, the `Dockerfile` does this.


# Optional Settings

`MAINTENANCE_MODE`: Set this flag on a server environment to stop all user requests to the site, such as when you need to make substantial server updates or run a complex database migration.
