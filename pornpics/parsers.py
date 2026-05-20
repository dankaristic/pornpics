import json
import re
from typing import List, Optional

from bs4 import BeautifulSoup
from .models import (
    GalleryResponse, GalleryImage, CategoryItem, TagItem,
    ChannelItem, PornstarItem, GalleryModel, CategoryResponse, HomeMedia
)
from .consts import *

def _soup(html: str) -> BeautifulSoup:
    """Converts HTML string to a BeautifulSoup instance."""
    return BeautifulSoup(html, "html.parser")

def _parse_gallery_images(soup: BeautifulSoup) -> List[GalleryImage]:
    """Extracts images from a gallery page."""
    images = soup.find("ul", id="tiles")
    combo = []
    for image in images.find_all("li", class_="thumbwook"):
        try:
            a_tag = image.find("a", class_="rel-link")
            img_tag = image.find("img")
            if a_tag and img_tag:
                combo.append(GalleryImage(
                    image=a_tag.get("href"),
                    thumbnail=img_tag.get("data-src")
                ))
        except AttributeError:
            continue
    return combo

def _parse_metadata(soup: BeautifulSoup) -> tuple[str, str, str, str]:
    """Extracts metadata (ID, title, rating, views) from a gallery page."""
    id_script_string = soup.find("script", attrs={"type": "text/javascript"}).string
    gallery_id = re.search(r"var\s+ID\s*=\s*'(\d+)'", id_script_string).group(1) if id_script_string else "100000"
    title = soup.find("h1").get_text(strip=True) if soup.find("h1") else ""
    rating = soup.find("span", class_="rate-count").get_text(strip=True) if soup.find("span", class_="rate-count") else ""
    views = soup.find("span", class_="info-views").get_text(strip=True).split(": ")[-1] if soup.find("span", class_="info-views") else ""
    return gallery_id, title, rating, views

def _parse_links(soup: BeautifulSoup) -> tuple[List[CategoryItem], List[TagItem], List[PornstarItem], List[ChannelItem]]:
    """Extracts channels, tags, models, and categories from a gallery page."""
    meta_div = soup.find("div", class_="gallery-info to-gall-info")
    channels, tags, models, categories = [], [], [], []
    if not meta_div:
        return channels, tags, models, categories

    for a_tag in meta_div.find_all("a"):
        href = a_tag.get("href")
        text = a_tag.get_text(strip=True)
        if href.startswith(CHANNELS_PATH):
            channels.append(ChannelItem(name=text, slug=href))
        elif href.startswith(PORNSTARS_PATH):
            models.append(PornstarItem(name=text, slug=href))
        elif href.startswith(TAGS_PATH):
            tags.append(TagItem(name=text, slug=href))
        else:
            categories.append(CategoryItem(name=text, slug=href))
    return channels, tags, models, categories

def parse_gallery_item(html: str) -> GalleryResponse:
    """
    Parses a gallery page into a GalleryResponse object.
    """
    soup = _soup(html)
    images = _parse_gallery_images(soup)
    gallery_id, title, rating, views = _parse_metadata(soup)
    channels, tags, models, categories = _parse_links(soup)

    return GalleryResponse(
        gallery_id=gallery_id,
        slug=soup.find("a", class_="alt-lang-item").get("href").replace(f"{BASE_URL}{GALLERIES_PATH}", "")[:-1],
        title=title,
        images=images,
        models=models,
        channels=channels,
        tags=tags,
        categories=categories,
        rating=rating,
        views=views
    )

def parse_category_item(html: str, offset: int = 0) -> CategoryResponse:
    """
    Parses a category or tag page into a CategoryResponse object.
    """
    combo = []
    main_slug = None
    main_title = None
    tags = []
    categories = []

    if offset > 0:
        try:
            soup = json.loads(html)
            items = soup if isinstance(soup, list) else soup.get("items", [])
            for item in items:
                gallery_url = item.get("g_url", "")
                gid = item.get("gid")
                slug = gallery_url.split(GALLERIES_PATH)[-1].strip("/") if gallery_url else ""
                title = item.get("desc", "") or item.get("title", "")
                thumbnail = item.get("t_url", "") or item.get("thumb", "")
                combo.append(GalleryModel(gid=gid, slug=slug, thumbnail=thumbnail, title=title))
        except (json.JSONDecodeError, AttributeError):
            pass
    else:
        soup = _soup(html)
        images = soup.find("ul", id="tiles")
        for image in images.find_all("li", class_="thumbwook"):
            try:
                a_tag = image.find("a", class_="rel-link")
                img_tag = image.find("img")
                if a_tag and img_tag:
                    slug = a_tag.get("href").replace(f"{BASE_URL}{GALLERIES_PATH}", "")[:-1]
                    combo.append(GalleryModel(
                        gid=slug.split("-")[-1],
                        slug=slug,
                        thumbnail=img_tag.get("data-src"),
                        title=img_tag.get("alt")
                    ))
            except AttributeError:
                continue

        main_slug_tag = soup.find("a", class_="alt-lang-item")
        main_slug = main_slug_tag.get("href").replace(f"{BASE_URL}/", "").split("/")[0] if main_slug_tag else None
        main_title = soup.find("h1").get_text(strip=True) if soup.find("h1") else None

        tags_div = soup.find("div", id="tags-section")
        for tag in tags_div.find_all("li"):
            a_tag = tag.find("a")
            if a_tag:
                href = a_tag.get("href")
                text = a_tag.get_text(strip=True)
                if href.startswith(TAGS_PATH):
                    tags.append(TagItem(name=text, slug=href))
                else:
                    categories.append(CategoryItem(name=text, slug=href))

    return CategoryResponse(
        slug=main_slug,
        title=main_title,
        tags=tags,
        categories=categories,
        galleries=combo
    )

def parse_home_page(html: str) -> List[HomeMedia]:
    """Parses the home page HTML to extract featured media (tags and categories).

    Args:
        html (str): The HTML content of the home page.

    Returns:
        List[HomeMedia]: A list of `HomeMedia` objects representing the featured tags and categories.
                       Each object contains the link, type (tag/category), name, and thumbnail.
    """
    soup = _soup(html)
    images = soup.find('ul', id="tiles")
    combo = []

    if images:
        for image in images.find_all('li', class_='thumbwook'):
            try:
                a_tag = image.find('a')
                link = a_tag.get('href') if a_tag else ""
                media_type = "tag" if link.startswith("/tags/") else "category"
                name = image.find('span', class_='h2').get_text(strip=True)
                thumbnail = image.find('img').get('data-src')
                combo.append(HomeMedia(
                    link=link,
                    type=media_type,
                    name=name,
                    thumbnail=thumbnail
                ))
            except AttributeError:
                continue

    return combo

def parse_search_page(html: str, offset: int = 0) -> List[GalleryModel]:
    combo = []
    try:
        soup = json.loads(html)
        items = soup if isinstance(soup, list) else soup.get("items", [])
        for item in items:
            gallery_url = item.get("g_url", "")
            gid = item.get("gid")
            slug = gallery_url.split(GALLERIES_PATH)[-1].strip("/") if gallery_url else ""
            title = item.get("desc", "") or item.get("title", "")
            thumbnail = item.get("t_url", "") or item.get("thumb", "")
            combo.append(GalleryModel(gid=gid, slug=slug, thumbnail=thumbnail, title=title))
    except (json.JSONDecodeError, AttributeError):
        pass

    return combo