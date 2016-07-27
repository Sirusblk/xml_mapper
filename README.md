# xml_mapper

A simple Python program that plots points in an ESRI shapefile based on XML file. Currently maps out California Highway Patrol as well as Southern California Edison outages.

## Usage

Requires Python 2 (because of ArcPy). Must have access to ArcPy to create the point shapefile. You can call the appropriate program from the command line. For example, for the California Highway Patrol incidents:
```
python map_chp.py
```

You can extend this usage to a cron job to run on your server fetching and mapping the results in a timely fashion. Each XML file is updated on a different schedule, that's why each has it's own python program so that they can be ran independently according to it's update schedule.


## License

This repository uses the [MIT License](https://github.com/Sirusblk/xml_mapper/blob/master/LICENSE)
