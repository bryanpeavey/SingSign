import requests
from bs4 import BeautifulSoup
import spacy
import re

nlp = spacy.load("en_core_web_sm")

artist = "ariana-grande"
song = "true-story"

# composes url with artist and song title
url = "https://genius.com/" + artist + "-" + song + "-lyrics"

# gets html from http request
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

print("Song: " + song + " by " + artist)

# uses beautiful soup to find the div the lyrics are in
lyricDivs = soup.find_all("div", attrs={"data-lyrics-container": "true"})

# if lyrics were found
if lyricDivs:

    # what will eventually be printed
    lyrics = ""

    # for each lyric-data-container
    for lyricDiv in lyricDivs:

        # remove unwanted text
        for unwanted in lyricDiv.find_all(["div"], attrs={"data-exclude-from-selection": "true"}):
            unwanted.decompose()

        # extracts texts from lyrics
        lyrics += lyricDiv.get_text(separator="\n")
        # removes any bracketed text (e.g., "[Chorus]")
        lyrics = re.sub(r"\[.*?\]", "", lyrics)

    # prints the lyrics followed by a line of white space
    print(lyrics + "\n")

    parsed_nouns = []

    # gets each paragraph of the lyrics
    paragraphs = lyrics.split("\n\n")

    # for each paragraph
    for paragraph in paragraphs:
        # split the paragraph into lines
        lines = paragraph.split("\n")

        paragraph_tokens = []

        # for each line in the paragraph
        for line in lines:
            # an empty list for the line tokens
            line_tokens = []
            # uses natural language processing on the line
            doc = nlp(line)

            # for each token processed from the line
            for token in doc:
                #if the token is a noun, adjective, or verb
                if token.pos_ in ["NOUN"]:
                    # add the token to the list
                    line_tokens.append(f"{token.text} - {token.pos_}\t")

            # print each token
            if line_tokens:
                paragraph_tokens.append(" ".join(line_tokens))

        if paragraph_tokens:
            parsed_nouns.append("\n".join(paragraph_tokens))

    #a line of whitespace after each paragraph
    print("\n\n".join(parsed_nouns))

#else if lyrics weren't found
else:
    print("Lyrics not found.")