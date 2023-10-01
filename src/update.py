import json
import logging
import re

import requests as requests

logging.basicConfig(
    level=logging.INFO, format='[%(asctime)s] %(message)s',
    datefmt='%m.%d %H:%M:%S')

if __name__ == '__main__':
    logger = logging.getLogger(__name__)

    r = requests.get('https://codingman.cc/post_list.json', verify=False, timeout=3)

    if r.status_code != 200:
        logger.error('Failed to get post_list.json')
        exit(1)

    post_list = r.json()

    logger.info(json.dumps(post_list, indent=4, ensure_ascii=False))

    new_post_list = None
    for post in post_list:
        # - [簡單易用的剪貼簿工具 - Clipy](https://codingman.cc/scrapbook-tool-clipy/)
        logger.info(f"{post['title']}\n{post['url']}")

        title = post['title']
        url = post['url']

        if new_post_list is None:
            new_post_list = f"- [{title}]({url})"
        else:
            new_post_list += f"\n- [{title}]({url})"

    logger.info(f'\n{new_post_list}')

    with open('./README.md', 'r') as f:
        readme = f.read()

    pattern = r'<!-- BLOG-POST-LIST:START -->\n(.+?)\n<!-- BLOG-POST-LIST:END -->'

    match = re.search(pattern, readme, re.DOTALL)

    if match:
        logger.info("Matched.")
        old_post_list = match.group(1)
        new_readme = readme.replace(old_post_list, new_post_list)

        logger.info(new_readme)

        with open('./README.md', 'w') as f:
            f.write(new_readme)
    else:
        logger.info("Not matched.")
        exit(1)

    logger.info("Done.")
