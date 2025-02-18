import logging

from django.core.cache import cache

from nautobot.core.utils.config import get_settings_or_config
from nautobot.core.tasks import get_releases

logger = logging.getLogger(__name__)


def get_latest_release(pre_releases=False):
    """
    Get latest known Nautobot release from cache, or if not available, queue up a background task to populate the cache.

    Returns:
        (Version, str): Latest release version and the release URL, if found in the cache
        ("unknown", None): If not present in the cache at this time
    """
    if get_settings_or_config("RELEASE_CHECK_URL"):
        logger.debug("Checking for most recent release")
        latest_release = cache.get("latest_release")
        if latest_release is not None:
            logger.debug(f"Found cached release: {latest_release}")
            return latest_release
        # Get the releases in the background worker, it will fill the cache
        logger.info("Initiating background task to retrieve updated releases list")
        get_releases.delay(pre_releases=pre_releases)

    else:
        logger.debug("Skipping release check; RELEASE_CHECK_URL not defined")

    return "unknown", None
