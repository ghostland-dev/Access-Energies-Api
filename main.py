import  json, requests, datetime, httpx
from fetching import electricity, get_templates , make_request , Query , JSONResponse ,date, timedelta, calculate_average
from fastapi import Depends, FastAPI, HTTPException, Request

# Get the current date and time
current_datetime = datetime.datetime.now()
# Calculate the next year and format it as a two-digit string
next_year = (current_datetime.year + 1) % 100
next_year_str = str(next_year).zfill(2)

# [1 Petrole] - [2 CO2] - [3 Charbon]
drivers_Codes = [5430841,7440404,5467855]

app = FastAPI(
    title='Voltaria API Energies DATA',
    description="Une API REST pour récoler les données de marche de l'energies pour le gaz naturel et l'éléctricité ainsi que l'actualité de l'énergie. "
    )


# Electrcité Baseload et Peakload

@app.get("/api/v1/e-market/electricite" , tags=["Eléctricité - Spot"])
async def get_electricity_data(
    trading_date: str = Query(default=date.today().strftime("%Y-%m-%d")),
    delivery_date: str = Query(default=(date.today() + timedelta(days=1)).strftime("%Y-%m-%d"))
):
    data = electricity(trading_date, delivery_date)
    return JSONResponse(content=data)

@app.get("/api/v1/e-market/futur/interjournalier/electricite/spot", tags=["Eléctricité - Futur"])
async def get_electricity_data(
    type : str = Query(default='B'),
    annee : str = Query(    default=next_year_str),
    trading_date: str = Query(default=date.today().strftime("%Y-%m-%d")),
    delivery_date: str = Query(default=(date.today() + timedelta(days=1)).strftime("%Y-%m-%d"))
):
    reqUrl = f"https://webservice-eex.gvsi.com/query/json/getChain/gv.pricesymbol/gv.displaydate/gv.expirationdate/tradedatetimegmt/gv.eexdeliverystart/ontradeprice/close/onexchsingletradevolume/onexchtradevolumeeex/offexchtradevolumeeex/openinterest/?priceSymbol=%22%2FE.F7{type.upper()}YF{annee}%22&chartstartdate={trading_date}&chartstarttime=00%3A00%3A00&chartstopdate={delivery_date}&chartstoptime=00%3A00%3A00"

  
    headersList = {
    "Accept": "*/*",
    "Referer": "https://www.eex.com"
    }

    payload = ""

    response = requests.request("GET", reqUrl, data=payload,  headers=headersList)
    data = json.loads(response.text)
    return JSONResponse(content=data)

@app.get("/api/v1/e-market/futur/fin-de-journee/electricite/spot", tags=["Eléctricité - Futur"])
async def get_electricity_data(
    type : str = Query(default='B'),
    annee : str = Query(    default=next_year_str),
    trading_date: str = Query(default=date.today().strftime("%Y-%m-%d")),
    delivery_date: str = Query(default=(date.today() + timedelta(days=1)).strftime("%Y-%m-%d"))
):
    reqUrl = f"https://webservice-eex.gvsi.com/query/json/getDaily/close/offexchtradevolumeeex/onexchtradevolumeeex/tradedatetimegmt/?priceSymbol=%22%2FE.F7{type.upper()}YF{annee}%22&chartstartdate={trading_date}&chartstopdate={delivery_date}&dailybarinterval=Days&aggregatepriceselection=First"

 
    headersList = {
    "Accept": "*/*",
    "Referer": "https://www.eex.com"
    }

    payload = ""

    response = requests.request("GET", reqUrl, data=payload,  headers=headersList)
    data = json.loads(response.text)
    return JSONResponse(content=data)

# DRIVERS

@app.post("/api/v1/e-market/petrole",  tags=["Drivers"])
async def get_petrole(period: int, request: Request):
    try:
        market_data = await make_request(drivers_Codes[0], period )
        return market_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/e-market/co2",  tags=["Drivers"])
async def get_co2(period: int, request: Request):
    try:
        market_data = await make_request(drivers_Codes[1], period )
        return market_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/e-market/charbon",  tags=["Drivers"])
async def get_charbon(period: int, request: Request):
    try:
        market_data = await make_request(drivers_Codes[2], period )
        return market_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Gaz Naturel SPOT

@app.get("/api/v1/e-market/spot/fin-de-journee/gaz",  tags=["Gaz Naturel - SPOT"])
async def get_electricity_data(
    type : str = Query(default='B'),
    # annee : str = Query(    default=next_year_str),
    trading_date: str = Query(default=date.today().strftime("%Y-%m-%d")),
    delivery_date: str = Query(default=(date.today() + timedelta(days=1)).strftime("%Y-%m-%d"))
):
    reqUrl = f"https://webservice-eex.gvsi.com/query/json/getDaily/close/onexchtradevolumeeex/tradedatetimegmt/?priceSymbol=%22%23E.CEGH_GND1%22&chartstartdate={trading_date}&chartstopdate={delivery_date}&dailybarinterval=Days&aggregatepriceselection=First"

  
    headersList = {
    "Accept": "*/*",
    "Referer": "https://www.eex.com"
    }

    payload = ""

    response = requests.request("GET", reqUrl, data=payload,  headers=headersList)
    data = json.loads(response.text)
    return JSONResponse(content=data)

@app.get("/api/v1/e-market/spot/interajournalier/gaz",  tags=["Gaz Naturel - SPOT"])
async def get_electricity_data(
    # type : str = Query(default='B'),
    # annee : str = Query(    default=next_year_str),
    trading_date: str = Query(default=date.today().strftime("%Y-%m-%d")),
    # delivery_date: str = Query(default=(date.today() + timedelta(days=1)).strftime("%Y-%m-%d"))
):
    reqUrl = f"https://webservice-eex.gvsi.com/query/json/getHistoricalTick/ontradeprice/onexchsingletradevolume/tradedatetimegmt/?priceSymbol=%22%23E.CEGH_GND1%22&maxrowcount=1000&chartstopdate={trading_date}&chartstoptime=22%3A00%3A0"

  
    headersList = {
    "Accept": "*/*",
    "Referer": "https://www.eex.com"
    }

    payload = ""

    response = requests.request("GET", reqUrl, data=payload,  headers=headersList)
    data = json.loads(response.text)
    return JSONResponse(content=data)

@app.get("/api/v1/e-market/futur/gaz",  tags=["Gaz Naturel - Prix Futur"])
async def get_electricity_data(
    annee : str = Query(default=next_year_str),
    trading_date: str = Query(default=date.today().strftime("%Y-%m-%d")),
    delivery_date: str = Query(default=(date.today() + timedelta(days=1)).strftime("%Y-%m-%d"))
):
    reqUrl = f"https://webservice-eex.gvsi.com/query/json/getDaily/close/offexchtradevolumeeex/onexchtradevolumeeex/tradedatetimegmt/?priceSymbol=%22%2FE.G5BYF{annee}%22&chartstartdate={trading_date}&chartstopdate={delivery_date}&dailybarinterval=Days&aggregatepriceselection=First"

 
    headersList = {
    "Accept": "*/*",
    "Referer": "https://www.eex.com"
    }

    payload = ""

    response = requests.request("GET", reqUrl, data=payload,  headers=headersList)
    data = json.loads(response.text)
    return JSONResponse(content=data)



# News


@app.get("/api/v1/e-market/news" , tags=["Actualités de l'énergie"])
async def get_news(query: str = "energie"):
    headers = {
        'X-RapidAPI-Host': 'free-news.p.rapidapi.com',
        'X-RapidAPI-Key': 'a76be59b22msha21a0b1d33c9faap1a235bjsneb32dc3d1ace',
    }

    url = f"https://free-news.p.rapidapi.com/v1/search?q={query}&lang=fr"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            articles = data.get('articles', [])
            return {"articles": articles}
        else:
            return {"error": "Failed to fetch news data"}