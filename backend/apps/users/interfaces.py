import logging

import subscriptions.apis as sub_api

logger = logging.getLogger(__name__)


class SubscriptionsInterface:
    def check_is_subscribed(self, user: int, author: int) -> dict:
        logger.info('Метод SubscriptionsInterface check_is_subscribed вызван из users')
        return sub_api.SubscriptionsAPI().check_is_subscribed(user=user, author=author).data
