 Flask implementation of the ff6worldscollide.com balance-and-ruin API (ref: https://github.com/kielbasiago/ultima/tree/main/apps/balance-and-ruin/api)

 Tested with python 3.9.6

 Running requires several environment variables in a .env file. This includes these values:
    PSQL_KEYS_TABLE='api_keys'
    PSQL_SEEDS_TABLE='seeds'
    PSQL_LOGS_TABLE='spoiler_logs'
    POSTGRES_URL='<your postgreSQL URL here>'
    AWS_SECRET_ACCESS_KEY='<your S3 bucket access secret here>'
    AWS_ACCESS_KEY_ID='<your S3 bucket access key id here>'
    PATCH_BUCKET='<your S3 bucket used to store patches>'
    NEXT_PUBLIC_RECAPTHA_KEY='<recaptcha key>'
    RECAPTCHA_SECRET='<recaptcha secret>'
    MONGODB_URI='<mongodb URL, including username & password>'
    PUBLIC_URL='<where you're hosting the ff6worldscollide frontend, for example https://dev.ff6worldscollide.com>'

 To run locally:
    pip install -r requirements.txt
    flask run



 
