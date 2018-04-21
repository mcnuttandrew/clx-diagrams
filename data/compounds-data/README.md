This folder contains data and scripts for the compounds project. Check out the sources.md for more info about the data. Here are some quick summaries of the stuff in the scripts folder:



## naive baysian

The naive baysian script (scripts/naive-byes-compound.py) can be run from root of the folder, and the running the command

```sh
python scripts/naive-bayes-compound.py
```

## bible scraper

Running the bible scraping script (scripts/bible-scraper) has several steps.

```sh
# installation
# from inside of the bible-scraper folder
yarn

# bible-scraper assumes that the folder it lives has siblings with appropriate data
# at the bottom of the bible-scraper.js file is an function execution for the name of that folder
# once all this is configured run
node bible-scraper
```

## modify-german-dict-2

modify-german-dict-2 simply modifies the file from http://www1.ids-mannheim.de/kl/projekte/methoden/derewo.html into a more easily parseable format. kept around for repeated research reasons.