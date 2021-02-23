from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    # Setting up windows browser chromedrivermanager
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()

    # Title/paragraph
    # Visit website
    url1 = "https://mars.nasa.gov/news/"
    browser.visit(url1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    news_title = soup.find_all('div', class_='content_title')[0].text
    news_p = soup.find_all('div', class_='article_teaser_body')[0].text

    print(news_title)
    print(news_p)

    # Featured image
    base_url = "https://data-class-jpl-space.s3.amazonaws.com/"
    url2 = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    browser.visit(url2)
    browser.links.find_by_partial_text('FULL IMAGE')

    html = browser.html
    soup = bs(html, "html.parser")

    image_url = soup.find('img', class_="headerimage fade-in")["src"] 

    featured_image_url = base_url + image_url
    print(featured_image_url)

    # Mars facts
    url3 = "https://space-facts.com/mars/"
    browser.visit(url3)

    html = browser.html
    soup = bs(html, "html.parser")

    mars_table = pd.read_html(url3)
    mars_table

    df = mars_table[0]
    df

    df.columns = ["Fact", "Value"]
    df.set_index("Fact",inplace=True)
    df

    html_table=df.to_html()
    html_table

    # Hemispiheres
    base_url = "https://astrogeology.usgs.gov/"
    url4 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url4)

    html = browser.html
    soup = bs(html, "html.parser")

    title_url_hem = []

    results = soup.find("div", class_ = "result-list" )
    mars_item = results.find_all("div", class_="item")

    base_url = "https://astrogeology.usgs.gov"

    for x in mars_item:
        #title
        title = x.find('h3').text
        #print(title)
        
        # URL
        img_url = x.find('a')["href"]
        link = base_url + img_url
        browser.visit(link)
        html=browser.html
        soup=bs(html,'html.parser')
        image_src=soup.find('li').a['href']
        
        # populate dictionary  
        title_url_hem.append({"title" : title, "URL" : image_src})
        
        print(title_url_hem)


    # Store all data above into dictionary
    mars_dict = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_facts": html_table,
        "hemisphere_image_urls": title_url_hem
        }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_dict

#if __name__ == '__main__':
    #scrape()
    
