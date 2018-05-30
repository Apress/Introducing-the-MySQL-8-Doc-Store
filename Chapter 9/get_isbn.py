from isbntools import app
import isbnlib
import argparse

parser = argparse.ArgumentParser(description='ISBN Lookup')
parser.add_argument('ISBN')
args = parser.parse_args()

app.config.add_apikey('isbndb', 'VHH8GLVV')
meta_dict = app.meta(args.ISBN)
print meta_dict
if meta_dict:
    print isbnlib.registry.bibformatters['json'](meta_dict)

