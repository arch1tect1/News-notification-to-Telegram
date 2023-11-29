import requests
import asyncio
from bs4 import BeautifulSoup
from telegram import Bot
from telegram.error import BadRequest


TELEGRAM_BOT_TOKEN = ''
TELEGRAM_CHAT_ID = ''
TARGET_URL = ''
KEYWORDS = ["Encryption", "Firewall", "Malware", "Phishing", "Authentication",
			"Intrusion detection", "VPN", "Cyberattack", "Zero-day exploit","Biometrics"
			"Patch", "Cybersecurity policy", "Endpoint security", "Two-factor authentication",
			"Cyber hygiene", "Vulnerability", "Penetration testing", "Incident response"
			"Ransomware", "Security awareness"
			]

# A file to store processed news links
LINKS_FILE = 'processed_links.txt'

# A set to store processed news links to get the latest news
processed_links = set()


async def send_telegram_message(message, link):
	bot = Bot(token=TELEGRAM_BOT_TOKEN)

	try:
		message_with_link = f"{message}\n\nRead more: {link}"
		await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message_with_link)
		print(f"Telegram message sent: {message_with_link}")
	except BadRequest as e:
		print(f"Error sending message: {e}")


def get_html(url):
	response = requests.get(url)
	print(f"HTTP request made to {url}")
	return response.text


async def parse_and_notify(html, base_url):
	soup = BeautifulSoup(html, 'html.parser')

	news_blocks = soup.find_all('div', class_='single-blog-posts h-100')

	for news_block in news_blocks:
		news_text = news_block.get_text(strip=True)
		news_link = base_url

		if news_text and any(keyword in news_text.lower() for keyword in KEYWORDS):
			add_space = '\n'.join(news_text.split('\n')[:3])

			# Add a space after the 2023 date
			add_space = add_space.replace('2023', '2023\n\n')

			# Check if the news link is not in the set of processed links
			if news_link not in processed_links:
				await send_telegram_message(add_space, news_link)
				processed_links.add(news_link)

			# Save the processed link to the file
			with open(LINKS_FILE, 'a') as f:
				f.write(news_link + '\n')
	else:
		print("News text is empty or does not contain relevant keywords.")


async def main():
	base_url = ''

	# Load previously processed links from the file
	try:
		with open(LINKS_FILE, 'r') as f:
		processed_links.update(line.strip() for line in f)
	except FileNotFoundError:
		pass # Ignore if the file doesn't exist

	html_content = get_html(TARGET_URL)
	await parse_and_notify(html_content, base_url)

	print("Script execution completed.")


# Event loop
if name == "main":
	asyncio.run(main())