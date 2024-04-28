from flask import Flask, abort,request
import requests
import json
from bs4 import BeautifulSoup
import pandas as pd

app = Flask(__name__)
blocked_user_agents = ["Go-http-client/1.1"]
@app.before_request
def block_user_agent():
    user_agent = request.headers.get('User-Agent')
    if user_agent in blocked_user_agents:
        abort(403)

@app.route('/')
def hello_world():
    URLS = "https://trendlyne.com/portfolio/bulk-block-deals/54044/vanguard-fund/"

    headers={"authority":"trendlyne.com",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding":"gzip, deflate, br, zstd",
    "Accept-Language":"en-US,en;q=0.9",
    "Sec-Ch-Ua":'"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    "User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
    "Cookie":"csrftoken=fJIHWYF2RLrOTf5nYqwAHitEkOt9bDyYHwoflEeRr3YBFYE35gLYituFIvWh0wXa"
    }
    df = None

    response = requests.get(URLS,headers=headers)
    soup = BeautifulSoup(response.text,'html.parser')
    list_col_name=soup.find_all('tr')[0].find_all('th')
    list_rows = soup.find_all('tr')[1:]
    result = []
    result.append([col.text for col in list_col_name])
    result[0].append("Stock Link")

    for tr in list_rows:
        temp=[]
        for td in tr.find_all('td'):
            temp.append(td.get_text().strip())
        temp.append("https://trendlyne.com"+tr.find('a')['href'])
        result.append(temp)
    if df is None:
        df = pd.DataFrame(result[1:],columns=result[0])
    else:
        df = pd.concat([df,pd.DataFrame(result[1:],columns=result[0])],ignore_index=False)

    return str(df)


if __name__ == '__main__':
    app.run(debug=True,port=5002,host='0.0.0.0')
