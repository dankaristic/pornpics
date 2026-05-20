# PornPics Python Wrapper

[![PyPI version](https://badge.fury.io/py/pornpics.svg)](https://badge.fury.io/py/pornpics)

An unofficial, developer-friendly Python wrapper for the PornPics website. It provides a clean, high-level interface for fetching galleries, categories, and search results, with both synchronous and asynchronous clients.

## Features

- **Simple & Clean:** A straightforward and easy-to-use API.
- **Sync & Async:** Provides both `Client` (for synchronous code) and `AsyncClient` (for `asyncio` applications).
- **Type-Hinted:** Fully type-hinted for a better developer experience with tools like MyPy and modern IDEs.
- **Data Models:** Uses Pydantic models for robust and clear data representation.
- **No API Key Needed:** Interacts with the website directly, so no API key is required.

## Installation

Install the package from PyPI using pip:

```bash
pip install pornpics
```

## Quick Start

### Synchronous Client

Here's a simple example of how to use the synchronous `Client`:

```python
from pornpics import Client

# Initialize the client
client = Client()

# 1. Get the homepage to discover categories and tags
print("--- Fetching Homepage ---")
homepage_items = client.get_home()
for item in homepage_items:
    print(f"Found {item.type}: {item.name} -> {item.link}")

# 2. Search for galleries
print("\n--- Searching for 'amateur' ---")
search_results = client.search("amateur")
if search_results.galleries:
    print(f"Found {search_results.total_galleries} galleries.")
    for gallery in search_results.galleries:
        print(f"- {gallery.title} ({len(gallery.images)} images)")

    # 3. Fetch a specific gallery from the search results
    first_gallery_slug = search_results.galleries[0].slug
    print(f"\n--- Fetching gallery: {first_gallery_slug} ---")
    gallery_details = client.get_gallery(first_gallery_slug)
    print(f"Title: {gallery_details.title}")
    print(f"Tags: {gallery_details.tags}")
    print(f"Image URLs: {[img.url for img in gallery_details.images]}")

# 4. Fetch a category page
print("\n--- Fetching category 'teen' ---")
category_page = client.get_category("teen") # 'teen' is the slug
print(f"Category has {category_page.total_galleries} galleries.")
for gallery in category_page.galleries:
    print(f"- {gallery.title}")
```

### Asynchronous Client

The `AsyncClient` provides the same functionality but with `async/await` syntax.

```python
import asyncio
from pornpics import AsyncClient

async def main():
    # Initialize the async client
    client = AsyncClient()

    # Search for galleries asynchronously
    print("--- Searching for 'ebony' (async) ---")
    search_results = await client.search("ebony")
    if search_results.galleries:
        print(f"Found {search_results.total_galleries} galleries.")

        # Fetch the first gallery
        first_gallery_slug = search_results.galleries[0].slug
        gallery_details = await client.get_gallery(first_gallery_slug)
        print(f"Fetched gallery: {gallery_details.title}")

if __name__ == "__main__":
    asyncio.run(main())
```

## API Reference

### `Client` and `AsyncClient`

Both clients provide the same methods. The only difference is that `AsyncClient` methods are coroutines and must be awaited.

- `get_home()`: Fetches the homepage and returns a list of featured `HomeMedia` objects (tags and categories).
- `search(query, lang="en", offset=0, limit=0)`: Performs a search. Returns a `SearchResponse` object containing a list of `Gallery` previews.
- `get_gallery(slug)`: Fetches a single, detailed gallery by its URL slug. Returns a `GalleryResponse` object with full-resolution image URLs and metadata.
- `get_category(slug, offset=0, limit=20)`: Fetches a category or tag page by its slug. Returns a `CategoryResponse` object containing a paginated list of `Gallery` previews.

## Data Models

The wrapper uses Pydantic models to structure the returned data. Key models include:

- `GalleryResponse`: A full gallery with title, tags, and a list of `Image` objects.
- `CategoryResponse`: A category page with total gallery count and a list of `Gallery` previews.
- `SearchResponse`: Search results with total gallery count and a list of `Gallery` previews.
- `HomeMedia`: An item from the homepage, representing a tag or category.
- `Gallery`: A gallery preview, typically found in search or category listings.
- `Image`: A single image with its URL and thumbnail URL.

## Future Enhancements

Support for proxies, cookies, and custom headers is planned for a future release. The architecture is designed to easily accommodate these features by extending the `Client` and `AsyncClient` constructors.

## Disclaimer

This is an unofficial wrapper and is not affiliated with, endorsed, or sponsored by PornPics. Please use it responsibly.
