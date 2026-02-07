# Erome

A lightweight, robust Python wrapper for Erome.com, supporting both synchronous and asynchronous operations.

[![PyPI version](https://badge.fury.io/py/erome.svg)](https://badge.fury.io/py/erome)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- **Full API Coverage**: Access explore, albums, searches, and user profiles.
- **Sync & Async**: Choose the client that fits your workflow.
- **Pydantic Models**: All responses are typed and validated using Pydantic.
- **Resilient Parsing**: Handles edge cases and changes in Erome's DOM structure.

## Installation

```bash
pip install erome
```

## Quick Start

### Synchronous Client

```python
from erome import Client

client = Client()

# Get featured albums from explore
albums = client.get_explore()
for album in albums:
    print(f"Album: {album.name} (ID: {album.id})")

# Get specific album details
album_id = albums[0].id.split('/')[-1]
album_data = client.get_album(album_id)
print(f"Title: {album_data.title}")
print(f"Videos: {len(album_data.contents['videos'])}")
```

### Asynchronous Client

```python
import asyncio
from erome import AsyncClient

async def main():
    client = AsyncClient()
    
    # Search for albums
    results = await client.get_search("milf")
    print(f"Found {len(results)} search results")
    
    # Get user profile
    profile = await client.get_profile("TheRealWolf")
    print(f"User: {profile.username}, Albums: {len(profile.albums)}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Available Methods

Both `Client` and `AsyncClient` share the same interface (except for `await` in async):

- `get_explore(page=1)`: Fetch featured albums from the explore page.
- `get_album(album_id)`: Get full details for an album, including media links.
- `get_related_albums(album_id)`: Get albums related to the specified one.
- `get_search(query, page=1)`: Search for albums by keyword.
- `get_profile(username, page=1)`: Fetch user profile information and their albums.

## Models

Responses are returned as Pydantic models:

- `AlbumCard`: Basic info used in lists (explore, search, profile).
- `AlbumResponse`: Detailed album information including media links (`MediaItem`).
- `ProfileResponse`: User profile information and a list of `AlbumCard`s.
- `MediaItem`: Direct links to images or videos with metadata (duration, captions).

## Requirements

- Python 3.11+
- `httpx`
- `beautifulsoup4`
- `pydantic`

## License

MIT

## GitHub

[https://github.com/dankaristic/erome](https://github.com/dankaristic/erome)
