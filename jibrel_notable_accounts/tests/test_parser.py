import pytest
from aiopg.sa import Engine

from requests_mock import Mocker

from jibrel_notable_accounts import settings
from jibrel_notable_accounts.common.tables import notable_accounts_t
from jibrel_notable_accounts.parser.structs import NotableAccount, AccountList
from jibrel_notable_accounts.tests.plugins.types import HtmlGetter

from jibrel_notable_accounts.parser.service import ParserService


async def test_parser_extracts_labels_links_from_label_cloud(
        parser: ParserService,
        requests_mock: Mocker,
        get_html: HtmlGetter,
) -> None:

    requests_mock.register_uri('GET', settings.ES_LABEL_CLOUD_URL, text=get_html('label-cloud.html'))

    accounts_lists = await parser.get_accounts_lists()

    assert set(accounts_lists) == {
        AccountList(url='/accounts/label/0x-ecosystem', label='0x Ecosystem'),
        AccountList(url='/accounts/label/0xuniverse', label='0xUniverse'),
        AccountList(url='/accounts/label/abcc', label='ABCC'),
        AccountList(url='/accounts/label/advertising', label='Advertising'),
        AccountList(url='/accounts/label/airswap', label='AirSwap'),
        AccountList(url='/accounts/label/allbit', label='Allbit'),
        AccountList(url='/accounts/label/bancor', label='Bancor'),
        AccountList(url='/accounts/label/basic-attention-token', label='Basic Attention Token'),
        AccountList(url='/accounts/label/bgogo', label='Bgogo'),
        AccountList(url='/accounts/label/binance', label='Binance'),
        AccountList(url='/accounts/label/bitfinex', label='Bitfinex'),
        AccountList(url='/accounts/label/bithumb', label='Bithumb'),
        AccountList(url='/accounts/label/bitmart', label='BitMart'),
        AccountList(url='/accounts/label/bitmax-io', label='BitMax.io'),
        AccountList(url='/accounts/label/bittrex', label='Bittrex'),
        AccountList(url='/accounts/label/blockchain-cuties', label='Blockchain Cuties'),
        AccountList(url='/accounts/label/bloom', label='Bloom'),
        AccountList(url='/accounts/label/bugs', label='Bugs'),
        AccountList(url='/accounts/label/chibi-fighters', label='Chibi Fighters'),
        AccountList(url='/accounts/label/cobinhood', label='Cobinhood'),
        AccountList(url='/accounts/label/coinbit', label='Coinbit'),
        AccountList(url='/accounts/label/cold-wallet', label='Cold Wallet'),
        AccountList(url='/accounts/label/collectibles', label='Collectibles'),
        AccountList(url='/accounts/label/compound', label='Compound'),
        AccountList(url='/accounts/label/compromised', label='Compromised'),
        AccountList(url='/accounts/label/coss-io', label='COSS.io'),
        AccountList(url='/accounts/label/counter-market', label='Counter.Market'),
        AccountList(url='/accounts/label/crex24', label='CREX24'),
        AccountList(url='/accounts/label/crowdfunding', label='Crowdfunding'),
        AccountList(url='/accounts/label/cryptobots', label='CryptoBots'),
        AccountList(url='/accounts/label/cryptodozer', label='CryptoDozer'),
        AccountList(url='/accounts/label/cryptokitties', label='CryptoKitties'),
        AccountList(url='/accounts/label/cryptopia-hack', label='Cryptopia Hack'),
        AccountList(url='/accounts/label/cryptorome', label='CryptoRome'),
        AccountList(url='/accounts/label/cryptosaga', label='CryptoSaga'),
        AccountList(url='/accounts/label/cryptowars', label='CryptoWars'),
        AccountList(url='/accounts/label/decentraland', label='Decentraland'),
        AccountList(url='/accounts/label/defi', label='DeFi'),
        AccountList(url='/accounts/label/derivatives', label='Derivatives'),
        AccountList(url='/accounts/label/dex', label='Dex'),
        AccountList(url='/accounts/label/digifinex', label='DigiFinex'),
        AccountList(url='/accounts/label/donate', label='Donate'),
        AccountList(url='/accounts/label/dragonereum', label='Dragonereum'),
        AccountList(url='/accounts/label/dydx', label='dYdX'),
        AccountList(url='/accounts/label/education', label='Education'),
        AccountList(url='/accounts/label/electronics', label='Electronics'),
        AccountList(url='/accounts/label/ens', label='ENS'),
        AccountList(url='/accounts/label/etherdelta-hack', label='EtherDelta Hack'),
        AccountList(url='/accounts/label/etheremon', label='Etheremon'),
        AccountList(url='/accounts/label/ethereum-foundation', label='Ethereum Foundation'),
        AccountList(url='/accounts/label/etheroll', label='Etheroll'),
        AccountList(url='/accounts/label/ethfinex', label='Ethfinex'),
        AccountList(url='/accounts/label/evolution-land', label='Evolution Land'),
        AccountList(url='/accounts/label/exchange', label='Exchange'),
        AccountList(url='/accounts/label/f2pool', label='F2Pool'),
        AccountList(url='/accounts/label/fiat-gateway', label='Fiat Gateway'),
        AccountList(url='/accounts/label/finance', label='Finance'),
        AccountList(url='/accounts/label/flagged-by-sec', label='Flagged by SEC'),
        AccountList(url='/accounts/label/flowerpatch', label='Flowerpatch'),
        AccountList(url='/accounts/label/foam', label='FOAM'),
        AccountList(url='/accounts/label/fomo3d', label='Fomo3D'),
        AccountList(url='/accounts/label/gambling', label='Gambling'),
        AccountList(url='/accounts/label/gate-io', label='Gate.io'),
        AccountList(url='/accounts/label/gbx', label='GBX'),
        AccountList(url='/accounts/label/gemini', label='Gemini'),
        AccountList(url='/accounts/label/gods-unchained', label='Gods Unchained'),
        AccountList(url='/accounts/label/heist', label='Heist'),
        AccountList(url='/accounts/label/high-risk', label='High Risk'),
        AccountList(url='/accounts/label/hitbtc', label='HitBTC'),
        AccountList(url='/accounts/label/hot-wallet', label='Hot Wallet'),
        AccountList(url='/accounts/label/hotbit', label='Hotbit'),
        AccountList(url='/accounts/label/humanity', label='Humanity'),
        AccountList(url='/accounts/label/huobi', label='Huobi'),
        AccountList(url='/accounts/label/hydro-protocol', label='Hydro Protocol'),
        AccountList(url='/accounts/label/hyper-dragons', label='Hyper Dragons'),
        AccountList(url='/accounts/label/ico-wallets', label='ICO Wallets'),
        AccountList(url='/accounts/label/idex', label='IDEX'),
        AccountList(url='/accounts/label/imtoken', label='imToken'),
        AccountList(url='/accounts/label/kraken', label='Kraken'),
        AccountList(url='/accounts/label/kryptono', label='Kryptono'),
        AccountList(url='/accounts/label/kucoin', label='KuCoin'),
        AccountList(url='/accounts/label/latoken', label='LAToken'),
        AccountList(url='/accounts/label/liqui.io', label='Liqui.io'),
        AccountList(url='/accounts/label/liquid', label='Liquid'),
        AccountList(url='/accounts/label/loans', label='Loans'),
        AccountList(url='/accounts/label/lordless', label='LORDLESS'),
        AccountList(url='/accounts/label/maker', label='Maker'),
        AccountList(url='/accounts/label/marketplace', label='Marketplace'),
        AccountList(url='/accounts/label/matic-network', label='Matic Network'),
        AccountList(url='/accounts/label/media', label='Media'),
        AccountList(url='/accounts/label/megacryptopolis', label='MegaCryptoPolis'),
        AccountList(url='/accounts/label/melon', label='Melon'),
        AccountList(url='/accounts/label/mining', label='Mining'),
        AccountList(url='/accounts/label/miningpoolhub', label='MiningPoolHub'),
        AccountList(url='/accounts/label/music', label='Music'),
        AccountList(url='/accounts/label/my-crypto-heroes', label='My Crypto Heroes'),
        AccountList(url='/accounts/label/neon-district', label='Neon District'),
        AccountList(url='/accounts/label/nft', label='NFT'),
        AccountList(url='/accounts/label/okex', label='Okex'),
        AccountList(url='/accounts/label/old-contract', label='Old Contract'),
        AccountList(url='/accounts/label/opensea', label='OpenSea'),
        AccountList(url='/accounts/label/otc', label='OTC'),
        AccountList(url='/accounts/label/others', label='Others'),
        AccountList(url='/accounts/label/paribu', label='Paribu'),
        AccountList(url='/accounts/label/parity-bug', label='Parity Bug'),
        AccountList(url='/accounts/label/payment', label='Payment'),
        AccountList(url='/accounts/label/phish-hack', label='Phish / Hack'),
        AccountList(url='/accounts/label/poloniex', label='Poloniex'),
        AccountList(url='/accounts/label/prediction-market', label='Prediction Market'),
        AccountList(url='/accounts/label/pundi-x', label='Pundi X'),
        AccountList(url='/accounts/label/quadrigacx', label='QuadrigaCX'),
        AccountList(url='/accounts/label/raiden', label='Raiden'),
        AccountList(url='/accounts/label/remitano', label='Remitano'),
        AccountList(url='/accounts/label/research', label='Research'),
        AccountList(url='/accounts/label/sentinel-protocol', label='Sentinel Protocol'),
        AccountList(url='/accounts/label/shapeshift', label='ShapeShift'),
        AccountList(url='/accounts/label/spam-token', label='Spam Token'),
        AccountList(url='/accounts/label/suspicious', label='Suspicious'),
        AccountList(url='/accounts/label/synthetix', label='Synthetix'),
        AccountList(url='/accounts/label/tidex', label='Tidex'),
        AccountList(url='/accounts/label/token-contract', label='Token Contract'),
        AccountList(url='/accounts/label/token-sale', label='Token Sale'),
        AccountList(url='/accounts/label/topbtc', label='TopBTC'),
        AccountList(url='/accounts/label/trade-io', label='Trade.io'),
        AccountList(url='/accounts/label/trading', label='Trading'),
        AccountList(url='/accounts/label/trusttoken', label='TrustToken'),
        AccountList(url='/accounts/label/uniswap', label='Uniswap'),
        AccountList(url='/accounts/label/unsafe', label='Unsafe'),
        AccountList(url='/accounts/label/upbit', label='Upbit'),
        AccountList(url='/accounts/label/wallet-app', label='Wallet App'),
        AccountList(url='/accounts/label/white-hat-group', label='White Hat Group'),
        AccountList(url='/accounts/label/yunbi', label='YUNBI'),
        AccountList(url='/accounts/label/zb-com', label='ZB.com'),
        AccountList(url='/accounts/label/zethr', label='Zethr'),
    }


async def test_parser_extracts_accounts_from_list_page(
        parser: ParserService,
        requests_mock: Mocker,
        get_html: HtmlGetter,
) -> None:

    list_url = '/accounts/label/0x-ecosystem'
    list_ = AccountList(url=list_url, label='0x Ecosystem')
    lists = [list_]

    requests_mock.register_uri('GET', f'{settings.ES_BASE_URL}{list_url}/1', text=get_html('0x-ecosystem-list.html'))
    requests_mock.register_uri('GET', f'{settings.ES_BASE_URL}{list_url}/2', text=get_html('generic-account-list-empty.html'))  # NOQA: E501

    accounts = await parser.get_accounts(lists)
    zero_x_ecosystem_accounts = {
        NotableAccount(address=address, name=name, labels=('0x Ecosystem',))
        for address, name in (
            ('0x17992e4ffb22730138e4b62aaa6367fa9d3699a6', '0x: Asset Proxy Owner'),
            ('0xa3b2d1087bcebe59d188a23f75620612d967df72', '0x: Deployer 1'),
            ('0x2d7dc2ef7c6f6a2cbc3dba4db97b2ddb40e20713', '0x: Deployer 2'),
            ('0x2240dab907db71e64d3e0dba4800c83b5c502d4e', '0x: ERC20 Proxy'),
            ('0x208e41fb445f1bb1b6780d58356e81405f3e6127', '0x: ERC721 Proxy'),
            ('0x12459c951127e0c374ff9105dda097662a027093', '0x: Exchange 1'),
            ('0x4f833a24e1f95d70f028921e27040ca56e09ab0b', '0x: Exchange 2'),
            ('0x206376e8940e42538781cd94ef024df3c1e0fd43', '0x: Ext Dev Pool'),
            ('0x7afc2d5107af94c462a194d2c21b5bdd238709d6', '0x: Forwarder'),
            ('0x5468a1dc173652ee28d249c271fa9933144746b1', '0x: Forwarder 2'),
            ('0x606af0bd4501855914b50e2672c5926b896737ef', '0x: MultiSig 1'),
            ('0x01d9f4d104668cdc0b6d13c45dff5e15d58d8f28', '0x: MultiSig 2'),
            ('0x9463e518dea6810309563c81d5266c1b1d149138', '0x: Order Validator'),
            ('0xdb63d40c033d35e79cdbb21430f0fe10e9d97303', '0x: Team Vesting'),
            ('0x926a74c5c36adf004c87399e65f75628b0f98d2c', '0x: Token Registry'),
            ('0xd4fd252d7d2c9479a8d616f510eac6243b5dddf9', '0x: Token Sale'),
            ('0x8da0d80f5007ef1e431dd2127178d224e32c2ef4', '0x: Token Transfer Proxy'),
            ('0x0e8ba001a821f3ce0734763d008c9d7c957f5852', 'AmadeusRelay'),
            ('0x5dd835a893734b8d556eccf87800b76dda5aedc5', 'Bamboo Relay'),
            ('0xe269e891a2ec8585a378882ffa531141205e92e9', 'DDEX'),
            ('0x58a5959a6c528c5d5e03f7b9e5102350e24005f1', 'ERC dEX'),
            ('0x2cc42d1cd65af27cc999e41ef93d1a763dc821f8', 'IDT Exchange'),
            ('0x4524baa98f9a3b9dec57caae7633936ef96bd708', 'LedgerDex'),
            ('0xc22d5b2951db72b44cfb8089bb8cd374a3c354ea', 'OpenRelay'),
            ('0xd2045edc40199019e221d71c0913343f7908d0d5', 'Paradex'),
        )
    }

    assert set(accounts) == zero_x_ecosystem_accounts


async def test_parser_extracts_empty_set_from_empty_page(
        parser: ParserService,
        requests_mock: Mocker,
        get_html: HtmlGetter,
) -> None:

    list_url = '/accounts/label/prediction-market'
    list_ = AccountList(url=list_url, label='Prediction Market')
    lists = [list_]

    requests_mock.register_uri('GET', f'{settings.ES_BASE_URL}{list_url}/1', text=get_html('generic-account-list-empty.html'))  # NOQA: E501

    accounts = await parser.get_accounts(lists)

    assert accounts == list()


async def test_parser_parses_all_pages(
        parser: ParserService,
        requests_mock: Mocker,
        get_html: HtmlGetter,
) -> None:

    list_url = '/accounts/label/dragonereum'
    list_ = AccountList(url=list_url, label='Dragonereum')
    lists = [list_]

    requests_mock.register_uri('GET', f'{settings.ES_BASE_URL}{list_url}/1', text=get_html('dragonereum-page-1.html'))
    requests_mock.register_uri('GET', f'{settings.ES_BASE_URL}{list_url}/2', text=get_html('dragonereum-page-2.html'))
    requests_mock.register_uri('GET', f'{settings.ES_BASE_URL}{list_url}/3', text=get_html('generic-account-list-empty.html'))  # NOQA: E501

    accounts = await parser.get_accounts(lists)
    dragonereum_accounts = {
        NotableAccount(address=address, name=name, labels=('Dragonereum',))
        for address, name in (
            ('0x54c5231c982c6ce0c44f7b0c4a18275db998a02e', 'Dragonereum: Battle'),
            ('0x94e34f68d66b5dd954b56a513cf7c48f08036f19', 'Dragonereum: Battle Controller'),
            ('0xd5bae616505430595ee28b9e0e092dc298ab1b19', 'Dragonereum: Breeding Marketplace'),
            ('0xf5c6acb57f13de23b2140b0b399cd7eeae800ff8', 'Dragonereum: Core'),
            ('0x69980dfd271daf09b606b7fa1d872d98c98015a8', 'Dragonereum: Core Controller'),
            ('0xb5b67b0bd9f0f188e900d6a50cd1d66a6d9932f7', 'Dragonereum: Distribution'),
            ('0x960f401aed58668ef476ef02b2a2d43b83c261d8', 'Dragonereum: Dragon'),
            ('0x6e9f056176b7997a98b9919bfb6642d4ea92a1ba', 'Dragonereum: Dragon Core'),
            ('0xdcd74ce660f8335f3840421b06d83a122d0570ff', 'Dragonereum: Dragon Core Helper'),
            ('0x0163f2aecc6263dfb2b9b01e9e76f93d4cc9862e', 'Dragonereum: Dragon Genetics'),
            ('0x59d2a1370e57427b0ad6342dcf45dec9adfb772d', 'Dragonereum: Dragon Getter'),
            ('0x556b52af1930bdfdde016851ce078b352ef643e5', 'Dragonereum: Dragon Leaderboard'),
            ('0x5cad8e26bf869c06467955045e97c829653a415c', 'Dragonereum: Dragon Marketplace'),
            ('0xe52b6ea97e40ae1619469dcc1e7711afb960762e', 'Dragonereum: Dragon Params'),
            ('0xfcad2859f3e602d4cfb9aca35465a618f9009f7b', 'Dragonereum: Egg'),
            ('0x2b0f6794c28efb6f73ae1c9732c51cd67a8296a1', 'Dragonereum: Egg Core'),
            ('0xbba8fbaa8e14061948dc370821fa311baa74172a', 'Dragonereum: Egg Marketplace'),
            ('0xd31b8e0219bd83678978f6db531d9a3f45608894', 'Dragonereum: Events'),
            ('0xf88fdb63dc782dae646cd6c74728ca83f56200e4', 'Dragonereum: Getter'),
            ('0x150b0b96933b75ce27af8b92441f8fb683bf9739', 'Dragonereum: Gold'),
            ('0xd2584e838896792d9abea79c06ee9d6ab7f100db', 'Dragonereum: Gold Marketplace'),
            ('0x577d6886fad02e5fb15b55645894b1ae14228ce4', 'Dragonereum: Gold Marketplace Storage'),
            ('0xad3cdf38ccace151cdf5f03fa64c1518a75cf7af', 'Dragonereum: Main Base'),
            ('0x68ed06af5989e05bc4aa510b44dc6d003e225187', 'Dragonereum: Main Battle'),
            ('0x0601ec5350b48fe2c3f421ea42915d16df108d27', 'Dragonereum: Main Market'),
            ('0x6d81d1fda601df52f83188dce617b65ac9b3c5be', 'Dragonereum: Marketplace Controller'),
            ('0xc643a0242d73c3f4368e0e84b0124bfb4629b3ff', 'Dragonereum: Nest'),
            ('0x00e04c3fbb3783fd57eae4037ee1ee02c4d84614', 'Dragonereum: Random'),
            ('0xc2b1fee7962a1338f2dedf4e4ff750f890d03111', 'Dragonereum: Skill Marketplace'),
            ('0xb3d5d71ff892f3b577e42d5271cc0ef924313d18', 'Dragonereum: Treasury'),
            ('0xf44026f15a44140175aca39c67603c74502a0bdd', 'Dragonereum: Upgrade Controller'),
            ('0x2b053438ec2ac37dbf912bcde32edfc956350fc5', 'Dragonereum: User'),
        )
    }

    assert set(accounts) == dragonereum_accounts


@pytest.mark.usefixtures('mock_sleepers')
async def test_parser_does_not_crashes_if_one_page_cannot_be_parsed(
        parser: ParserService,
        requests_mock: Mocker,
) -> None:

    list_ = AccountList(url='/accounts/label/liqui.io', label='Liqui.io')
    lists = [list_]

    # Real scenario of an invalid Liqui.io label page.
    requests_mock.register_uri('GET', f'{settings.ES_BASE_URL}/accounts/label/liqui.io/1', status_code=302, headers={'location': '../404'})  # NOQA: E501
    requests_mock.register_uri('GET', f'{settings.ES_BASE_URL}/accounts/404', status_code=302, headers={'location': '/accounts'})  # NOQA: E501
    requests_mock.register_uri('GET', f'{settings.ES_BASE_URL}/accounts')

    accounts = await parser.get_accounts(lists)

    assert accounts == list()


async def test_parser_does_not_crashes_if_one_page_html_is_invalid(
        parser: ParserService,
        requests_mock: Mocker,
        get_html: HtmlGetter,
) -> None:

    list_url = '/accounts/label/invalid'
    list_ = AccountList(url=list_url, label='Invalid')
    lists = [list_]

    requests_mock.register_uri('GET', f'{settings.ES_BASE_URL}{list_url}/1', text=get_html('accounts-invalid-list.html'))  # NOQA: E501

    accounts = await parser.get_accounts(lists)

    assert accounts == list()


async def test_parser_dedupes_accounts_and_aggregates_accounts_labels(
        parser: ParserService,
        requests_mock: Mocker,
        get_html: HtmlGetter,
) -> None:

    lists = [
        AccountList(url='/accounts/label/bitfinex', label='Bitfinex'),
        AccountList(url='/accounts/label/exchange', label='Exchange'),
    ]

    requests_mock.register_uri('GET', f'{settings.ES_BASE_URL}/accounts/label/bitfinex/1', text=get_html('bitfinex-list.html'))  # NOQA: E501
    requests_mock.register_uri('GET', f'{settings.ES_BASE_URL}/accounts/label/bitfinex/2', text=get_html('generic-account-list-empty.html'))  # NOQA: E501
    requests_mock.register_uri('GET', f'{settings.ES_BASE_URL}/accounts/label/exchange/1', text=get_html('exchange-list.html'))  # NOQA: E501
    requests_mock.register_uri('GET', f'{settings.ES_BASE_URL}/accounts/label/exchange/2', text=get_html('generic-account-list-empty.html'))  # NOQA: E501

    accounts = await parser.get_accounts(lists)

    assert set(accounts) == {
        # Appears in both lists.
        NotableAccount(address='0x1151314c646ce4e0efd76d1af4760ae66a9fe30f', name='Bitfinex 1', labels=('Bitfinex', 'Exchange')),  # NOQA: E501
        NotableAccount(address='0x7727e5113d1d161373623e5f49fd568b4f543a9e', name='Bitfinex 2', labels=('Bitfinex', 'Exchange')),  # NOQA: E501
        NotableAccount(address='0x4fdd5eb2fb260149a3903859043e962ab89d8ed4', name='Bitfinex 3', labels=('Bitfinex', 'Exchange')),  # NOQA: E501
        NotableAccount(address='0x876eabf441b2ee5b5b0554fd502a8e0600950cfa', name='Bitfinex 4', labels=('Bitfinex', 'Exchange')),  # NOQA: E501
        NotableAccount(address='0x742d35cc6634c0532925a3b844bc454e4438f44e', name='Bitfinex 5', labels=('Bitfinex', 'Exchange')),  # NOQA: E501

        # Appears only in Bitfinex.
        NotableAccount(address='0x2af5d2ad76741191d15dfe7bf6ac92d4bd912ca3', name='Bitfinex: LEO Token', labels=('Bitfinex',)),  # NOQA: E501
        NotableAccount(address='0xcafb10ee663f465f9d10588ac44ed20ed608c11e', name='Bitfinex: Old Address 1', labels=('Bitfinex',)),  # NOQA: E501
        NotableAccount(address='0x7180eb39a6264938fdb3effd7341c4727c382153', name='Bitfinex: Old Address 2', labels=('Bitfinex',)),  # NOQA: E501

        # Appears only in Exchange.
        NotableAccount(address='0x05f51aab068caa6ab7eeb672f88c180f67f17ec7', name='ABCC', labels=('Exchange',)),
        NotableAccount(address='0x7a10ec7d68a048bdae36a70e93532d31423170fa', name='Bgogo 1', labels=('Exchange',)),
        NotableAccount(address='0xce1bf8e51f8b39e51c6184e059786d1c0eaf360f', name='Bgogo 2', labels=('Exchange',)),
        NotableAccount(address='0xf73c3c65bde10bf26c2e1763104e609a41702efe', name='Bibox', labels=('Exchange',)),
        NotableAccount(address='0xa30d8157911ef23c46c0eb71889efe6a648a41f7', name='BigONE', labels=('Exchange',)),
        NotableAccount(address='0xf7793d27a1b76cdf14db7c83e82c772cf7c92910', name='Bilaxy', labels=('Exchange',)),
        NotableAccount(address='0x3f5ce5fbfe3e9af3971dd833d26ba9b5c936f0be', name='Binance 1', labels=('Exchange',)),
        NotableAccount(address='0xd551234ae421e3bcba99a0da6d736074f22192ff', name='Binance 2', labels=('Exchange',)),
        NotableAccount(address='0x564286362092d8e7936f0549571a803b203aaced', name='Binance 3', labels=('Exchange',)),
        NotableAccount(address='0x0681d8db095565fe8a346fa0277bffde9c0edbbf', name='Binance 4', labels=('Exchange',)),
        NotableAccount(address='0xfe9e8709d3215310075d67e3ed32a380ccf451c8', name='Binance 5', labels=('Exchange',)),
        NotableAccount(address='0x4e9ce36e442e55ecd9025b9a6e0d88485d628a67', name='Binance 6', labels=('Exchange',)),
        NotableAccount(address='0x7c49e1c0e33f3efb57d64b7690fa287c8d15b90a', name='Bit2C', labels=('Exchange',)),
        NotableAccount(address='0xdf5021a4c1401f1125cd347e394d977630e17cf7', name='Bitbox', labels=('Exchange',)),
        NotableAccount(address='0x8fa8af91c675452200e49b4683a33ca2e1a34e42', name='Bithumb 1', labels=('Exchange',)),
        NotableAccount(address='0x3052cd6bf951449a984fe4b5a38b46aef9455c8e', name='Bithumb 2', labels=('Exchange',)),
        NotableAccount(address='0x3fbe1f8fc5ddb27d428aa60f661eaaab0d2000ce', name='Bithumb Contract', labels=('Exchange',)),  # NOQA: E501
        NotableAccount(address='0xe79eef9b9388a4ff70ed7ec5bccd5b928ebb8bd1', name='BitMart', labels=('Exchange',)),
        NotableAccount(address='0x03bdf69b1322d623836afbd27679a1c0afa067e9', name='Bitmax 1', labels=('Exchange',)),
        NotableAccount(address='0x4b1a99467a284cc690e3237bc69105956816f762', name='Bitmax 2', labels=('Exchange',)),
    }


async def test_parser_lowers_checksum_accounts_addresses(
        parser: ParserService,
        requests_mock: Mocker,
        get_html: HtmlGetter,
) -> None:

    lists = [
        AccountList(url='/accounts/label/checksummed', label='Checksummed'),
    ]

    requests_mock.register_uri('GET', f'{settings.ES_BASE_URL}/accounts/label/checksummed/1', text=get_html('checksummed-list.html'))  # NOQA: E501
    requests_mock.register_uri('GET', f'{settings.ES_BASE_URL}/accounts/label/checksummed/2', text=get_html('generic-account-list-empty.html'))  # NOQA: E501

    accounts = await parser.get_accounts(lists)

    assert set(accounts) == {
        NotableAccount(address='0xf5673c0ad28ca6a0064670ce1fe2a73ce847c74f', name='Pieta Token', labels=('Checksummed',)),  # NOQA: E501
    }


async def test_parser_inserts_a_single_item_to_database(
        sa_engine: Engine,
        parser: ParserService,
) -> None:
    await parser.write_accounts(
        [
            NotableAccount(
                address='0x4b1a99467a284cc690e3237bc69105956816f762',
                name='Bitmax 2',
                labels=('Exchange',)
            ),
        ],
    )

    async with sa_engine.acquire() as conn:
        in_db = await conn.execute(notable_accounts_t.select())
        in_db = [dict(item) for item in in_db]

    assert in_db == [
        {
            'address': '0x4b1a99467a284cc690e3237bc69105956816f762',
            'name': 'Bitmax 2',
            'labels': ['Exchange'],
            'is_admin_reviewed': False,
        },
    ]


async def test_parser_does_not_override_an_item_if_requested(
        parser: ParserService,
        sa_engine: Engine,
) -> None:
    async with sa_engine.acquire() as conn:
        await conn.execute(notable_accounts_t.insert().values(
            {
                'address': '0x8da0d80f5007ef1e431dd2127178d224e32c2ef4',
                'name': '0x: Token Transfer Proxy',
                'labels': ['0x Ecosystem'],
                'is_admin_reviewed': True,
            },
        ))

    await parser.write_accounts(
        [
            NotableAccount(
                address='0x8da0d80f5007ef1e431dd2127178d224e32c2ef4',
                name='NEW NAME FOR A TOKEN',
                labels=('0x Ecosystem', 'ANOTHER LABEL'),
            ),
        ],
    )

    async with sa_engine.acquire() as conn:
        in_db = await conn.execute(notable_accounts_t.select())
        in_db = [dict(item) for item in in_db]

    assert in_db == [
        {
            'address': '0x8da0d80f5007ef1e431dd2127178d224e32c2ef4',
            'name': '0x: Token Transfer Proxy',
            'labels': ['0x Ecosystem'],
            'is_admin_reviewed': True,
        },
    ]


async def test_parser_overrides_an_item_if_requested(
        parser_with_override: ParserService,
        sa_engine: Engine,
) -> None:
    async with sa_engine.acquire() as conn:
        await conn.execute(notable_accounts_t.insert().values(
            {
                'address': '0x4b1a99467a284cc690e3237bc69105956816f762',
                'name': 'Bitmax 2',
                'labels': ['Exchange'],
                'is_admin_reviewed': True,
            },
        ))

    await parser_with_override.write_accounts(
        [
            NotableAccount(
                address='0x4b1a99467a284cc690e3237bc69105956816f762',
                name='NEW NAME FOR A TOKEN',
                labels=('0x Ecosystem', 'ANOTHER LABEL'),
            ),
        ],
    )

    async with sa_engine.acquire() as conn:
        in_db = await conn.execute(notable_accounts_t.select())
        in_db = [dict(item) for item in in_db]

    assert in_db == [
        {
            'address': '0x4b1a99467a284cc690e3237bc69105956816f762',
            'name': 'NEW NAME FOR A TOKEN',
            'labels': ['0x Ecosystem', 'ANOTHER LABEL'],
            'is_admin_reviewed': False,
        },
    ]
