import sys


FEATURE_REQUIREMENTS = {
    "direct_upload": {
        "enabled": "{{ cookiecutter.direct_upload }}" == "enabled",
        "requires": {
            "vue": "{{ cookiecutter.vue }}" == "enabled",
            "django_storages": "{{ cookiecutter.django_storages }}" == "enabled",
            "reference_examples": "{{ cookiecutter.reference_examples }}" == "on",
        },
    },
}


def main():
    errors = []
    for feature, config in FEATURE_REQUIREMENTS.items():
        if not config["enabled"]:
            continue
        for requirement, satisfied in config["requires"].items():
            if not satisfied:
                errors.append(f"`{feature}` requires `{requirement}` to be enabled")
    if errors:
        print("\nInvalid feature selection:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
