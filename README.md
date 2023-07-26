# Stonk Stalker
A Dashboard to stalk your stocks

## Get the image from Docker Hub or build it locally
```
docker pull fullaxx/stonk_stalker
docker build -t="fullaxx/smtd" github.com/Fullaxx/stonk_stalker
```

## Run the dashboard with your symbol list
```
docker run -d --rm -e TICKER_TABLES="TECH=AAPL,MSFT,GOOG,META,ORCL;CHIPS=NVDA,AMD,TSM,MU;AUTO=F,GM,TSLA,NIO,LI;TRAVEL=BKNG,HLT,MAR,ABNB,UBER,LYFT" -p 80:80 fullaxx/stonk_stalker
```

## Run the dashboard with dark mode enabled
DARK MODE IS NOT FUNCTIONAL YET
```
docker run -d --rm -e DARKMODE=1 -e TICKER_TABLES="TECH=AAPL,MSFT,GOOG,META,ORCL;CHIPS=NVDA,AMD,TSM,MU;AUTO=F,GM,TSLA,NIO,LI;TRAVEL=BKNG,HLT,MAR,ABNB,UBER,LYFT" -p 80:80 fullaxx/stonk_stalker
```
