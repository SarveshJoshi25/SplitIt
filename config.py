import dotenv
import os

dotenv.load_dotenv()

DatabaseString = os.getenv("DATABASE_STRING")
DatabaseString2 = os.getenv("DATABASE_STRING2")
DatabasePassword = os.getenv("DATABASE_PASSWORD")
AccessSecretKey = os.getenv('ACCESS_KEY')
RefreshSecretKey = os.getenv('REFRESH_KEY')
DjangoSecretKey = os.getenv('DJANGO_SECRET_KEY')
EmailAddress = os.getenv('EMAIL_ADDRESS')
EmailPassword = os.getenv('EMAIL_PASSWORD')