import json
import plyvel

from dateutil import parser
from PIL import Image, ImageDraw, ImageFont

LOG = []     # The log as a list of dictionaries
AUTHORS = [] # The list if author names
DATES = []   # The first days the authors commit
FONT = ImageFont.truetype('/usr/share/fonts/truetype/ubuntu-font-family/Ubuntu-M.ttf', 12)
LONGEST_NAME = 0
LONGEST_DATE = 0
NUM_WEEKS = 0
FIRST_DATE = None
LAST_DATE = None

def find_week(date):
    return int((date - FIRST_DATE).days / 7)

if __name__ == '__main__':
    commitdb = plyvel.DB('../data/commits/', create_if_missing=True)
    orgs = commitdb.prefixed_db(b'zalando')
    project = orgs.prefixed_db(b'nakadi')

    # Data preparation
    for date, commit_data in project:
        commit = json.loads(commit_data)

        # Convert the date to a datetime obj
        dt = parser.parse(date)
        if not FIRST_DATE: FIRST_DATE = dt
        LAST_DATE = dt

        # Check if we know the name
        # Check if this is the longest name
        if not commit['commit']['author']['name'] in AUTHORS:
            AUTHORS.append(commit['commit']['author']['name'])
            DATES.append(parser.parse(commit['commit']['author']['date']))
            name_length = FONT.getsize(commit['commit']['author']['name'])[0]
            if name_length > LONGEST_NAME: 
                LONGEST_NAME = name_length
            date_length = FONT.getsize(str(dt))[0]
            if date_length > LONGEST_DATE:
                LONGEST_DATE = date_length

    NUM_WEEKS = find_week(LAST_DATE)

    # Now draw this
    padding = FONT.getsize("X")[1]
    img_height = (2 * padding) + (padding * len(AUTHORS))
    img_width = (6 * padding) + (padding * NUM_WEEKS) + (2 * LONGEST_NAME) + LONGEST_DATE
    im = Image.new("RGB", (img_width, img_height))
    draw = ImageDraw.Draw(im, "RGBA")

    draw.rectangle([(0, 0), (img_width, img_height)], fill = "#FFFFFF", outline = "#FFFFFF")

    # Draw all the names
    for author in AUTHORS:
        draw.text((padding, padding + (padding * AUTHORS.index(author))), author, fill = "black", font = FONT)

    # Draw all the first dates
    for date in range(len(DATES)):
        txt_width = FONT.getsize(str(DATES[date]))[0]
        week_num = find_week(DATES[date])
        block_x = (padding * 3) + LONGEST_NAME + LONGEST_DATE + (padding * week_num)
        x_pos = block_x - (txt_width + padding)
        y_pos = padding + (padding * date)
        draw.text((x_pos, y_pos), str(DATES[date]), fill = "black", font = FONT)

    # Draw all the blobs
    for date, commit_data in project:
        commit = json.loads(commit_data)
        week_num = find_week(parser.parse(date))
        block_x = (padding * 3) + LONGEST_NAME + LONGEST_DATE + (padding * week_num)
        block_y = padding + (padding * AUTHORS.index(commit['commit']['author']['name']))
        draw.rectangle([(block_x, block_y),(block_x + padding, block_y + padding)], fill = (92, 212, 247, 64))

    # Draw the names again
    for author in AUTHORS:
        x_pos = img_width - (padding + LONGEST_NAME)
        y_pos = padding + (padding * AUTHORS.index(author))
        draw.text((x_pos, y_pos), author, fill = "black", font = FONT)

    del draw
    im.save("result.png", "PNG")
