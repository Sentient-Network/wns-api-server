__author__ = 'mdavid'

from netki.api.util import create_json_response
from netki.util.logutil import LogUtil
from netki.util.validation import InputValidation

from wnsresolver import *

# Get Config
from netki.common.config import ConfigManager
config = ConfigManager().get_config()

log = LogUtil.setup_logging('domain_api')

def api_wallet_lookup(wallet_name, currency):

    log.info('Calling wallet_lookup(%s, %s)' % (wallet_name, currency))

    addr = error = None

    if not InputValidation.is_valid_field(wallet_name) or not InputValidation.is_valid_field(currency) or '.' not in wallet_name:

        log.warn('wallet_lookup fields invalid, returning failure')
        return create_json_response(success=False, message='Invalid Parameters')

    # Handle transforms to lowercase and doge to dgc
    currency = 'dgc' if currency.lower() == 'doge' else currency.lower()
    wallet_name = wallet_name.lower()

    try:

        # If you do not have access to Namecoin node, allow for .bit lookups via API
        if wallet_name.endswith('.bit') and config.namecoin.enabled and config.namecoin.use_api:
            response = requests.get('%s/%s/%s' % (config.general.lookup_api_url, wallet_name, currency))
            if response.json().get('success'):
                addr = response.json().get('wallet_address')
            else:
                raise WalletNameLookupError

        else:
            wnsresolver = WalletNameResolver(resolv_conf=config.general.resolv_conf_path, dnssec_root_key=config.general.dnssec_root_key_path)

            if config.namecoin.enabled:
                wnsresolver.set_namecoin_options(
                    host=config.namecoin.host,
                    user=config.namecoin.user,
                    password=config.namecoin.password,
                    port=config.namecoin.port,
                    tmpdir=config.namecoin.resolver_temp_path
                )

            addr = wnsresolver.resolve_wallet_name(wallet_name, currency)

    except (WalletNameLookupError, WalletNameUnavailableError):
        error = 'Wallet Name does not exist'

    except WalletNameCurrencyUnavailableError:
        error = 'Wallet Name Does Not Contain Requested Currency'

    except WalletNameLookupInsecureError:
        error = 'Wallet Name Lookup is Insecure'

    except WalletNameNamecoinUnavailable:
        error = 'Namecoin Wallet Name cannot be resolved at this time'

    except Exception as e:
        log.error('wallet_lookup(%s, %s) failed: %s' % (wallet_name, currency, str(e)))
        return create_json_response(success=False, message='General Wallet Lookup Failure')

    success_flag=True
    msg = ''
    rdata = {}
    if addr:
        rdata['wallet_name'] = wallet_name
        rdata['currency'] = currency
        rdata['wallet_address'] = addr
        log.debug('Wallet Lookup for (%s, %s) returned successfully with address: %s' % (wallet_name, currency, addr))

    elif error:
        success_flag=False
        msg = str(error)
        log.debug('Wallet Lookup for (%s, %s) returned an error: %s' % (wallet_name, currency, msg))

    return create_json_response(success=success_flag, message=msg, data=rdata)
