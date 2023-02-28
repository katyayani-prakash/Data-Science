A few tweets appear more than once in the dataset, and it turns out that they have been caught like that in the original file "IRA_handle_tweets.csv". 
On preliminary investigation, I found this was due to different time stamps on the same tweets, with very minor updates in punctuations in the edited tweets. 
My guess is, they were edited by the author and re-published, thus getting picked up multiple times in the dataset.

There are also a couple of issues with our counting approach:

1. The column 'language' isn't a reliable filter, since a lot of English tweets were tagged as 'Language Undefined', leading to incorrect Data Collection.
2. The approach for data annotation is also not correct, by using only white-space and non-alphanumeric characters in front of Trump, we're filtering out Trump's own tweet handle "@realDonaldTrump" and many other legitimate mentions.
