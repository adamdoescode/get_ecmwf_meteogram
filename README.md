# wrapper script for extracting meteograms quickly from ECMWF

I was just trying to get some meteograms data and ended up building a small thing.

Easy to add your own defaults by creating a constant in the script.

## Usage:

Get latest 10 day forecast for Perth:
```
python get_meteogram.py --location Perth
```

Get latest 10 day forecast for Brockman 4 minesite:
```
python get_meteogram.py --location Brockman
```

Get latest 10 day forecast as png for a given lat and lon:
```
python get_meteogram.py --outputFormat png --lat 11 --lon -11
```


