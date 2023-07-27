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
```
docker run -d --rm -e TICKER_TABLES="TECH=AAPL,MSFT,GOOG,META,ORCL;CHIPS=NVDA,AMD,TSM,MU;AUTO=F,GM,TSLA,NIO,LI;TRAVEL=BKNG,UAL,DAL,AAL,HLT,MAR,ABNB,UBER,LYFT" -p 80:80 fullaxx/stonk_stalker
```

## Run the dashboard with a set refresh value
Default: 2 seconds during trading hours, otherwise 10 seconds
```
docker run -d --rm -e HTMLREFRESH=30 -e TICKER_TABLES="TECH=AAPL,MSFT,GOOG,META,ORCL;CHIPS=NVDA,AMD,TSM,MU;AUTO=F,GM,TSLA,NIO,LI;TRAVEL=BKNG,UAL,DAL,AAL,HLT,MAR,ABNB,UBER,LYFT" -p 80:80 fullaxx/stonk_stalker
docker run -d --rm -e HTMLREFRESH=0 -e TICKER_TABLES="TECH=AAPL,MSFT,GOOG,META,ORCL;CHIPS=NVDA,AMD,TSM,MU;AUTO=F,GM,TSLA,NIO,LI;TRAVEL=BKNG,UAL,DAL,AAL,HLT,MAR,ABNB,UBER,LYFT" -p 80:80 fullaxx/stonk_stalker
```

## Run the dashboard with dark mode enabled
DARK MODE IS NOT FUNCTIONAL YET
```
docker run -d --rm -e DARKMODE=1 -e TICKER_TABLES="TECH=AAPL,MSFT,GOOG,META,ORCL;CHIPS=NVDA,AMD,TSM,MU;AUTO=F,GM,TSLA,NIO,LI;TRAVEL=BKNG,UAL,DAL,AAL,HLT,MAR,ABNB,UBER,LYFT" -p 80:80 fullaxx/stonk_stalker
```
