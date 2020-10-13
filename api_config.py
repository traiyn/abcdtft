class ApiConfig(object):
    """
    Be a good developer and put some wel-formatted info here, please, Taylor.
    """

    def __init__(self, api_key, rate_limit):
        self.api_key = api_key
        self.rate_limit_permin = rate_limit['per_second']
        self.rate_limit_persec = rate_limit['per_minute']