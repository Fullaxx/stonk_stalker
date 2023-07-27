# Stonk Stalker
A simple dashboard to stalk your stocks, circa 1997

## Example
![Example](Stonk_Stalker.png)

## Get the image from Docker Hub or build it locally
```
docker pull fullaxx/stonk_stalker
docker build -t="fullaxx/stonk_stalker" github.com/Fullaxx/stonk_stalker
```

## Run the dashboard with your symbol list
TICKER_TABLES is the env variable that will control the layout of the tables. \
TICKER_TABLES is a semi-colon delimited list of tables. \
Each table includes a name and a list of symbols. \
4 Tables listed from the example code: \
TECH=AAPL,MSFT,GOOG,META,ORCL \
CHIPS=NVDA,AMD,TSM,MU \
AUTO=F,GM,TSLA,NIO,LI \
TRAVEL=BKNG,HLT,MAR,ABNB,UBER,LYFT
```
docker run -d --rm -e TICKER_TABLES="TECH=AAPL,MSFT,GOOG,META,ORCL;CHIPS=NVDA,AMD,TSM,MU;AUTO=F,GM,TSLA,NIO,LI;TRAVEL=BKNG,HLT,MAR,ABNB,UBER,LYFT" -p 80:80 fullaxx/stonk_stalker
```

## Run the dashboard with a set refresh value
Default: 2 seconds during trading hours, otherwise 10 seconds
```
docker run -d --rm -e HTMLREFRESH=30 -e TICKER_TABLES="TECH=AAPL,MSFT,GOOG,META,ORCL;CHIPS=NVDA,AMD,TSM,MU;AUTO=F,GM,TSLA,NIO,LI;TRAVEL=BKNG,HLT,MAR,ABNB,UBER,LYFT" -p 80:80 fullaxx/stonk_stalker
docker run -d --rm -e HTMLREFRESH=0 -e TICKER_TABLES="TECH=AAPL,MSFT,GOOG,META,ORCL;CHIPS=NVDA,AMD,TSM,MU;AUTO=F,GM,TSLA,NIO,LI;TRAVEL=BKNG,HLT,MAR,ABNB,UBER,LYFT" -p 80:80 fullaxx/stonk_stalker
```

## Run the dashboard with dark mode enabled
DARK MODE IS NOT FUNCTIONAL YET
```
docker run -d --rm -e DARKMODE=1 -e TICKER_TABLES="TECH=AAPL,MSFT,GOOG,META,ORCL;CHIPS=NVDA,AMD,TSM,MU;AUTO=F,GM,TSLA,NIO,LI;TRAVEL=BKNG,HLT,MAR,ABNB,UBER,LYFT" -p 80:80 fullaxx/stonk_stalker
```
