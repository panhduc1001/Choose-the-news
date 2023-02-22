#
#  Choose Your News
#
#  In this assignment you will combine your knowledge of HTMl/CSS
#  mark-up languages with your skills in Python scripting, pattern
#  matching, databases and Graphical User Interface design to produce
#  a useful application that allows the user to compare news stories
#  from multiple sources and save them for later perusal.
#
#  See the client's requirements accompanying this file for full
#  details.
#
# --------------------------------------------------------------------#


# -----Initialisation Steps-------------------------------------------#
#

# Import standard Python 3 modules needed to complete this assignment.
# You should not need to use any modules other than those provided
# in a standard Python 3 installation for your solution.
#
# In particular, you may NOT use any Python modules that need to be
# downloaded and installed separately, such as "Beautiful Soup" or
# "Pillow", because the markers will not have access to such modules
# and will not be able to run your code.  Only modules that are part
# of a standard Python 3 installation may be used.

# A function for exiting the program immediately (renamed
# because "exit" is already a standard Python function).
from sys import exit as abort

# The function for opening a web document given its URL.
# (You WILL need to use this function in your solution,
# either directly or via our "download" function below.)
from urllib.request import urlopen

# Some standard Tkinter functions.  (You WILL need to use
# SOME of these functions in your solution.)  You may also
# import other widgets from the "tkinter" module, provided they
# are standard ones and don't need to be downloaded and installed
# separately.  (NB: DON'T import all of the "tkinter.tkk" functions
# using a "*" wildcard because this module includes alternative
# versions of standard widgets like "Label".)
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Progressbar

# Functions for finding occurrences of a pattern defined
# via a regular expression.  (You do not necessarily need to
# use these functions in your solution, because the problem
# can be solved with the string "find" function, but it will
# be difficult to produce a concise and robust solution
# without using regular expressions.)
from re import *

# A function for displaying a web document in the host
# operating system's default web browser (renamed to
# distinguish it from the built-in "open" function for
# opening local files).  (You WILL need to use this function
# in your solution.)
from webbrowser import open as urldisplay

# All the standard SQLite functions.
from sqlite3 import *

# Confirm that the student has declared their authorship.
# You must NOT change any of the code below.
if not isinstance(student_number, int):
    print("\nUnable to run: No student number supplied", "(must be an integer)\n")
    abort()
if not isinstance(student_name, str):
    print("\nUnable to run: No student name supplied", "(must be a character string)\n")
    abort()

#
# --------------------------------------------------------------------#


# -----Supplied Function----------------------------------------------#
#
# Below is a function you can use in your solution if you find it
# helpful.  (You are not required to use this function, but it may
# save you some effort.)
#


# A function to download and save a web document.  The function
# returns the downloaded document as a character string and
# optionally saves it as a local file.  If the attempted download
# fails, an error message is written to the shell window and the
# special value None is returned.
#
# Parameters:
# * url - The address of the web page you want to download.
# * target_filename - Name of the file to be saved (if any).
# * filename_extension - Extension for the target file, usually
#      "html" for an HTML document or "xhtml" for an XML
#      document.
# * save_file - A file is saved only if this is True. WARNING:
#      The function will silently overwrite the target file
#      if it already exists!
# * char_set - The character set used by the web page, which is
#      usually Unicode UTF-8, although some web pages use other
#      character sets.
# * incognito - If this parameter is True the Python program will
#      try to hide its identity from the web server. This can
#      sometimes be used to prevent the server from blocking access
#      to Python programs. However we do NOT encourage using
#      this option as it is both unreliable and unethical to
#      override the wishes of the web document provider!
#
def download(
    url="http://www.wikipedia.org/",
    target_filename="downloaded_document",
    filename_extension="html",
    save_file=True,
    char_set="UTF-8",
    incognito=False,
):
    # Import the function for opening online documents and
    # the class for creating requests
    from urllib.request import urlopen, Request

    # Import an exception raised when a web server denies access
    # to a document
    from urllib.error import HTTPError

    # Open the web document for reading
    try:
        if incognito:
            # Pretend to be a Windows 10 computer instead of
            # a Python script (NOT RELIABLE OR RECOMMENDED!)
            request = Request(url)
            request.add_header(
                "User-Agent",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                + "AppleWebKit/537.36 (KHTML, like Gecko) "
                + "Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
            )
            print("Warning - Request does not reveal client's true identity.")
            print("          This is both unreliable and unethical!")
            print("          Proceed at your own risk!\n")
        else:
            # Behave ethically
            request = url
        web_page = urlopen(request)
    except ValueError:
        print("Download error - Cannot find document at URL '" + url + "'\n")
        return None
    except HTTPError:
        print("Download error - Access denied to document at URL '" + url + "'\n")
        return None
    except Exception as message:
        print(
            "Download error - Something went wrong when trying to download "
            + "the document at URL '"
            + url
            + "'"
        )
        print("Error message was:", message, "\n")
        return None

    # Read the contents as a character string
    try:
        web_page_contents = web_page.read().decode(char_set)
    except UnicodeDecodeError:
        print(
            "Download error - Unable to decode document from URL '"
            + url
            + "' as '"
            + char_set
            + "' characters\n"
        )
        return None
    except Exception as message:
        print(
            "Download error - Something went wrong when trying to decode "
            + "the document from URL '"
            + url
            + "'"
        )
        print("Error message was:", message, "\n")
        return None

    # Optionally write the contents to a local text file
    # (overwriting the file if it already exists!)
    if save_file:
        try:
            text_file = open(
                target_filename + "." + filename_extension, "w", encoding=char_set
            )
            text_file.write(web_page_contents)
            text_file.close()
        except Exception as message:
            print("Download error - Unable to write to file '" + target_filename + "'")
            print("Error message was:", message, "\n")

    # Return the downloaded document to the caller
    return web_page_contents


#
# --------------------------------------------------------------------#


# -----Student's Solution---------------------------------------------#
#
# Put your solution at the end of this file.
#

# News' URL
url1 = "https://www.brisbanetimes.com.au/breaking-news"
url2 = "https://www.9news.com.au/just-in"
url3 = "https://www.abc.net.au/news/justin/"
url4 = "https://www.smh.com.au/breaking-news"

# Access to URL's source
source_page1 = urlopen(url1)
source_page2 = urlopen(url2)
source_page3 = urlopen(url3)
source_page4 = urlopen(url4)

# Extract contents as a Unicode string
html_code1 = source_page1.read().decode("UTF-8")
html_code2 = source_page2.read().decode("UTF-8")
html_code3 = source_page3.read().decode("UTF-8")
html_code4 = source_page4.read().decode("UTF-8")

# Close
source_page1.close()
source_page2.close()
source_page3.close()
source_page4.close()

# Find the title

# URL1
title1_pattern = '<a data-testid="article-link".*?>(.*?)</a>'
title1_results = search(title1_pattern, html_code1)
title1 = title1_results.group()
title1 = sub("<.+?>", "", title1)
title1 = sub("&#x27;", "'", title1)
print("Title 1 is: ", title1)

content1_pattern = '<p class="_3b7W- _3XEsE" data-pb-type="ab">(.*?)</p>'
content1_results = search(content1_pattern, html_code1)
content1 = content1_results.group()
content1 = sub("<.*?>", " ", content1)
content1 = sub("&#x27;", "'", content1)
print("Content 1 is: ", content1)

time1_pattern = '<time class="_2_zR-".*?>(.*?)</time>'
time1_results = search(time1_pattern, html_code1)
time1 = time1_results.group()
time1 = sub("<.*?>", "", time1)
time1 = sub("&#x27;", "'", time1)
print("Time 1 is: ", time1)

author1_pattern = "<span><span>(.*?)</span></span>"
author1_results = search(author1_pattern, html_code1)
author1 = author1_results.group()
author1 = sub("<.*?>", "", author1)
author1 = sub("&#x27;", "'", author1)
print("Author 1 is: ", author1)

# URL2
title2_pattern = '<span class="story__headline__text">(.*?)</span>'
title2_results = search(title2_pattern, html_code2)
title2 = title2_results.group()
title2 = sub("<.*?>", "", title2)
title2 = sub("&#x27;", "'", title2)
print("Title 2 is: ", title2)

content2_pattern = '<div class="story__abstract">(.*?)</div>'
content2_results = search(content2_pattern, html_code2)
content2 = content2_results.group()
content2 = sub("<.*?>", "", content2)
content2 = sub("&#x27;", "'", content2)
print("Content 2 is: ", content2)

time2_pattern = '<time class="story__time">(.*?)</time>'
time2_results = search(time2_pattern, html_code2)
time2 = time2_results.group()
time2 = sub("<.*?>", "", time2)
time2 = sub("&#x27;", "'", time2)
print("Time 2 is: ", time2)

author2_pattern = '<span class="story__extras"><a href="/(.*?)" class="story__tag">(.*?)</a>(.*?)</span>'
author2_results = search(author2_pattern, html_code2)
author2 = author2_results.group()
author2 = sub('<time class="story__time">(.*?)</time>', "", author2)
author2 = sub("<.*?>", "", author2)
author2 = sub("&#x27;", "'", author2)
print("Author 2 is: ", author2)

# URL3
title3_pattern = '<a class="_3T9Id _2f8qj FQVx7 _2tPjN _1QHxY _3OwCD".*?>(.*?)</a>'
title3_results = search(title3_pattern, html_code3)
title3 = title3_results.group()
title3 = sub("<.*?>", "", title3)
title3 = sub("&#x27;", "'", title3)
print("Title 3 is: ", title3)

content3_pattern = '<div class="_3P1Sq _1deB8 _1hGzz _1-RZJ _1yL-m" data-component="CardDescription">(.*?)</div>'
content3_results = search(content3_pattern, html_code3)
content3 = content3_results.group()
content3 = sub("<.*?>", "", content3)
content3 = sub("&#x27;", "'", content3)
print("Content 3 is: ", content3)

"""
time3_pattern = '<span class="_21KQl">(.*?)</span>'
time3_results = search(time3_pattern, html_code3)
time3 = time3_results.group()
time3 = sub('<abbr aria-hidden="true" class="_2t5cr" title="minutes">(.*?)</abbr>', ' ', time3)
time3 = sub('<.*?>', '', time3)
time3 = sub('&#x27;', "'", time3)
print('Time 3 is: ', time3, 'ago')
"""

time3_pattern = ' datetime="(.*?)" '
time3_results = search(time3_pattern, html_code3)
time3 = time3_results.group()
# time3 = sub('<time class="_21SmZ _3_Aqg _1hGzz _1-RZJ P8HGV" data-component="Timestamp" datetime', ' ', time3)
# time3 = sub('', '', time3)
time3 = sub("&#x27;", "'", time3)
print("Time 3 is: ", time3)

author3_pattern = '<a class="_2f8qj FQVx7 _2tPjN _1QHxY".*?>(.*?)</a>'
author3_results = search(author3_pattern, html_code3)
author3 = author3_results.group()
author3 = sub("<.*?>", "", author3)
author3 = sub("&#x27;", "'", author3)
print("Author 3 is: ", author3)

# URL4
title4_pattern = '<a data-testid="article-link"(.*?)>(.*?)</a>'
title4_results = search(title4_pattern, html_code4)
title4 = title4_results.group()
title4 = sub("<.*?>", "", title4)
title4 = sub("&#x27;", "'", title4)
print("Title 4 is: ", title4)

content4_pattern = '<p class="_3b7W- _3XEsE" data-pb-type="ab">(.*?)</p>'
content4_results = search(content4_pattern, html_code4)
content4 = content4_results.group()
content4 = sub("<.*?>", "", content4)
content4 = sub("&#x27;", "'", content4)
print("Content 4 is: ", content4)

time4_pattern = '<time class="_2_zR-"(.*?)>(.*?)</time>'
time4_results = search(time4_pattern, html_code4)
time4 = time4_results.group()
time4 = sub("<.*?>", "", time4)
time4 = sub("hours", "", time4)
time4 = sub("&#x27;", "'", time4)
print("Time 4 is: ", time4)

author4_pattern = "<span>(.*?)</span>"
author4_results = search(author4_pattern, html_code4)
author4 = author4_results.group()
author4 = sub("<.*?>", "", author4)
author4 = sub("&#x27;", "'", author4)
print("Author 4 is: ", author4)
