# test_equipment
Equipment tests.

## Post-MRI Audio-Video
### low-level features (openSMILE)
Comparing low-level features few had poor parity between the four possible combinations of {close, far} × {pop shield on, pop shield off}. Out of thousands of features analyzed, below are boxplots of the features sorted by parity from worst to best. Within each box are all four conditions. The recordings analyzed here were conducted one at a time with the same person performing the same task in the same space.

![Worst parity: PMAV emobase](https://github.com/shnizzedy/SM_openSMILE/blob/master/test_equipment/PMAV/emobase/collected/boxplot.png)

![Worst parity: PMAV ComParE_2016](https://github.com/shnizzedy/SM_openSMILE/blob/master/test_equipment/PMAV/ComParE_2016/collected/boxplot.png)
### transcription (Watson)
The results of transcription were predictable.

|             | close_screen_off_(Watson).json | close_screen_on_(Watson).json | far_screen_off_(Watson).json | far_screen_on_(Watson).json | Key     | 
|--------------------|----------------------------------|---------------------------------|--------------------------------|-------------------------------|-----------| 
|                  | Peter                          | Peter                         | Peter                        | Peter                       | Peter   | 
|                  | Piper                          | Piper                         | Piper                        | Piper                       | Piper   | 
|                  | picked                         | picked                        | picked                       | picked                      | picked  | 
|                  | a                              | a                             | up                           | a                           | a       | 
|                  | Peck                           | Peck                          | but                          | pack                        | peck    | 
|                  | of                             | of                            | first                        | of                          | of      | 
|                  | pickled                        | pickled                       | thinking                     | pickled                     | pickled | 
|                  | peppers                        | peppers                       | about                        | peppers                     | peppers | 
|                  | Peggy                          | Peggy                         | I                            | piggyback                   | Peggy   | 
|                  | Babcock                        | Babcock                       | think                        | because                     | Babcock | 
|                  | piggy                          | Peggy                         | he                           | picking                     | Peggy   | 
|                  | back                           | that                          |                              | out                         | Babcock | 
| hamming distance | 3                              | 2                             | 9                            | 5                           | 0       | 


## Recorder tests
Comparing low-level features, few had poor parity between the Sony recorder and the RØDE → Canon recording set-up. Out of thousands of features analyzed, below are boxplots of the features with the worst parity sorted from worst to best. Within each box are all participants recorded in the given task with the specified recording set-up. The tasks were recorded with both set-ups simultaneously.

### low-level features (openSMILE)

![Worst parity: sentences/emobase](https://raw.githubusercontent.com/shnizzedy/SM_openSMILE/master/test_equipment/recorder_test/sentences/emobase/collected/boxplot.png)

![Worst parity: sentences/ComParE_2016](https://raw.githubusercontent.com/shnizzedy/SM_openSMILE/master/test_equipment/recorder_test/sentences/ComParE_2016/collected/boxplot.png)

![Worst parity: word_list/emobase](https://raw.githubusercontent.com/shnizzedy/SM_openSMILE/master/test_equipment/recorder_test/word_list/emobase/collected/boxplot.png)

![Worst parity: word_list/ComParE_2016](https://raw.githubusercontent.com/shnizzedy/SM_openSMILE/master/test_equipment/recorder_test/word_list/ComParE_2016/collected/boxplot.png)

### transcription (Watson)
The results of transcription showed few differences across participants. These numbers are the hamming distance between transcripts of each of the two recording set-ups of a single recording

| Sentences       | Hamming Distance           |
| ------------- |:-------------:| 
|      | 3 |
|      | 1     | 
|  | 0      | 
|      | 3 |
|      | 6      | 

| Word List        | Hamming Distance           |
| ------------- |:-------------:| 
|      | 0 |
|      | 0      | 
|  | 0      | 
|      | 0 |
|      | 0      | 
|  | 4      | 
|      | 1 |
|      | 4     | 
|  | 1     | 
|  | 1     | 
