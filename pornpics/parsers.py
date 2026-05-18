import re

from bs4 import BeautifulSoup
from .models import GalleryItem, GalleryImage, CategoryItem, TagItem, ChannelItem, ModelItem


def _soup(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "html.parser")


def parse_gallery_item(html: str):
    soup = _soup(html)
    combo = []
    images = soup.find('ul', id="tiles")
    for image in images.find_all('li', class_='thumbwook'):
        try:
            image_link = image.find('a', class_='rel-link').get("href")
            thumbnail = image.find("img").get("data-src")

            combo.append(GalleryImage(
                image=image_link,
                thumbnail=thumbnail
            ))
        except Exception:
            continue

    id_script_string = soup.find("script", attrs={"type": "text/javascript"}).string
    match = re.search(r"var\s+ID\s*=\s*'(\d+)'", id_script_string)
    gallery_id = 100000

    if match:
        gallery_id = match.group(1)

    title = soup.find("h1").get_text(strip=True)
    rating = soup.find("span", class_="rate-count").get_text(strip=True)
    views = soup.find("span", class_="info-views").get_text(strip=True).split(": ")[-1]
    meta_div = soup.find("div", class_="gallery-info to-gall-info")
    # get channels
    channels = []
    tags = []
    models = []
    categories = []

    div_tags = meta_div.find_all("a")
    for a_tag in div_tags:
        href = a_tag.get("href")
        if href.startswith("/channels/"):
            channels.append(ChannelItem(
                name=a_tag.get_text(strip=True),
                slug=href
            ))
        elif href.startswith("/pornstars/"):
            models.append(ModelItem(
                name=a_tag.get_text(strip=True),
                slug=href
            ))
        elif href.startswith("/tags/"):
            tags.append(TagItem(
                name=a_tag.get_text(strip=True),
                slug=href
            ))
        else:
            categories.append(CategoryItem(
                name=a_tag.get_text(strip=True),
                slug=href
            ))

    return GalleryItem(
        gallery_id=gallery_id,
        slug=soup.find("a", class_="alt-lang-item").get("href").replace("https://www.pornpics.com/galleries/", "")[:-1],
        title=title,
        images=combo,
        models=models,
        channels=channels,
        tags=tags,
        categories=categories,
        rating=rating,
        views=views
    )

