from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


def scrape():
    # browser = init_browser()
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    mars_data = {}

    # NASA Mars News
    news_url = "https://redplanetscience.com/"
    browser.visit(news_url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    titles = soup.find_all('div', class_='content_title')[0].text
    paragraphs  = soup.find_all('div', class_='article_teaser_body')[0].text

    # JPL Mars Space Images - Featured Image
    jpl_url = "https://spaceimages-mars.com/"
    browser.visit(jpl_url)

    featured_image_url = soup.find('img', class_="headerimage fade-in")['src']

    # Mars Facts

    fact_url = "https://galaxyfacts-mars.com/"
    tables = pd.read_html(fact_url)

    fact_df = tables[0]
    fact_df = fact_df.rename(columns={
        0: "Mars - Earth Comparison", 1: "Mars", 2: "Earth"})

    fact_df = fact_df.drop([0, 0])
    fact_df.set_index("Mars - Earth Comparison", inplace=True)

    html_table = fact_df.to_html()
    html_table.replace('\n', '')

    # Mars Hemispheres
    hemis_url = "https://marshemispheres.com/"
    browser.visit(hemis_url)

    html = browser.html
    soup = bs(html, 'html.parser')

    images = soup.find_all('div', class_="description")

    hemisphere_image_urls = []
    for image in images:
        # Error handling
        try:
            # Extract href
            href = image.a['href']
            text = image.h3.text
            browser.visit(hemis_url + href )

            html = browser.html
            soup = bs(html, 'html.parser')
            image_src = soup.find('li').a['href']

            image_url = soup.find('img', class_="wide-image")['src']
            print(text + ": \n" + image_url + "\n")

            hemisphere_dict = {
                "titles": text,
                "img_url": image_url
            }

            hemisphere_image_urls.append(hemisphere_dict)

        except Exception as e:
            print(e)

    # Store data in a dictionary
    mars_data = {
        "news_title": titles,
        "news_p": paragraphs,
        "featured_image": featured_image_url,
        "hemisphere_image_urls": hemisphere_image_urls,
        "html_table": html_table
    }

    # Quit the browser
    browser.quit()

    return mars_data
