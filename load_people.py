import asyncio
import os
from typing import Any

import aiohttp
import asyncpg

BASE_URL = "https://www.swapi.tech/api/people"
REQUEST_TIMEOUT = aiohttp.ClientTimeout(total=30)
CONCURRENCY_LIMIT = 10


async def fetch_json(session: aiohttp.ClientSession, url: str, semaphore: asyncio.Semaphore) -> dict[str, Any]:
    async with semaphore:
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.json()


async def fetch_all_person_urls(session: aiohttp.ClientSession, semaphore: asyncio.Semaphore) -> list[str]:
    first_page = await fetch_json(session, BASE_URL, semaphore)
    total_pages = first_page["total_pages"]

    person_urls = [item["url"] for item in first_page["results"]]
    page_urls = [f"{BASE_URL}?page={page}&limit=10" for page in range(2, total_pages + 1)]

    page_tasks = [fetch_json(session, page_url, semaphore) for page_url in page_urls]
    pages = await asyncio.gather(*page_tasks)

    for page in pages:
        person_urls.extend(item["url"] for item in page["results"])

    return person_urls


async def fetch_person(session: aiohttp.ClientSession, url: str, semaphore: asyncio.Semaphore) -> tuple:
    payload = await fetch_json(session, url, semaphore)
    properties = payload["result"]["properties"]
    person_id = int(payload["result"]["uid"])

    return (
        person_id,
        properties.get("birth_year"),
        properties.get("eye_color"),
        properties.get("gender"),
        properties.get("hair_color"),
        properties.get("homeworld"),
        properties.get("mass"),
        properties.get("name"),
        properties.get("skin_color"),
    )


async def save_people(connection: asyncpg.Connection, people: list[tuple]) -> None:
    query = """
        INSERT INTO people (
            id,
            birth_year,
            eye_color,
            gender,
            hair_color,
            homeworld,
            mass,
            name,
            skin_color
        )
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
        ON CONFLICT (id) DO UPDATE SET
            birth_year = EXCLUDED.birth_year,
            eye_color = EXCLUDED.eye_color,
            gender = EXCLUDED.gender,
            hair_color = EXCLUDED.hair_color,
            homeworld = EXCLUDED.homeworld,
            mass = EXCLUDED.mass,
            name = EXCLUDED.name,
            skin_color = EXCLUDED.skin_color;
    """
    await connection.executemany(query, people)


async def main() -> None:
    database_dsn = os.getenv(
        "DATABASE_DSN",
        "postgresql://postgres:postgres@localhost:5432/starwars",
    )

    semaphore = asyncio.Semaphore(CONCURRENCY_LIMIT)

    async with aiohttp.ClientSession(timeout=REQUEST_TIMEOUT) as session:
        person_urls = await fetch_all_person_urls(session, semaphore)
        person_tasks = [fetch_person(session, url, semaphore) for url in person_urls]
        people = await asyncio.gather(*person_tasks)

    people.sort(key=lambda item: item[0])

    connection = await asyncpg.connect(database_dsn)
    try:
        await save_people(connection, people)
    finally:
        await connection.close()

    print(f"Загружено персонажей: {len(people)}")


if __name__ == "__main__":
    asyncio.run(main())
