# Adapted from https://nafiulis.me/making-a-static-blog-with-pelican.html

import sys
from datetime import datetime

TEMPLATE = """

Title: {title}
Date: {year}-{month}-{day} {hour}:{minute:02d}
Tags:
Category:
Slug:{slug}

"""

def make_entry(title):
    today = datetime.today()
    slug = title.lower().strip().replace(' ', '-')
    f_create="content/posts/{}_{:0>2}_{:0>2}_{}.md".format(today.year, today.month, today.day, slug)
    t = TEMPLATE.strip().format(title=title, year=today.year, 
                    month=today.month, day=today.day,
                    hour=today.hour, minute=today, slug=slug)
    with open(f_create, 'w') as w:
        w.write(t)
    print("File created -> " + f_create)

if __name__ == '__main__':

	if len(sys.argv) > 1:
		make_entry(sys.argv[1])
	else:
		print("No title given")