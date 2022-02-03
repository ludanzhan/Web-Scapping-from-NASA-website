# Web Scraping
## Project Goal
Builds a web application that scrapes various websites for Mars-related data and displays the information on a single HTML page. 
## Process
### Initial scraping using Jupyter Notebook, BeautifulSoup, Pandas, and Requests/Splinter.
- Setup splinter
  ```python
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
  ```
- URL to be scraped
  ```python
      url = "https://redplanetscience.com/"
      jpl_url = "https://spaceimages-mars.com/"
      facts_url = 'https://galaxyfacts-mars.com/'
      hemis_url = "https://marshemispheres.com/"
      browser.visit(urlName)
      html = browser.html
      soup = bs(html, 'html.parser')
  ```
- Scraping using **BeautifulSoup** based on the inspected **html tag**
  ```python
      hemisphere_image_urls = []
      for image in images:
              # Error handling
              try:
                  # Extract href
                  href = image.a['href']
                  text = image.h3.text
                  browser.visit(hemis_url + href)

                  html=browser.html
                  soup=bs(html,'html.parser')
                  image_src=soup.find('li').a['href']

                  image_url = hemis_url + soup.find('img',class_="wide-image")['src']
                  print(text + ": \n"+ image_url + "\n")

                  hemisphere_dict={
                      "titles" : text,
                      "img_url" : image_url
                  }

                  hemisphere_image_urls.append(hemisphere_dict)

              except Exception as e:
                  print(e)
  ```
- Using Pandas **read_html** to scaping the website and store the information into a DataFrame. Generating html table using **to_html** function
  ```python
    facts_url = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(facts_url)

    # generate HTML tables from DataFrames
    html_table = fact_df.to_html()
    html_table.replace('\n', '')
  ```
### Use MongoDB with Flask templating to create a new HTML page that displays all of the information that was scraped from the URLs above.
- Converting your Jupyter notebook into a Python script 
  ```python
      from splinter import Browser
      from bs4 import BeautifulSoup as bs
      from webdriver_manager.chrome import ChromeDriverManager
      import pandas as pd


      def scrape():
          .
          .  (# similiar to the jupyter notebook, but need to store everything scraped in to a "dictonary")
          .
          
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
  ```
- Create a route "/scrape" that will import Python script 
  ```python
      app = Flask(__name__)

      # Use PyMongo to establish Mongo connection
      mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

      # create route that renders index.html template
      @app.route("/")
      def home():
          # Find one record of data from the mongo database
          mars_data = mongo.db.collection.find_one()

          # Return template and data

          return render_template("index.html",mars = mars_data)
  ```
- Create a root route "/" that will query Mongo database and pass the mars data into an HTML template to display the data.
  ```python
      def scrape():

          # Run the scrape function
          mars_data = scrape_mars.scrape()

          # Insert the record
          mongo.db.collection.update_one({}, {"$set": mars_data}, upsert=True)

          # Redirect back to home page
          return redirect("/")
  ```
- Create a template HTML file called index.html that will take the mars data dictionary and display all of the data in the appropriate HTML elements.

### Final Results
![img](https://github.com/ludanzhan/web-scraping-challenge/blob/main/website%20screen%20shot/Screen%20Shot%202022-02-02%20at%2011.14.36%20PM.png)
![img](https://github.com/ludanzhan/web-scraping-challenge/blob/main/website%20screen%20shot/Screen%20Shot%202022-02-02%20at%2011.14.48%20PM.png)


