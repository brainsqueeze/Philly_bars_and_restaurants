from bs4 import BeautifulSoup
from urllib2 import urlopen
from datetime import date
import sys
import csv
from pygeocoder import Geocoder

base_url = ('http://www.phillymag.com/foobooz/food-drink-guides/')

def GetLinks():
    soup = BeautifulSoup(urlopen(base_url).read())
    GuideList = soup.find('ul', 'guides_list') # Get guide list

    # Pulls the URL for each category (ie. 50-best-rest, etc.)
    CatURLs = [cat.a['href'] for cat in GuideList.findAll('li')]
    return [CatURLs[0], CatURLs[2]]


def MakeRestLists():
    url = GetLinks()[0]
    field = ('Rank', 'Restaurant', 'Neighborhood', 'Location', 'Cuisine Category', 'Price', 'BYOB')

    cat = url.split('/')[-2] # Gets category title
    f = open('Lists/%s_%s.tsv' % (cat, date.today().year - 1), 'wb')
    output = csv.writer(f, delimiter = '\t')
    output.writerow(field)
        

    """ 
    Get restaurant name, they are ranked sequentially 
    can't pull the rank from the site easily, so just
    increment the rank manually.
    """
    ListPage = urlopen(url)
    rank = 1
    soup = BeautifulSoup(ListPage.read()).findAll('ol')
    for column in soup[0:2]:
        for x in column.findAll('li'):
            restaurant = x.find('a', href = True).contents[0]
                                                

            # Get restaurant information
            if restaurant == 'Fat Ham':
                rest = urlopen('http://www.phillymag.com/restaurant/the-fat-ham/')
            else:
                rest = urlopen(x.a['href'])
            detailsDB = BeautifulSoup(rest.read()).find_all('ul', 'db_details_list')
            cuisineList = []
            for x in detailsDB:
                for item in x.find_all('a', href = True):
                    if 'neighborhood' in item['href'].split('/'):
                        neighborhood = item.contents[0]
                    if 'cuisine' in item['href'].split('/'):
                        cuisineList.append(item.contents[0])
                    cuisine = ','.join(cuisineList)

                for item in x.find_all('b'):
                    if len(item.contents[0].split(':')) == 1:
                        Address = Geocoder.geocode(item.contents[0])[0].coordinates
                   
                    
                for item in x.find_all('li'):
                    if len(item.contents) == 2:
                        if '$' in item.contents[1]:
                            price = item.contents[1]
                    if len(item.contents) == 3:
                        if 'Alcohol' in item.contents[1].contents[0].split(':')[0]:
                            if 'BYOB' in item.contents[2].split(',')[0]:
                                BYOB = 1
                            else:
                                BYOB = 0
                    
                                        
            output.writerow([rank, restaurant.encode('ascii', 'ignore'), neighborhood, Address, cuisine, price, BYOB])
            rank += 1
    f.close()



def MakeOldRestLists():
    url = 'http://www.phillymag.com/foobooz/2012/12/26/the-philadelphia-magazine-50-best-restaurants-for-2012/'
    field = ('Rank', 'Restaurant', 'Neighborhood', 'Location', 'Cuisine Category', 'Price', 'BYOB')

    f = open('Lists/50-best-restaurants_2012.tsv', 'wb')
    output = csv.writer(f, delimiter = '\t')
    output.writerow(field)
        

    """ 
    Get restaurant name, they are ranked sequentially 
    can't pull the rank from the site easily, so just
    increment the rank manually.
    """
    ListPage = urlopen(url)
    rank = 1
    soup = BeautifulSoup(ListPage.read()).findAll('ol')
    for column in soup[:1]:
        for x in column.findAll('li'):
            restaurant = x.find('a', href = True).contents[0]
            NewUrl = 'http://www.phillymag.com/restaurant/' + restaurant.replace(' ', '-').replace('&', 'and') + '/'
                        
            # Get restaurant information
            if restaurant == 'Koo Zee Doo':
                rank += 1
                continue
            else:
                rest = urlopen(NewUrl)
            
            detailsDB = BeautifulSoup(rest.read()).find_all('ul', 'db_details_list')
            cuisineList = []
            for x in detailsDB:
                for item in x.find_all('a', href = True):
                    if 'neighborhood' in item['href'].split('/'):
                        neighborhood = item.contents[0]
                    if 'cuisine' in item['href'].split('/'):
                        cuisineList.append(item.contents[0])
                    cuisine = ','.join(cuisineList)

                for item in x.find_all('b'):
                    if len(item.contents[0].split(':')) == 1:
                        Address = Geocoder.geocode(item.contents[0])[0].coordinates

                BYOB = 0
                for item in x.find_all('li'):
                    if len(item.contents) == 2:
                        if '$' in item.contents[1]:
                            price = item.contents[1]

                    if len(item.contents) == 3:
                        if 'Alcohol' in item.contents[1].contents[0].split(':')[0]:
                            if 'BYOB' in item.contents[2].split(',')[0]:
                                BYOB += 1
                            else:
                                BYOB = 0
                                                            
            output.writerow([rank, restaurant.encode('ascii', 'ignore'), neighborhood, Address, cuisine, price, BYOB])
            rank += 1         
    f.close()



def MakeBarLists():
    url = GetLinks()[1]
    field = ('Rank', 'Bar', 'Neighborhood', 'Address', 'Cuisine Category', 'Price')

    cat = url.split('/')[-2] # Gets category title
    f = open('Lists/%s_%s.tsv' % (cat, date.today().year - 1), 'wb')
    output = csv.writer(f, delimiter = '\t')
    output.writerow(field)

    ListPage = urlopen(url)
    rank = 1
    soup = BeautifulSoup(ListPage.read()).findAll('ol')
    for column in soup[0:2]:
        for x in column.findAll('li'):
            Bar = x.find('a', href = True).contents[0]

            bar = urlopen(x.a['href'])
            detailsDB = BeautifulSoup(bar.read()).find_all('ul', 'db_details_list')
            cuisineList = []
            for x in detailsDB:
                for item in x.find_all('a', href = True):
                    if 'neighborhood' in item['href'].split('/'):
                        neighborhood = item.contents[0]
                    if 'cuisine' in item['href'].split('/'):
                        cuisineList.append(item.contents[0])
                    cuisine = ','.join(cuisineList)

                for item in x.find_all('b'):
                    if len(item.contents[0].split(':')) == 1:
                        Address = Geocoder.geocode(item.contents[0])[0].coordinates

                
                for item in x.find_all('li'):
                    if len(item.contents) == 2:
                        if '$' in item.contents[1]:
                            price = item.contents[1]
            
            output.writerow([rank, Bar.encode('ascii', 'ignore'), neighborhood, Address, cuisine, price])
            rank += 1
    f.close()



def MakeOldBarLists():
    base_url = ('http://www.phillymag.com/foobooz/foobooz-50-best-bars-philadelphia/foobooz-50-best-bars-previous-years/')

    soup = BeautifulSoup(urlopen(base_url).read())
    GuideList = soup.find_all('ol')
    field = ('Rank', 'Bar', 'Neighborhood', 'Cuisine Category', 'Price')

    past = 2

    for Lists in GuideList:
        rank = 1
        year = date.today().year - past
        
        f = open('Lists/foobooz-50-best-bars-philadelphia_%s.tsv' % (year), 'wb')
        output = csv.writer(f, delimiter = '\t')
        output.writerow(field)

        for x in Lists.find_all('li'):
            neighborhood = None
            cuisine = None
            price = None
            if x.contents[0].find('em') is None:
                rank += 1
                continue
            else:
                bar = x.contents[0]
            output.writerow([rank, bar.encode('ascii', 'ignore'), neighborhood, cuisine, price])
            rank += 1
        past += 1
        f.close()
        
        



def main():
    args = sys.argv[1:]
    if len(args) < 2:
        print 'Needs "python GetRest.py --makelist [--rest | --bar | --oldrest | --oldbar]"'

    else:
        if args[0] == '--makelist':
            if args[1] == '--rest':
                MakeRestLists()
            elif args[1] == '--oldrest':
                MakeOldRestLists()
            elif args[1] == '--bar':
                MakeBarLists()
            elif args[1] == '--oldbar':
                MakeOldBarLists()
            else:
                print 'Needs "python GetRest.py --makelist [--rest | --bar | --oldrest | --oldbar]"'



if __name__ == '__main__':
    main()
