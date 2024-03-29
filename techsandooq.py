from bs4 import BeautifulSoup #Beautiful Soup is a Python library for pulling data out of HTML and XML files
import requests
import pandas as pd #pandas is best for handling data
import re
url = "https://techsandooq.com/list-companies-email/"
html_content = requests.get(url).text
soup = BeautifulSoup(html_content, "lxml")
print(soup.prettify())
gdp = soup.find_all("table", attrs={"class": "tablepress tablepress-id-1"})
print("Number of tables on site: ",len(gdp))
# Lets go ahead and scrape first table with HTML code gdp[0]
table1 = gdp[0]
# the head will form our column names
body = table1.find_all("tr")
# Head values (Column names) are the first items of the body list
head = body[0] # 0th item is the header row
body_rows = body[1:] # All other items becomes the rest of the rows

# Lets now iterate through the head HTML code and make list of clean headings

# Declare empty list to keep Columns names
headings = []
for item in head.find_all("th"): # loop through all th elements
    # convert the th elements to text and strip "\n"
    item = (item.text).rstrip("\n")
    # append the clean column name to headings
    headings.append(item)
print(headings)

# Next is now to loop though the rest of the rows

#print(body_rows[0])
all_rows = [] # will be a list for list for all rows
for row_num in range(len(body_rows)): # A row at a time
    row = [] # this will old entries for one row
    for row_item in body_rows[row_num].find_all("td"): #loop through all row entries
        # row_item.text removes the tags from the entries
        # the following regex is to remove \xa0 and \n and comma from row_item.text
        # xa0 encodes the flag, \n is the newline and comma separates thousands in numbers
        aa = re.sub("(\xa0)|(\n)|,","",row_item.text)
        #append aa to row - note one row entry is being appended
        row.append(aa)
    # append one row to all_rows
    all_rows.append(row)
    
    # We can now use the data on all_rowsa and headings to make a table
# all_rows becomes our data and headings the column names
df = pd.DataFrame(data=all_rows,columns=headings)
df

df.head()
df.columns
result = df.drop(columns = ['Company Website',"Sr. No"])

result
result.to_csv("final.csv")
