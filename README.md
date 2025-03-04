**Active URL Tester**

Over the years, I've bookmarked thousands of websites (>4K bookmarks). Some of these links have become inactive, so I created this Python script to check which ones are still accessible. This helps me remove broken links and better organize my bookmark folders.

The script performs a TCP test on a list of URLs extracted from an HTML file (the default format for Chrome/Firefox bookmark exports). It runs in parallel with a default of 10 worker threads, and the results are printed to the console.
