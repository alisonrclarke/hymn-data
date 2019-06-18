import feedparser
import re
from datetime import datetime
from lxml import html

d = feedparser.parse('http://www.singingthefaithplus.org.uk/?cat=264&feed=atom')

for entry in d.entries[:1]:
    date = datetime.strptime(entry.title, '%A %d %B, %Y')
    print(date)

    data = html.fragments_fromstring(entry.summary)

    # lectionary date is the first top-level <strong> tag
    print(data[0].tag)
    if data[0].tag == 'strong':
        lectionary_date = data[0].text_content()
        print(lectionary_date)

    # Reading is first (top-level) link, to bible.oremus.org
    # Following links (of format /?p=51232) are Hymns
    current_reading = None
    for fragment in data[1:]:
        if fragment.tag == 'a':
            if "http://bible.oremus.org" in fragment.attrib['href']:
                current_reading = fragment.text_content()
                print(current_reading)
                match = re.search("^(\d+ )?(\w+) (.*)$", current_reading)
                print("Reading:" + match.group())
                # FIXME: Currently the above fails at line 53 of the sample file,
                # because there are 2 sets of verses and 2 links.
            elif fragment.attrib['href'].startswith("?p="):
                print("Suggestion: " + fragment.text_content())
