# Home Assignment
When invoked, frequent_synonym_groups.py starts listen to Twitter stream, and every 2 seconds prints the top N synonym group that appeared most frequently the last minute (for english words only)

### How to run:
##### input params:
  - -h Shows this help message and exit
  - --synonyms  Number of synonyms
#### Command example:
./frequent_synonym_groups.py --synonyms 3

# python depandencies:
You need to do the following in order to run it:
1. Download the code
2. Install the requirements:


        pip install -r requirements.txt
3. Run nltk.download() and download all nltk data
