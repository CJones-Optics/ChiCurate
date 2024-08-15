import feedparser
import pandas as pd

def getAbstract(rssItem):
    # from the summary item, extract the string after "Abstract: "
    summary = rssItem['summary']
    abstract = summary[summary.find("Abstract: ")+len("Abstract: "):]
    return abstract

def parse_rss_feed(url):
    # Parse the RSS feed
    feed = feedparser.parse(url)

    # Initialize an empty list to store the feed items
    feed_items = []

    # Loop through each entry in the feed
    for entry in feed.entries:
        # Create a dictionary for each entry
        item = {
            'id': entry.get('id', None),
            'title': entry.get('title', None),
            'link': entry.get('link', None),
            'summary': entry.get('summary', None),
            'category': entry.get('category', None)
        }
        # Append the dictionary to the list
        item["abstract"] = getAbstract(item)
        feed_items.append(item)

    return feed_items


def parse_rss_feed_DF(url):
    # Parse the RSS feed
    feed = feedparser.parse(url)

    # Initialize a list to store the feed items
    feed_items = []

    # Loop through each entry in the feed
    for entry in feed.entries:
        # Create a dictionary for each entry
        item = {
            'id': entry.get('id', None),
            'title': entry.get('title', None),
            'link': entry.get('link', None),
            'summary': entry.get('summary', None),
            'category': entry.get('category', None)
        }

        item["abstract"] = getAbstract(item)
        # Get the PDF url by find and replace
        # the 'abs' substring with 'pdf'
        pdfUrl = item['link'].replace('abs', 'pdf')
        item['pdf'] = pdfUrl

        # Append the dictionary to the list
        feed_items.append(item)


    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(feed_items)

    return df


if __name__=="__main__":
    # Example usage
    url = 'https://rss.arxiv.org/atom/astro-ph.IM'
    # rss_items = parse_rss_feed(url)
    # print(f"Number of items in the feed: {len(rss_items)}")

    # print (rss_items[0]['summary'])
    rss_df = parse_rss_feed_DF(url)
    print(rss_df)
