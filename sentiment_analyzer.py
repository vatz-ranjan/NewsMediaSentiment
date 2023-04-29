from string import punctuation
from pandas import DataFrame, read_csv
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from textblob import TextBlob


class SentimentAnalyzer:
    __masterDataset = DataFrame()
    __positiveWords = []
    __negativeWords = []

    def __init__(self):
        self.__text = None
        self.__cleanWords = []
        self.__scores = {
            'PositiveScore': 0,
            'NegativeScore': 0,
            'PolarityScore': 0,
            'SubjectivityScore': 0
        }

    @staticmethod
    def define_master_dictionary(master_dictionary):
        SentimentAnalyzer.__masterDataset = read_csv(master_dictionary, header=0)
        SentimentAnalyzer.__positiveWords = [word for word in SentimentAnalyzer.__masterDataset[SentimentAnalyzer.__masterDataset['Positive'] != 0][
                                            'Word']]
        SentimentAnalyzer.__negativeWords = [word for word in SentimentAnalyzer.__masterDataset[SentimentAnalyzer.__masterDataset['Negative'] != 0][
                                            'Word']]

    def __extract_text(self, file_loc):
        try:
            file = open(file_loc, 'r')
            self.__text = file.read()
        except:
            file = open(file_loc, 'rb')
            self.__text = file.read().decode('utf-8')
        file.close()

    def __cal_tokens(self):
        wordTokens = word_tokenize(self.__text)
        stopWords = set(stopwords.words('english'))
        wordsWithoutPunctuations = [word for word in wordTokens if not (word in punctuation)]
        self.__cleanWords = [word for word in wordsWithoutPunctuations if not (word.lower() in stopWords)]

    def __sentiment_analysis(self):
        positiveScore = 0
        negativeScore = 0

        for word in self.__cleanWords:
            word = word.upper()
            if word in self.__positiveWords:
                positiveScore += 1
            if word in self.__negativeWords:
                negativeScore += 1
        
        textblob = TextBlob(self.__text)
        sentiment = textblob.sentiment

        self.__scores['PositiveScore'] = positiveScore
        self.__scores['NegativeScore'] = negativeScore
        self.__scores['PolarityScore'] = sentiment.polarity
        self.__scores['SubjectivityScore'] = sentiment.subjectivity

    def analyze(self, file_loc):
        self.__extract_text(file_loc)
        if len(self.__text) > 1:
            self.__cal_tokens()
            self.__sentiment_analysis()
        return self.__scores

