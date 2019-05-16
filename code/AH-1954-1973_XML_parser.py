import os
import csv
import xml.etree.ElementTree as ET


def extractFolder(dataset_name, path):
    """Find all files and folders in this directory.
    Extract all the files, and recursively go through the subfolders.
    """
    files = [f for f in sorted(os.listdir(path)) if os.path.isfile(os.path.join(path, f))]
    directories = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

    for file in files:
        if file[-4:].lower() == ".xml":
            date = path.split("/")[3]
            extractFile(dataset_name, os.path.join(path, file), date)

    # Recursively combine the subfolders.
    for directory in directories:
        extractFolder(dataset_name, os.path.join(path, directory))


def extractFile(dataset_name, path, date):
    """Read the XML file and extract the <text> element.
    The result will be stored in a newly created folder structure in text files
    containing only the text of the file in the folder YY under the folder MM
    as i.txt
    where i is the index of the article of that day (in case of multiple articles).
    """
    tree = ET.parse(path)
    root = tree.getroot()

    year = date[-4:]
    month = date[0:2]

    if not year or not date:
        return

    content = []
    for block in root[0]:

        for text in [x for x in block if x.tag.split('}')[-1] == 'text']:
            article = ""
            for par in text:
                for line in [x for x in par if x.text]:         
                    article += '\n' + line.text.strip()
            content.append(article)

    directory = os.path.join('{}_processed'.format(dataset_name), year, month)

    # Create the new directories for the processed data.
    if not os.path.exists(directory):
        os.makedirs(directory)

    i = 1
    newPath = os.path.join(directory, "{}.txt".format(year + '-' + month + '_' + str(i)))

    while os.path.isfile(newPath):
        i += 1
        newPath = os.path.join(directory, "{}.txt".format(year + '-' + month + '_' + str(i)))

    #with open(newPath, 'w+', encoding='utf-8') as f:
    #    f.write(content)
    with open(newPath, 'w+') as f:
        wr = csv.writer(f)
        wr.writerows([row] for row in content)


def main():
    dataset_name = "allerhande"
    # Scrape all the XML files in the following folder and its subfolders.
    path = "./allerhande_xml"
    extractFolder(dataset_name, path)
    print("All XML files in {0} extracted to {0}_processed".format(path))


if __name__ == "__main__":
    main()

