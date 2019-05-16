import xml.etree.ElementTree as xml
import pandas as pd
import glob
import numpy as np

files = glob.glob("../../datasets/Allerhande_1978-2009/**/*.xml", recursive=True)


def parse_article(i):
    doc = xml.parse(i)
    for article in doc.findall(".//{http://www.abbyy.com/FineReader_xml/FineReader10-schema-v1.xml}text"):
        line = []
        quality = []
        article = ''
        for char in doc.findall(".//{http://www.abbyy.com/FineReader_xml/FineReader10-schema-v1.xml}charParams"):
            if char.get("charConfidence") is not None:
                quality.append(int(char.get("charConfidence")))
        avg_quality = np.mean(quality)
        for x in doc.findall(".//{http://www.abbyy.com/FineReader_xml/FineReader10-schema-v1.xml}line"):
            characters = []
            for char in x.findall(".//{http://www.abbyy.com/FineReader_xml/FineReader10-schema-v1.xml}charParams"):
                characters.append(char.text)
                words = ''.join(characters)
                if words.endswith('-'):
                    words = words[:-1]
                else:
                    words = words + ' '
            line.append(words)
        article = ''.join(line)
        article = article[:-1]
        return article


d = []
content = []
avg_quality = []
for file in files[:10]:
    if file.endswith('xml'):
        page_nr = file[-7:-4]
        issue = file[-21:-9]

        ocr_quality, content = parse_article(file)
        d.append({'page_nr': page_nr, 'issue': issue,
                  'avg_quality': ocr_quality, 'content': content})
df = pd.DataFrame(d)
df.to_csv('test.csv')
