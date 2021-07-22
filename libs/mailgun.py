from requests import post
import os


class MailGunException(Exception):
	def __init__(self, message):
		super.__init__(message)


class Mailgun:
	MAILGUN_DOMAIN = os.environ.get("MAILGIN_DOMAIN")
	MAILGUN_API_KEY = os.environ.get("MAILGUN_API_KEY")
	FROM_TITLE = "Store Bom Bom"
	FROM_EMAIL = "postmaster@sandbox5b58ae5401714a5fae1b1dc10bd4274c.mailgun.org"

	@classmethod
	def send_email(cls, email, subject, text, html):
		if cls.MAILGUN_API_KEY is None:
			raise MailGunException("Failed to load Mailgun api key")

		if cls.MAILGUN_DOMAIN is None:
			raise MailGunException("Failed to load Mailgun domain")

		response = post(
	        f"http://api.mailgun.net/v3/{cls.MAILGUN_DOMAIN}/messages",
	        auth = ("api", cls.MAILGUN_API_KEY),
	        data = {"from": f"{cls.FROM_TITLE} <{cls.FROM_EMAIL}",
	                "to": email,
	                "subject": subject,
	                "text": text
	                "html": html,
	        },
	    )

	   	if response.status_code != 200:
	   		raise MailGunException("Error in sending confirmation mail")

	   	return response