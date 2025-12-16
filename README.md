# IMDB-Scraper

[Ir a la versión en Español](./README_es.md)

## Project overview

This project is a Python scraper that queries IMDb, retrieves detailed information about titles (movies, series, episodes), and optionally downloads the associated poster image to a local path.​​
It uses the Requests library with a persistent Session and BeautifulSoup to parse HTML from IMDb’s Spanish interface (https://www.imdb.com/es-es).​​

### How it works

    * The IMDB class exposes a search(query: str) method that sends a GET request to IMDb’s search endpoint and parses the results list.

    * The get_info(url: URL) method receives a specific title URL and extracts fields such as title, original title, duration, synopsis, genres, rating, and poster image path, returning a FinalResult object.​

Internally, helper methods parse specific sections and tags using CSS-like attributes, and dedicated utility functions handle URL normalization and image download.

### Main features

    * Search titles on IMDb by free-text query and get a structured list of candidates (ResultReturned).

    * Extract detailed information of a selected title, including rating, genres, and plot synopsis from the main content section.​

    * Download and save the poster image to disk using helper functions that wrap image lookup and binary download logic.​

### Technologies used

    * Python 3

    * requests for HTTP communication

    * BeautifulSoup (bs4) for HTML parsing

    * yarl URL objects to manage URLs

    * Custom exception types (TagNotFound) and data structures (ResultReturned, FinalResult) to clearly signal parsing errors and encapsulate results.​

### Usage

    * Instantiate the client: create an IMDB() object to initialize the base URL, session, and headers (User-Agent).

    * Call search("your query") and select one of the returned ResultReturned URLs.

    * Pass the selected URL to get_info() to obtain a FinalResult with all parsed attributes and the local poster image path if download succeeds.​

The code is designed to raise a RuntimeError on connection issues and a TagNotFound error when IMDb’s HTML structure changes and required tags cannot be located.

### Usage example:
```python3
im_db = IMDB()

# this will return an object list of ResultReturned type, it contains name and url
result = imdb.search("Avatar La leyenda de Aang")

# now we iterate over all the result and we pass to .get_info from the class, this will return an object FinalResult with all the info for each one
for res in result:
    tv = im_db.get_info(res.url)
    print(tv)
```

### FAQ

    * Is this project affiliated with IMDb?
        - No. This is an independent educational/utility scraper and is not affiliated with or endorsed by IMDb. Always review IMDb’s Terms of Use before scraping.​

    * Can this scraper break in the future?
        - Yes. If IMDb changes its HTML structure or CSS class names, methods that depend on those selectors may raise TagNotFound and need to be updated.​

    * What data does it return for a title?
        - It returns the main title, original title (when available), duration, synopsis, genres, average rating, and the local path of the downloaded poster image, wrapped in a FinalResult object.​

    * Can I change the language or base URL?
        - The current implementation targets https://www.imdb.com/es-es. You can modify self.url or extend the class to support other locales or endpoints as needed. But i can't afford it's gonna work.​​

    * Is this suitable for large-scale crawling?
        - It is primarily intended for small-scale or personal use. For large-scale scraping, consider adding politeness mechanisms (delays, rotation, error handling) and possibly specialized scraping infrastructure.​