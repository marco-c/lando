from unittest import mock

from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT

from lando.api.legacy.projects import SEC_PROJ_SLUG, get_project_phid


def test_get_project_phid_caches_found_project_for_long(phabdouble):
    phab = phabdouble.get_phabricator_client()

    with mock.patch.object(cache, "set") as cache_set:
        phid = get_project_phid(SEC_PROJ_SLUG, phab)

    assert phid is not None
    cache_set.assert_called_once_with(
        f"PROJECT_{SEC_PROJ_SLUG}",
        phid,
        settings.PHABRICATOR_PROJECT_PHID_CACHE_TIMEOUT,
    )


def test_get_project_phid_caches_missing_project_for_default_timeout(phabdouble):
    phab = phabdouble.get_phabricator_client()

    with mock.patch.object(cache, "set") as cache_set:
        phid = get_project_phid("does-not-exist", phab)

    assert phid is None
    cache_set.assert_called_once_with("PROJECT_does-not-exist", None, DEFAULT_TIMEOUT)
