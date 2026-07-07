# Data

- `nyc-rolling-sales-sample.csv` — first 500 rows, committed to the repo for
  quick local testing without needing the full file.
- `nyc-rolling-sales.csv` — the full ~84,500-row dataset used by the pipeline
  and tests. Gitignored due to size (13MB). Fetch it with:

```bash
curl -sL -o data/nyc-rolling-sales.csv \
  "https://raw.githubusercontent.com/karimitani/Real-Estate/master/nyc-rolling-sales.csv"
```

Original source: [NYC Department of Finance – Rolling Sales Data](https://www.nyc.gov/site/finance/property/property-rolling-sales-data.page),
published via [NYC Open Data](https://data.cityofnewyork.us/dataset/NYC-Citywide-Rolling-Calendar-Sales/usep-8jbt).
