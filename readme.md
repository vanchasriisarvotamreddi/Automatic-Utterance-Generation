
# Title - Automatic Generation of Utterances for Intelligent BOT development using T-5 pre trained model


### Automatic Utterances for Training model
To generate the possible utterances and to convert the data in to yaml format and store in `nlu.yml`, run:
```sh
python dumpyaml.py
```
### Training rasa nlu 

To train the nlu model, simply run:
```sh
rasa train
```
### Testing automation

run the following command to test the trained model and convert in to `.csv`.The responses consist of confidence scores and intent classification.
```sh
python test.py
```

