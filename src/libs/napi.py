import config
import numerapi

napi = numerapi.NumerAPI(
    public_id=config.NUMERAI_PUBLIC, secret_key=config.NUMERAI_SECRET, verbosity="info"
)
