# MalPipe

                  _   ___ _            
      /\/\   __ _| | / _ (_)_ __   ___ 
     /    \ / _` | |/ /_)/ | '_ \ / _ \
    / /\/\ \ (_| | / ___/| | |_) |  __/
    \/    \/\__,_|_\/    |_| .__/ \___|
                       |_|         


MalPipe is a modular malware (and indicator) collection and processing framework.  It is designed to pull malware, domains, URLs and IP addresses from multiple feeds, enrich the collected data and export the results.

At this time, the following feeds are supported:
* VirusTotal (https://www.virustotal.com)
* MalShare (https://malshare.com/)
* BambenekFeeds (osint.bambenekconsulting.com/feeds/)
* FeodoBlockList (https://feodotracker.abuse.ch)
* Malc0deIPList (http://malc0de.com/)
* NoThinkIPFeeds (www.nothink.org/)
* OpenPhishURLs (https://openphish.com)
* TorNodes (https://torstatus.blutmagie.de)


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.


### Installing

Deployment of MalPipe requires installing the required python libraries and configuring the various modules.

Python dependencies can be installed by running:
```
pip install -r requirements.txt
```

### Configuring

#### Feeds 

An example configuration is provided in `config_example.json` with settings to get started.  This file contains a JSON object containing the required settings for each feed / processor / exporter.  An description of a feeds settings are shown below:

```
...
    "feeds": {
...
        "MalShare": {
            "ENABLED" : true,
            "API_KEY" : "00000000000000000000000000000000000000000000000000000000000",
            "EXPORTERS" :  ["DetailsPrinter", "JSONLog"],
            "PROCESSORS" :  ["YaraScan", "DNSResolver"]
        },

...
```  

As some feeds update daily, feeds can be in two forms: scheduled and active.  Settings for when these should run is defined outside of the configuration in the individual modules.

#### Processors
 
Processors are used to enrich/standardize the collected.  For example, data from `VirusTotal` contains yara results for each file collected, whereas `MalShare` does not.  By adding, `YaraScan` to the `PROCESSORS` key, you can scan the files to also include this data. 

An example modules settings are below: 

```
...
    "processors": {
    ...
        "YaraScan": {
            "ENABLED" : false,
            "RULES_PATH": "/yara_rules/Malware.yara"
        },
        ...
```
Currently, the following processors have been implemented:
* `ASNLookup`
* `DNSResolver`
* `FileType`
* `RDNS`
* `YaraScan`

#### Exporters
 
The final components is exporters, these control where the data goes.  These can be used to export collected data to a malware repository, a SIEM, JSON Log files or printed for the user. 

```
     ...
     "exporters": {
        ...
        "JSONLog": {
            "ENABLED" : true,
            "PRETTY" : true,
            "LOG_PATH": "./temp/"
        },
        ...
```

Currently, the following processors have been implemented:
* `DetailsPrinter`
* `GenericWebStorage`
* `JSONLog`
* `LocalFileStorage`

### Running

After setup, MalPipe can be run by using:
```
python malpipe.py
```



## Developing Modules
Modules for MalPipe located under [malpipe/](malpipe/) by type:
* [Feeds](malpipe/feeds)
* [Processors](malpipe/processors)
* [Exporters](malpipe/exporters)

Creating new modules is easy, 

### Create Python Module

MalPipe modules are defined as Python classes.  Following is an example Module header

```
class ModuleName(Processor):
    def __init__(self):
        md = ProcessorDescription(
            module_name="ModuleName",
            description="Description",
            authors=["Author Name"],
            version="VersionNumber"
        )
        Processor.__init__(self, md)
        self.types = ['ipaddresses']
        self.parse_settings()
 ```

Settings can be set by importing the configuration and set to class variables, shown below:

```
	from malpipe.config import CONFIG
            ...
            self.yara_rule_path = CONFIG['processors'][self.get_module_name()]['RULES_PATH']
```

Each processor is required to have a `run` function that is called by the feed.  

### Add Settings
After creation of the module, settings need to be added to are `config.json` under the `processors`, `feeds` , or `exporters` key. If the new module is a processor or exporter, it will also need to be added to the associated feeds.  An example is shown below:

```
     ...
    "processors": {
     ...    
        "SuperNewModule": {
            "ENABLED" : true,
            "DOCOOLSTUFF": true
        },
     ...
    "feeds": {
        ...
        "0DayMalwareFeed": { 
            "ENABLED" : true,
            "EXPORTERS" :  ["DetailsPrinter", "JSONLog"],
            "PROCESSORS" :  ["SuperNewModule"]
        }
        ...
```




## Contributing

Please report any problems by creating a issue or starting a pull request.  If you have additional modules or features you would like to see, please consider opening an issue.

## Authors

* **Silas Cutler** -  [GitHub](https://github.com/SilasCutler) | [Twitter](https://twitter.com/SilasCutler) | 

See also the list of [contributors](https://github.com/silascutler/malpipe/contributors) who participated in this project.

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Thanks to [bwall](https://github.com/bwall) / [bamfdetect](https://github.com/bwall/bamfdetect) for inspiration on module loading


