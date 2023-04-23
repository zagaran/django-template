import pytest
from django.urls import reverse, resolve

from common import views


class TestClass:

    @pytest.mark.parametrize(
        "url_name, url, view_class",
        [
            ("index", "/", views.IndexView),
        ],
    )
    def test_urls(self, url_name, url, view_class):
        resolver = resolve(url)
        assert resolver.view_name == url_name
        assert resolver.func.view_class == view_class
