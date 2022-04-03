import numpy as np
import pandas as pd
import re


class DataframeNormalizer():

    def __init__(self, dataframe):
        self.dataframe = dataframe

    def string_normalize(self, dataframe):
        self.dataframe = self.dataframe.applymap(lambda s: s.strip() if type(s) == str else s)
        self.dataframe = self.dataframe.applymap(lambda s: s.lower() if type(s) == str else s)
        self.dataframe = self.dataframe.applymap(lambda s: self.accents_normalize(s) if type(s) == str else s)
        self.dataframe = self.dataframe.applymap(lambda s: re.sub(r"\s{2,}", r" ", s) if type(s) == str else s)
        return dataframe

    def accents_normalize(s):
        replacements = (
            ("á", "a"),
            ("é", "e"),
            ("í", "i"),
            ("ó", "o"),
            ("ú", "u"),
        )
        for a, b in replacements:
            s = s.replace(a, b)
        return s

    def rut_normalize(self, input_colname, output_colname):

        self.dataframe[input_colname] = self.dataframe.loc[:, input_colname].str.strip().str.lower()

        self.dataframe[output_colname] = np.where(self.dataframe.loc[:,input_colname].str.contains('-', regex=False)==False, 
                                                    self.dataframe.loc[:,input_colname].str[:-1] + "-" + self.dataframe.loc[:,input_colname].str[-1:], 
                                                    self.dataframe.loc[:,input_colname])

        self.dataframe[output_colname] = np.where(self.dataframe.loc[:,output_colname].str.contains('.', regex=False)==True, 
                                                    self.dataframe.loc[:,output_colname].replace('.', ''), 
                                                    self.dataframe.loc[:,output_colname])
        self.dataframe.drop(input_colname, axis=1, inplace=True)
        return self.dataframe

if __name__ == '__main__':
    pass