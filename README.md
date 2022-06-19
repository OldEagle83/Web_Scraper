# Web_Scraper

This is a simple nature.com article scraper.

It asks the user for a few parameters:
year: The year the script should search articles from.
Type: The type article to search for.
Pages: How many result pages it should scrape nature.com for, starting from page 1 up to (and including) the page entered.

The script will raise an error or stop if any of the following occur:
- There are no articles on the year provided
- There are no result pages
- User has no write permissions in the current working directory

Please refrain from extensively quering nature.com for results as this can result in a temporary ip ban.
