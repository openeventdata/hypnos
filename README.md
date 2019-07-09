[![Circle CI](https://circleci.com/gh/caerusassociates/hypnos.svg?style=svg)](https://circleci.com/gh/caerusassociates/hypnos)
[![Code Health](https://landscape.io/github/openeventdata/hypnos/petrarch2/landscape.svg?style=flat)](https://landscape.io/github/openeventdata/hypnos/petrarch2)

hypnos
======

**Note: hypnos now works with PETRARCH2 by default.**

A RESTful API around the [PETRARCH2](https://github.com/openeventdata/petrarch2)
event data coder. Using `docker compose`, this setup also integrates the 
Stanford [CoreNLP](http://nlp.stanford.edu/software/corenlp.shtml) parser
using Casey Hilland's [docker container](https://github.com/chilland/ccNLP).
This setup allows the users to stream texts into the API, rather than the 
batch mode seen in applications such as the [Phoenix pipeline](https://github.com/openeventdata/phoenix_pipeline).

This software was developed by Caerus Associates and donated to the Open Event
Data Alliance.

Running
-------

Running the system is as simple as `cd`ing into the `hypnos` directory and using

`docker-compose up`

or 

`docker-compose up -d`

to run in the background.

This assumes that you have `docker-compose` and `docker` installed.

Example Python Usage
-----

```
import requests
import json 
from pprint import pprint

headers = {'Content-Type': 'application/json'}
data = {'text':"A Tunisian court has jailed a Nigerian student for two years for helping young militants join an armed Islamic group in Lebanon, his lawyer said Wednesday.", 'id': 'abc123', 'date':'20010101'}
data = json.dumps(data)
r = requests.get('http://localhost:5002/hypnos/extract', data=data, headers=headers)
pprint(r.json())
```

Returns:

```
{'abc123': {'meta': {'date': '20010101', 'verbs': []},
            'sents': {'0': {'content': 'A Tunisian court has jailed a Nigerian '
                                       'student for two years for helping '
                                       'young militants join an armed Islamic '
                                       'group in Lebanon , his lawyer said '
                                       'Wednesday .',
                            'events': [['TUNJUD', 'NGAEDU', '173']],
                            'issues': [['STUDENTS', 1],
                                       ['NAMED_TERROR_GROUP', 1]],
                            'meta': {'actorroot': [['', '']],
                                     'actortext': [['Tunisian court',
                                                    'Nigerian student']],
                                     'eventtext': ['has jailed'],
                                     'nouns': [[[' TUNISIAN', ' COURT'],
                                                ['TUNJUD'],
                                                [['TUN', []], ['~']]],
                                               [[' NIGERIAN', ' STUDENT'],
                                                ['NGAEDU'],
                                                [['NGA', []], ['~']]],
                                               [[' ARMED ISLAMIC GROUP'],
                                                ['DZAREB'],
                                                [['DZAREB', []]]],
                                               [[' LEBANON'],
                                                ['LBN'],
                                                [['LBN', []]]],
                                               [[' LAWYER'],
                                                ['~JUD'],
                                                [['~']]]]},
                            'parsed': '(SBAR (S (NP (DT A )  (JJ TUNISIAN )  '
                                      '(NN COURT )  )  (VP (VBZ HAS )  (VP '
                                      '(VBN JAILED )  (NP (DT A )  (JJ '
                                      'NIGERIAN )  (NN STUDENT )  )  (PP (IN '
                                      'FOR )  (NP (CD TWO )  (NNS YEARS )  )  '
                                      ')  (PP (IN FOR )  (S (VP (VBG HELPING '
                                      ')  (NP (JJ YOUNG )  (NNS MILITANTS )  '
                                      ')  )  )  )  )  )  )  (S (VP (VBP JOIN '
                                      ')  (NP (DT AN )  (JJ ARMED )  (JJ '
                                      'ISLAMIC )  (NN GROUP )  )  (PP (IN IN '
                                      ')  (NP (NNP LEBANON )  )  )  )  )  (, , '
                                      ')  (S (NP (PRP$ HIS )  (NN LAWYER )  )  '
                                      '(VP (VBD SAID )  (NP (NNP WEDNESDAY )  '
                                      ')  )  )  (. . )  )  '}}}}
```
