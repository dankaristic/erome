# parsers.py
import re
from typing import List

from bs4 import BeautifulSoup
from erome.models import MediaItem, AlbumResponse, AlbumCard, ProfileResponse
from erome.exceptions import ParseError


def _soup(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "html.parser")

def _parse_album_card(album) -> AlbumCard:
    album_link = album.find("a")
    album_img = album.find("img")
    album_title = album.find("a", class_="album-title")
    views_tag = album.find("span", class_="album-bottom-views")

    if not all([album_link, album_img, album_title, views_tag]):
        raise ParseError("Invalid album card")

    return AlbumCard(
        id=album_link["href"].replace("https://www.erome.com/a/", ""),
        thumb=album_img.get("data-src"),
        name=album_title.get_text(strip=True),
        views=views_tag.get_text(strip=True),
        images=(
            album.find("span", class_="album-images").get_text(strip=True)
            if album.find("span", class_="album-images") else None
        ),
        videos=(
            album.find("span", class_="album-videos").get_text(strip=True)
            if album.find("span", class_="album-videos") else None
        ),
    )

def parse_albums(html: str):
    soup = _soup(html)
    container = soup.find("div", id="albums")
    if not container:
        raise ParseError("Albums container missing")

    data = []
    for album in container.find_all("div", id=re.compile(r"^album-\d+$")):
        try:
            data.append(_parse_album_card(album))
        except ParseError:
            continue

    return data

def _process_media_group(item):
    video = None
    image = None

    if v := item.find("div", class_="video"):
        source = v.find("source")
        duration_tag = v.find("span", class_="duration")

        if source:
            video = MediaItem(
                link=source.get("src"),
                duration=duration_tag.text.strip() if duration_tag else None
            )

    if i := item.find("div", class_="img"):
        img = i.find("img")
        if img and img.get("data-src"):
            image = MediaItem(
                link=img.get("data-src"),
                caption=img.get("alt")
            )

    return video, image


def parse_album(html: str, album_id: str) -> AlbumResponse:
    soup = _soup(html)

    # Some albums use different IDs in the DOM or don't have this specific div
    # Let's try to find the main content div more reliably
    album = soup.find("div", id=f"album_{album_id}") or soup.find("div", id="album_content") or soup.find("div", class_="album-content")
    
    if not album:
        # Fallback to looking for media-group elements in the whole page if specific container is not found
        album = soup

    title_tag = soup.find("h1")
    title = title_tag.get_text(strip=True) if title_tag else "Unknown Album"
    username_tag = soup.find("a", id="user_name")
    username = username_tag.get_text(strip=True) if username_tag else "Unknown"

    icon_tag = soup.find("a", id="user_icon")
    icon = icon_tag.find("img").get("src") if icon_tag and icon_tag.find("img") else None

    total_images = "0"
    total_videos = "0"

    info_div = soup.find("div", class_="col-sm-7 user-info text-right")
    if info_div:
        for span in info_div.find_all("span"):
            svg = span.find("svg")
            if svg:
                classes = svg.get("class", [])
                if "svg-fas-fa-camera" in classes:
                    total_images = span.get_text(strip=True)
                elif "svg-fas-fa-video" in classes:
                    total_videos = span.get_text(strip=True)

    contents = {"videos": [], "images": []}

    for item in album.find_all("div", class_="media-group"):
        v, i = _process_media_group(item)
        if v:
            contents["videos"].append(v)
        if i:
            contents["images"].append(i)

    return AlbumResponse(
        title=title,
        album_id=album_id,
        username=username,
        icon=icon,
        total_images=total_images,
        total_videos=total_videos,
        contents=contents,
        success=True,
        message=None,
    )


def parse_search(html: str):
    return parse_albums(html)

def parse_profile(html: str, page: int) -> ProfileResponse:
    soup = _soup(html)

    albums_container = soup.find("div", id="albums")
    if not albums_container:
        raise ParseError("Albums container missing")

    albums: List[AlbumCard] = []
    for album in albums_container.find_all("div", id=re.compile(r"^album-\d+$")):
        try:
            albums.append(_parse_album_card(album))
        except ParseError:
            continue

    username = None
    icon = None
    metadata = {}

    # Only page 1 has user meta
    if page == 1:
        user_div = soup.find("div", id="user")
        if user_div:
            img = user_div.find("img")
            icon = img.get("src") if img else None

        uname_tag = soup.find("h1", class_="username")
        username = uname_tag.get_text(strip=True) if uname_tag else None

        meta_tag = soup.find("div", class_="col-xs-12 user-info text-center")
        if meta_tag:
            for span in meta_tag.find_all("span"):
                text = span.get_text(strip=True).lower()
                for key in ["albums", "views", "followers", "following"]:
                    if key in text:
                        metadata[key] = text.replace(key, "").strip()

    return ProfileResponse(
        username=username,
        icon=icon,
        metadata=metadata,
        albums=albums,
        page=page,
    )

