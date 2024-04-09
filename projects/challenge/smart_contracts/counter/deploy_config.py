import logging

import algokit_utils
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient
from algosdk import account

logger = logging.getLogger(__name__)


# define deployment behaviour based on supplied app spec
def deploy(
    algod_client: AlgodClient,
    indexer_client: IndexerClient,
    app_spec: algokit_utils.ApplicationSpecification,
    deployer: algokit_utils.Account,
) -> None:
    from smart_contracts.artifacts.counter.client import (
        CounterClient,
    )

    app_client = CounterClient(
        algod_client,
        creator=deployer,
        indexer_client=indexer_client,
    )

    app_client.app_client.create()

    app_client.opt_in_bare()

    logger.info("----Account 1 incrementing----")

    for i in range(3):
        response = app_client.increment()
        logger.info(f"Incremented by 1 and now the count is {response.return_value}")

    account2 = algokit_utils.get_localnet_default_account(algod_client)

    app_client2 = CounterClient(
        algod_client,
        app_id=app_client.app_id,
        signer=account2,
        sender=account2.address,
    )

    app_client2.opt_in_bare()

    logger.info("----Account 2 incrementing----")

    for i in range(4):
        response = app_client2.increment()
        logger.info(f"Incremented by 1 and now the count is {response.return_value}")

    response = app_client.get_global_state()
    logger.info(f"Total # of counters: {response.counters} people")
