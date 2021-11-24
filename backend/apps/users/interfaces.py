import logging

import subscriptions.apis as sub_api

logger = logging.getLogger(__name__)


class SubscriptionsInterface:
    def check_is_subscribed(self, user: int, author: int) -> bool:
        return sub_api.SubscriptionsAppAPI().check_is_subscribed(user=user, author=author)
