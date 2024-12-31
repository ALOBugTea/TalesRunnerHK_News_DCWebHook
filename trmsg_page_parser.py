import requests
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook, DiscordEmbed

# Set up the webhook
# btw, base_Url cannot be changed, becuase it's can be only used at 'https://www.talesrunner.com.hk'
base_Url = 'https://www.talesrunner.com.hk'
webhook_links = ['']

#create requirements.txt
#pipreqs --force --encoding UTF-8

# For this python file
def remove_new_line_symbol(lines):
	removedLines = []
	for line in lines:
		removedLines.append(line.rstrip('\r\n\t').rstrip())
	_str = ''
	for rl in removedLines:
		_str += rl
	return _str

# For trmsg_titles.txt
def remove_new_line_symbol2(lines):
	removedLines = []
	for line in lines:
		removedLines.append(line.rstrip('\r\n\t'))
	_str = ''
	for rl in removedLines:
		_str += rl
	return _str

# Check the news page on talesrunner.com.hk
def getNews_html():
	r = requests.get('https://www.talesrunner.com.hk/notice/notice.php?type=system')
	csoup = BeautifulSoup(r.text, 'html.parser')
	return csoup

# Check the patch page on talesrunner.com.hk
def getpatchNews_html():
	r = requests.get('https://www.talesrunner.com.hk/notice/notice.php?type=patch')
	csoup = BeautifulSoup(r.text, 'html.parser')
	return csoup

# Process the content element, formatting it as needed
# Such as patch page have youtube links, banned players or prizes who get...
# 
def custom_format(element):
	# Initialize a variable to store the formatted content
	formatted_content = ""

	# Define a recursive function to process each element
	def process_element(el):
		nonlocal formatted_content
		if el.name == "p":
			# Check if the paragraph contains a table
			if el.find("table"):
				# Process the table within the paragraph
				for table in el.find_all("table"):
					formatted_content += process_table(table)
			else:
				# Process paragraph content
				formatted_content += el.get_text(strip=True) + "\n"
		# Img always put as picture first (what a funtown style)
		# elif el.name == "img":
		#     # Process image content
		#     img_src = el.get("src", "")
		#     formatted_content += f"Image: {img_src}\n"
		elif el.name == "iframe":
			# Check if the iframe is a YouTube embed
			iframe_src = el.get("src", "")
			if "youtube.com" in iframe_src or "youtu.be" in iframe_src:
				# Extract the video ID from the YouTube embed URL
				video_id = iframe_src.split('/')[-1].split('?')[0]
				# Construct a standard YouTube URL
				youtube_url = f"https://www.youtube.com/watch?v={video_id}"
				formatted_content += f"YouTube Video: {youtube_url}\n"
		# Almost useless, because table always in "p" tag ...
		elif el.name == "table":
			# Process table content
			formatted_content += process_table(el)
		elif el.name is not None:
			# If the element has children, process them recursively
			for child in el.children:
				process_element(child)
		else:
			# Process other content (text nodes)
			if el.string:
				formatted_content += el.string.strip() + "\n"

	# Helper function to process tables
	def process_table(table):
		table_content = ""
		rows = table.find_all("tr")
		for row in rows:
			cells = row.find_all("td")
			row_data = []
			for cell in cells:
				# Recursively process each cell to handle nested elements
				cell_content = custom_format(cell)
				row_data.append(cell_content.strip())
			table_content += " | ".join(row_data) + "\n"
		return table_content

	# Start processing from the root element
	process_element(element)

	# Return the formatted content for discord webhook
	return formatted_content

# Main processing, read trmsg_titles.txt;
# parse news, check new titles, and send webhooks
def get_trmsg_news():
	
	# File Input
	f = open('trmsg_titles.txt','r+', encoding="utf-8")
	readTitles = f.readlines()
	writeTitles = readTitles

	# Crawler
	r = requests.get("https://www.talesrunner.com.hk/news/MMXIII_news.html")
	r.encoding = 'big5'#抓官網的meta標籤看編碼
	soup = BeautifulSoup(r.text, 'html.parser')

	# Crawler get News and patchNews
	newsSoup = getNews_html()
	patchSoup = getpatchNews_html()

	boardData = soup.find(id="allNoticeContainer")
	boardItems = boardData.find_all("tr")
	isUpdated = False
	for div in reversed(boardItems):
		#link type
		dtObjects = div.find_all('td')
		if len(dtObjects) < 3:
			continue
		if dtObjects[1].find("span") == None:
			continue
		event_link = dtObjects[0].img['src']
		event_type = '最新消息'
		if "item_02" in event_link:
			event_type = '更新情報'
		if "item_03" in event_link:
			event_type = '活動消息'
		title = dtObjects[1].a
		board_title = str(dtObjects[1].span.get_text())
		# if "停權" in board_title:
		#     continue
		board_date = dtObjects[2].get_text()
		board_read = False
		if event_type == '最新消息':
			tsoup = newsSoup
			board_read = True
		elif event_type == '更新情報':
			tsoup = patchSoup
			board_read = True
		board_content = ""
		board_date = remove_new_line_symbol(board_date).replace("-", "/")
		afterboardTitle = remove_new_line_symbol(board_title)
		save_board_title = f'{board_date} {afterboardTitle}'
		# print(f'{board_date} {afterboardTitle}')
		# print("----------------------------------------")
		if (board_read):
			csoup = tsoup
			searchOtherContent = False
			Content = ""
			findPointer = csoup.find_all('td', 'pointer')
			for line in findPointer:
				titleCheck = line.find_previous('tr')
				for titleC in titleCheck:
					afterTitleC = remove_new_line_symbol(titleC.text)
					date_td = line.find_next('td').find('td', class_='date')
					if date_td:
						date_td_text = remove_new_line_symbol(date_td.text)
						if date_td_text == board_date:
							# print(f'{date_td_text} | {afterTitleC}')
							if afterboardTitle in afterTitleC:
								searchOtherContent = True
								break
				if searchOtherContent:
					tempContent = line.find_parent('tr').find_parent('tr').find_next_siblings('tr')
					lineCount = 0
					for addC in tempContent:
						if lineCount > 3:
							break
						lineCount += 1
						Content += custom_format(addC)
					break
			board_content = Content

		# tag color
		tag_color = 5028631
		if event_type == '活動消息':
			tag_color = 561039
		elif event_type == '更新情報':
			tag_color = 16734003

		current_title = board_title
		find_news = False
		for line in readTitles:
			temp_title = save_board_title
			temp_line = remove_new_line_symbol2(line)
			if temp_title in temp_line:
				if len(temp_title) == len(temp_line):
					find_news = True
					break
		if find_news == False:
			temp_title = remove_new_line_symbol2(current_title)
			writeTitles.insert(0, save_board_title + '\n')#temp_title + '\n')
			current_link = title['href']

			content = title['onmouseover']
			content = content.replace('changeBanner("', '')
			content = content.replace('");', '')

			embed = DiscordEmbed()
			embed.set_author(name='跑online官網公告轉送', url=current_link,
							icon_url='https://www.talesrunner.com.hk/images/MMXIII/index/tr_logo.png')
			embed.title = event_type + '：' + save_board_title #current_title
			embed.description = board_content[:600]
			embed.set_thumbnail(url='https://www.talesrunner.com.hk/news' + '/' + event_link)
			embed.set_image(url=content)
			embed.add_embed_field(name='官網連結', value=current_link)
			embed.color = tag_color
			
			for link in webhook_links:
				new_embed = embed
				webhook = DiscordWebhook(url=link)
				webhook.add_embed(new_embed)
				webhook.execute()
				#print("已發布：" + current_title)
			# print(embed.title)
			# print(embed.description)
			print("已更新：" + save_board_title)
			isUpdated = True
		else:
			print("未更新：" + save_board_title)
		
		#count -= 1
	
	while len(writeTitles) > 20:
		writeTitles.pop()

	if isUpdated:
		print("已儲存檔案")
		f.seek(0)
		f.truncate(0)
		f.writelines(writeTitles)
	f.close()


if __name__ == '__main__':
	get_trmsg_news()
