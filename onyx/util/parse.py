#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


def extractnumber(text, lang="en-US"):

    """Takes in a string and extracts a number.
    Args:
        text (str): the string to extract a number from
        lang (str): the code for the language text is in
    Returns:
        (str): The number extracted or the original text.
    """

    lang_lower = str(lang).lower()
    if lang_lower.startswith("en"):
        # return extractnumber_en(text, remove_articles)
        return extractnumber_en(text)
    elif lang_lower.startswith("fr"):
        # return extractnumber_en(text, remove_articles)
        return extractnumber_fr(text)

    # TODO: Normalization for other languages
    return text


def extract_datetime(text, anchorDate=None, lang="en-US"):

    """
    Parsing function that extracts date and time information
    from sentences. Parses many of the common ways that humans
    express dates and times. Includes relative dates like "5 days from today".
    Vague terminology are given arbitrary values, like:
        - morning = 8 AM
        - afternoon = 3 PM
        - evening = 7 PM
    If a time isn't supplied, the function defaults to 12 AM
    Args:
        str (string): the text to be normalized
        anchortDate (:obj:`datetime`, optional): the date to be used for
            relative dating (for example, what does "tomorrow" mean?).
            Defaults to the current date
            (acquired with datetime.datetime.now())
        lang (string): the language of the sentence(s)
    Returns:
        [:obj:`datetime`, :obj:`str`]: 'datetime' is the extracted date
            as a datetime object. Times are represented in 24 hour notation.
            'leftover_string' is the original phrase with all date and time
            related keywords stripped out. See examples for further
            clarification
            Returns 'None' if no date was extracted.
    Examples:
        >>> extract_datetime(
        ... "What is the weather like the day after tomorrow?",
        ... datetime(2017, 06, 30, 00, 00)
        ... )
        [datetime.datetime(2017, 7, 2, 0, 0), 'what is weather like']
        >>> extract_datetime(
        ... "Set up an appointment 2 weeks from Sunday at 5 pm",
        ... datetime(2016, 02, 19, 00, 00)
        ... )
        [datetime.datetime(2016, 3, 6, 17, 0), 'set up appointment']
    """

    lang_lower = str(lang).lower()

    if lang_lower.startswith("en"):
        return extract_datetime_en(text, anchorDate)
    elif lang_lower.startswith("fr"):
        return extract_datetime_fr(text, anchorDate)

    return text


def is_numeric(input_str):
    """
    Takes in a string and tests to see if it is a number.
    Args:
        text (str): string to test if a number
    Returns:
        (bool): True if a number, else False
    """

    try:
        float(input_str)
        return True
    except ValueError:
        return False


def extractnumber_en(text):
    """
    This function prepares the given text for parsing by making
    numbers consistent, getting rid of contractions, etc.
    Args:
        text (str): the string to normalize
    Returns:
        (int) or (float): The value of extracted number
    """
    aWords = text.split()
    aWords = [word for word in aWords if word not in ["the", "a", "an"]]
    andPass = False
    valPreAnd = False
    val = False
    count = 0
    while count < len(aWords):
        word = aWords[count]
        if is_numeric(word):
            # if word.isdigit():            # doesn't work with decimals
            val = float(word)
        elif word == "first":
            val = 1
        elif word == "second":
            val = 2
        elif isFractional(word):
            val = isFractional(word)
        else:
            if word == "one":
                val = 1
            elif word == "two":
                val = 2
            elif word == "three":
                val = 3
            elif word == "four":
                val = 4
            elif word == "five":
                val = 5
            elif word == "six":
                val = 6
            elif word == "seven":
                val = 7
            elif word == "eight":
                val = 8
            elif word == "nine":
                val = 9
            elif word == "ten":
                val = 10
            if val:
                if count < (len(aWords) - 1):
                    wordNext = aWords[count+1]
                else:
                    wordNext = ""
                valNext = isFractional(wordNext)

                if valNext:
                    val = val * valNext
                    aWords[count+1] = ""

        # if val == False:
        if not val:
            # look for fractions like "2/3"
            aPieces = word.split('/')
            # if (len(aPieces) == 2 and is_numeric(aPieces[0])
            #   and is_numeric(aPieces[1])):
            if look_for_fractions(aPieces):
                val = float(aPieces[0]) / float(aPieces[1])
            elif andPass:
                # added to value, quit here
                val = valPreAnd
                break
            else:
                count += 1
                continue

        aWords[count] = ""

        if (andPass):
            aWords[count-1] = ''     # remove "and"
            val += valPreAnd
        elif count+1 < len(aWords) and aWords[count+1] == 'and':
            andPass = True
            valPreAnd = val
            val = False
            count += 2
            continue
        elif count+2 < len(aWords) and aWords[count+2] == 'and':
            andPass = True
            valPreAnd = val
            val = False
            count += 3
            continue

        break

    # if val == False:
    if not val:
        return False

    # Return the $str with the number related words removed
    # (now empty strings, so strlen == 0)
    aWords = [word for word in aWords if len(word) > 0]
    text = ' '.join(aWords)

    return val


def extract_datetime_en(str, currentDate=None):

    def clean_string(str):
        # cleans the input string of unneeded punctuation and capitalization
        # among other things
        str = str.lower().replace('?', '').replace('.', '').replace(',', '')\
            .replace(' the ', ' ').replace(' a ', ' ').replace(' an ', ' ')
        wordList = str.split()
        for idx, word in enumerate(wordList):
            word = word.replace("'s", "")

            ordinals = ["rd", "st", "nd", "th"]
            if word[0].isdigit():
                for ord in ordinals:
                    if ord in word:
                        word = word.replace(ord, "")
            wordList[idx] = word

        return wordList

    def date_found():
        return found or \
            (
                datestr != "" or timeStr != "" or
                yearOffset != 0 or monthOffset != 0 or
                dayOffset is True or hrOffset != 0 or
                hrAbs != 0 or minOffset != 0 or
                minAbs != 0 or secOffset != 0
            )

    if str == "":
        return None
    if currentDate is None:
        currentDate = datetime.now()

    found = False
    daySpecified = False
    dayOffset = False
    monthOffset = 0
    yearOffset = 0
    dateNow = currentDate
    today = dateNow.strftime("%w")
    currentYear = dateNow.strftime("%Y")
    fromFlag = False
    datestr = ""
    hasYear = False
    timeQualifier = ""

    timeQualifiersList = ['morning', 'afternoon', 'evening']
    markers = ['at', 'in', 'on', 'by', 'this', 'around', 'for', 'of']
    days = ['monday', 'tuesday', 'wednesday',
            'thursday', 'friday', 'saturday', 'sunday']
    months = ['january', 'february', 'march', 'april', 'may', 'june',
              'july', 'august', 'september', 'october', 'november', 'december']
    monthsShort = ['jan', 'feb', 'mar', 'apr', 'may', 'june', 'july', 'aug',
                   'sept', 'oct', 'nov', 'dec']

    words = clean_string(str)

    for idx, word in enumerate(words):
        if word == "":
            continue
        wordPrevPrev = words[idx-2] if idx > 1 else ""
        wordPrev = words[idx-1] if idx > 0 else ""
        wordNext = words[idx+1] if idx+1 < len(words) else ""
        wordNextNext = words[idx+2] if idx+2 < len(words) else ""

        # this isn't in clean string because I don't want to save back to words
        word = word.rstrip('s')
        start = idx
        used = 0
        # save timequalifier for later
        if word in timeQualifiersList:
            timeQualifier = word
            # parse today, tomorrow, day after tomorrow
        elif word == "today" and not fromFlag:
            dayOffset = 0
            used += 1
        elif word == "tomorrow" and not fromFlag:
            dayOffset = 1
            used += 1
        elif (word == "day" and
                wordNext == "after" and
                wordNextNext == "tomorrow" and
                not fromFlag and
                not wordPrev[0].isdigit()):
            dayOffset = 2
            used = 3
            if wordPrev == "the":
                start -= 1
                used += 1
            # parse 5 days, 10 weeks, last week, next week
        elif word == "day":
            if wordPrev[0].isdigit():
                dayOffset += int(wordPrev)
                start -= 1
                used = 2
        elif word == "week" and not fromFlag:
            if wordPrev[0].isdigit():
                dayOffset += int(wordPrev) * 7
                start -= 1
                used = 2
            elif wordPrev == "next":
                dayOffset = 7
                start -= 1
                used = 2
            elif wordPrev == "last":
                dayOffset = -7
                start -= 1
                used = 2
            # parse 10 months, next month, last month
        elif word == "month" and not fromFlag:
            if wordPrev[0].isdigit():
                monthOffset = int(wordPrev)
                start -= 1
                used = 2
            elif wordPrev == "next":
                monthOffset = 1
                start -= 1
                used = 2
            elif wordPrev == "last":
                monthOffset = -1
                start -= 1
                used = 2
            # parse 5 years, next year, last year
        elif word == "year" and not fromFlag:
            if wordPrev[0].isdigit():
                yearOffset = int(wordPrev)
                start -= 1
                used = 2
            elif wordPrev == "next":
                yearOffset = 1
                start -= 1
                used = 2
            elif wordPrev == "last":
                yearOffset = -1
                start -= 1
                used = 2
            # parse Monday, Tuesday, etc., and next Monday,
            # last Tuesday, etc.
        elif word in days and not fromFlag:
            d = days.index(word)
            dayOffset = (d+1)-int(today)
            used = 1
            if dayOffset < 0:
                dayOffset += 7
            if wordPrev == "next":
                dayOffset += 7
                used += 1
                start -= 1
            elif wordPrev == "last":
                dayOffset -= 7
                used += 1
                start -= 1
            # parse 15 of July, June 20th, Feb 18, 19 of February
        elif word in months or word in monthsShort and not fromFlag:
            try:
                m = months.index(word)
            except ValueError:
                m = monthsShort.index(word)
            used += 1
            datestr = months[m]
            if wordPrev[0].isdigit() or \
                    (wordPrev == "of" and wordPrevPrev[0].isdigit()):
                if wordPrev == "of" and wordPrevPrev[0].isdigit():
                    datestr += " " + words[idx-2]
                    used += 1
                    start -= 1
                else:
                    datestr += " " + wordPrev
                start -= 1
                used += 1
                if wordNext and wordNext[0].isdigit():
                    datestr += " " + wordNext
                    used += 1
                    hasYear = True
                else:
                    hasYear = False

            elif wordNext and wordNext[0].isdigit():
                datestr += " " + wordNext
                used += 1
                if wordNextNext and wordNextNext[0].isdigit():
                    datestr += " " + wordNextNext
                    used += 1
                    hasYear = True
                else:
                    hasYear = False
        # parse 5 days from tomorrow, 10 weeks from next thursday,
        # 2 months from July
        validFollowups = days + months + monthsShort
        validFollowups.append("today")
        validFollowups.append("tomorrow")
        validFollowups.append("next")
        validFollowups.append("last")
        validFollowups.append("now")
        if (word == "from" or word == "after") and wordNext in validFollowups:
            used = 2
            fromFlag = True
            if wordNext == "tomorrow":
                dayOffset += 1
            elif wordNext in days:
                d = days.index(wordNext)
                tmpOffset = (d+1)-int(today)
                used = 2
                if tmpOffset < 0:
                    tmpOffset += 7
                dayOffset += tmpOffset
            elif wordNextNext and wordNextNext in days:
                d = days.index(wordNextNext)
                tmpOffset = (d+1)-int(today)
                used = 3
                if wordNext == "next":
                    tmpOffset += 7
                    used += 1
                    start -= 1
                elif wordNext == "last":
                    tmpOffset -= 7
                    used += 1
                    start -= 1
                dayOffset += tmpOffset
        if used > 0:
            if start-1 > 0 and words[start-1] == "this":
                start -= 1
                used += 1

            for i in range(0, used):
                words[i+start] = ""

            if (start-1 >= 0 and words[start-1] in markers):
                words[start-1] = ""
            found = True
            daySpecified = True

    # parse time
    timeStr = ""
    hrOffset = 0
    minOffset = 0
    secOffset = 0
    hrAbs = 0
    minAbs = 0
    military = False

    for idx, word in enumerate(words):
        if word == "":
            continue

        wordPrevPrev = words[idx-2] if idx > 1 else ""
        wordPrev = words[idx-1] if idx > 0 else ""
        wordNext = words[idx+1] if idx+1 < len(words) else ""
        wordNextNext = words[idx+2] if idx+2 < len(words) else ""
        # parse noon, midnight, morning, afternoon, evening
        used = 0
        if word == "noon":
            hrAbs = 12
            used += 1
        elif word == "midnight":
            hrAbs = 0
            used += 1
        elif word == "morning":
            if hrAbs == 0:
                hrAbs = 8
            used += 1
        elif word == "afternoon":
            if hrAbs == 0:
                hrAbs = 15
            used += 1
        elif word == "evening":
            if hrAbs == 0:
                hrAbs = 19
            used += 1
            # parse half an hour, quarter hour
        elif word == "hour" and \
                (wordPrev in markers or wordPrevPrev in markers):
            if wordPrev == "half":
                minOffset = 30
            elif wordPrev == "quarter":
                minOffset = 15
            elif wordPrevPrev == "quarter":
                minOffset = 15
                if idx > 2 and words[idx-3] in markers:
                    words[idx-3] = ""
                words[idx-2] = ""
            else:
                hrOffset = 1
            if wordPrevPrev in markers:
                words[idx-2] = ""
            words[idx-1] = ""
            used += 1
            hrAbs = -1
            minAbs = -1
            # parse 5:00 am, 12:00 p.m., etc
        elif word[0].isdigit():
            isTime = True
            strHH = ""
            strMM = ""
            remainder = ""
            if ':' in word:
                # parse colons
                # "3:00 in the morning"
                stage = 0
                length = len(word)
                for i in range(length):
                    if stage == 0:
                        if word[i].isdigit():
                            strHH += word[i]
                        elif word[i] == ":":
                            stage = 1
                        else:
                            stage = 2
                            i -= 1
                    elif stage == 1:
                        if word[i].isdigit():
                            strMM += word[i]
                        else:
                            stage = 2
                            i -= 1
                    elif stage == 2:
                        remainder = word[i:].replace(".", "")
                        break
                if remainder == "":
                    nextWord = wordNext.replace(".", "")
                    if nextWord == "am" or nextWord == "pm":
                        remainder = nextWord
                        used += 1
                    elif wordNext == "in" and wordNextNext == "the" and \
                            words[idx+3] == "morning":
                        reaminder = "am"
                        used += 3
                    elif wordNext == "in" and wordNextNext == "the" and \
                            words[idx+3] == "afternoon":
                        remainder = "pm"
                        used += 3
                    elif wordNext == "in" and wordNextNext == "the" and \
                            words[idx+3] == "evening":
                        remainder = "pm"
                        used += 3
                    elif wordNext == "in" and wordNextNext == "morning":
                        remainder = "am"
                        used += 2
                    elif wordNext == "in" and wordNextNext == "afternoon":
                        remainder = "pm"
                        used += 2
                    elif wordNext == "in" and wordNextNext == "evening":
                        remainder = "pm"
                        used += 2
                    elif wordNext == "this" and wordNextNext == "morning":
                        remainder = "am"
                        used = 2
                    elif wordNext == "this" and wordNextNext == "afternoon":
                        remainder = "pm"
                        used = 2
                    elif wordNext == "this" and wordNextNext == "evening":
                        remainder = "pm"
                        used = 2
                    elif wordNext == "at" and wordNextNext == "night":
                        if strHH > 5:
                            remainder = "pm"
                        else:
                            remainder = "am"
                        used += 2
                    else:
                        if timeQualifier != "":
                            military = True
                            if strHH <= 12 and \
                                    (timeQualifier == "evening" or
                                        timeQualifier == "afternoon"):
                                strHH += 12
            else:
                # try to parse # s without colons
                # 5 hours, 10 minutes etc.
                length = len(word)
                strNum = ""
                remainder = ""
                for i in range(length):
                    if word[i].isdigit():
                        strNum += word[i]
                    else:
                        remainder += word[i]

                if remainder == "":
                    remainder = wordNext.replace(".", "").lstrip().rstrip()

                if (
                        remainder == "pm" or
                        wordNext == "pm" or
                        remainder == "p.m." or
                        wordNext == "p.m."):
                    strHH = strNum
                    remainder = "pm"
                    used = 1
                elif(
                        remainder == "am" or
                        wordNext == "am" or
                        remainder == "a.m." or
                        wordNext == "a.m."):
                    strHH = strNum
                    remainder = "am"
                    used = 1
                else:
                    if wordNext == "pm" or wordNext == "p.m.":
                        strHH = strNum
                        reaminder = "pm"
                        used = 1
                    elif wordNext == "am" or wordNext == "a.m.":
                        strHH = strNum
                        remainder = "am"
                        used = 1
                    elif(
                            int(word) > 100 and
                            (
                                wordPrev == "o" or
                                wordPrev == "oh"
                            )):
                        # 0800 hours (pronounced oh-eight-hundred)
                        strHH = int(word)/100
                        strMM = int(word) - strHH*100
                        military = True
                        if wordNext == "hours":
                            used += 1
                    elif(
                            wordNext == "hours" and
                            word[0] != '0' and
                            (
                                int(word) < 100 and
                                int(word) > 2400
                            )):
                        # ignores military time
                        # "in 3 hours"
                        hrOffset = int(word)
                        used = 2
                        isTime = False
                        hrAbs = -1
                        minAbs = -1

                    elif wordNext == "minutes":
                        # "in 10 minutes"
                        minOffset = int(word)
                        used = 2
                        isTime = False
                        hrAbs = -1
                        minAbs = -1
                    elif wordNext == "seconds":
                        # in 5 seconds
                        secOffset = int(word)
                        used = 2
                        isTime = False
                        hrAbs = -1
                        minAbs = -1
                    elif int(word) > 100:
                        strHH = int(word)/100
                        strMM = int(word) - strHH*100
                        military = True
                        if wordNext == "hours":
                            used += 1
                    elif wordNext[0].isdigit():
                        strHH = word
                        strMM = wordNext
                        military = True
                        used += 1
                        if wordNextNext == "hours":
                            used += 1
                    elif(
                            wordNext == "" or wordNext == "o'clock" or
                            (
                                wordNext == "in" and
                                (
                                    wordNextNext == "the" or
                                    wordNextNext == timeQualifier
                                )
                            )):
                        strHH = word
                        strMM = 00
                        if wordNext == "o'clock":
                            used += 1
                        if wordNext == "in" or wordNextNext == "in":
                            used += (1 if wordNext == "in" else 2)
                            if (
                                    wordNextNext and
                                    wordNextNext in timeQualifier or
                                    (words[words.index(wordNextNext)+1] and
                                    words[words.index(wordNextNext)+1] in timeQualifier)  # noqa
                                ):
                                if (
                                        wordNextNext == "afternoon" or
                                        (len(words) > words.index(wordNextNext) + 1 and  # noqa
                                        words[words.index(wordNextNext)+1] == "afternoon")  # noqa
                                    ):
                                    remainder = "pm"
                                if (
                                        wordNextNext == "evening" or
                                        (len(words) > (words.index(wordNextNext) + 1) and  # noqa
                                        words[words.index(wordNextNext)+1] == "evening")  # noqa
                                    ):
                                    remainder = "pm"
                                if (
                                        wordNextNext == "morning" or
                                        (len(words) > words.index(wordNextNext) + 1 and  # noqa
                                        words[words.index(wordNextNext)+1] == "morning")  # noqa
                                    ):
                                    remainder = "am"
                        if timeQualifier != "":
                            military = True
                    else:
                        isTime = False

            strHH = int(strHH) if strHH else 0
            strMM = int(strMM) if strMM else 0
            strHH = strHH+12 if remainder == "pm" and strHH < 12 else strHH
            strHH = strHH-12 if remainder == "am" and strHH >= 12 else strHH
            if strHH > 24 or strMM > 59:
                isTime = False
                used = 0
            if isTime:
                hrAbs = strHH * 1
                minAbs = strMM * 1
                used += 1
        if used > 0:
            # removed parsed words from the sentence
            for i in range(used):
                words[idx + i] = ""

            if wordPrev == "o" or wordPrev == "oh":
                words[words.index(wordPrev)] = ""

            if wordPrev == "early":
                hrOffset = -1
                words[idx-1] = ""
                idx -= 1
            elif wordPrev == "late":
                hrOffset = 1
                words[idx-1] = ""
                idx -= 1
            if idx > 0 and wordPrev in markers:
                words[idx-1] = ""
            if idx > 1 and wordPrevPrev in markers:
                words[idx-2] = ""

            idx += used-1
            found = True

    # check that we found a date
    if not date_found:
        return None

    if dayOffset is False:
        dayOffset = 0

    # perform date manipulation

    extractedDate = dateNow
    extractedDate = extractedDate.replace(microsecond=0,
                                          second=0,
                                          minute=0,
                                          hour=0)
    if datestr != "":
        temp = datetime.strptime(datestr, "%B %d")
        if not hasYear:
            temp = temp.replace(year=extractedDate.year)
            if extractedDate < temp:
                extractedDate = extractedDate.replace(year=int(currentYear),
                                                      month=int(temp.strftime("%m")),  # noqa
                                                      day=int(temp.strftime("%d")))  # noqa
            else:
                extractedDate = extractedDate.replace(year=int(currentYear)+1,
                                                      month=int(temp.strftime("%m")),  # noqa
                                                      day=int(temp.strftime("%d")))  # noqa
        else:
            extractedDate = extractedDate.replace(year=int(temp.strftime("%Y")),  # noqa
                                                 month=int(temp.strftime("%m")),  # noqa
                                                 day=int(temp.strftime("%d")))

    if timeStr != "":
        temp = datetime(timeStr)
        extractedDate = extractedDate.replace(hour=temp.strftime("%H"),
                                              minute=temp.strftime("%M"),
                                              second=temp.strftime("%S"))

    if yearOffset != 0:
        extractedDate = extractedDate + relativedelta(years=yearOffset)
    if monthOffset != 0:
        extractedDate = extractedDate + relativedelta(months=monthOffset)
    if dayOffset != 0:
        extractedDate = extractedDate + relativedelta(days=dayOffset)
    if hrAbs != -1 and minAbs != -1:

        extractedDate = extractedDate + relativedelta(hours=hrAbs,
                                                      minutes=minAbs)
        if (hrAbs != 0 or minAbs != 0) and datestr == "":
            if not daySpecified and dateNow > extractedDate:
                extractedDate = extractedDate + relativedelta(days=1)
    if hrOffset != 0:
        extractedDate = extractedDate + relativedelta(hours=hrOffset)
    if minOffset != 0:
        extractedDate = extractedDate + relativedelta(minutes=minOffset)
    if secOffset != 0:
        extractedDate = extractedDate + relativedelta(seconds=secOffset)
    for idx, word in enumerate(words):
        if words[idx] == "and" and words[idx-1] == "" and words[idx+1] == "":
            words[idx] = ""

    resultStr = " ".join(words)
    resultStr = ' '.join(resultStr.split())
    return [extractedDate, resultStr]

def extractnumber_fr(text):
    """
    This function prepares the given text for parsing by making
    numbers consistent, getting rid of contractions, etc.
    Args:
        text (str): the string to normalize
    Returns:
        (int) or (float): The value of extracted number
    """
    aWords = text.split()
    aWords = [word for word in aWords if word not in ["le"]]
    andPass = False
    valPreAnd = False
    val = False
    count = 0
    while count < len(aWords):
        word = aWords[count]
        if is_numeric(word):
            # if word.isdigit():            # doesn't work with decimals
            val = float(word)
        elif word == "premier":
            val = 1
        elif word == "second":
            val = 2
        elif isFractional(word):
            val = isFractional(word)
        else:
            if word == "une":
                val = 1
            elif word == "un":
                val = 1
            elif word == "deux":
                val = 2
            elif word == "trois":
                val = 3
            elif word == "quatre":
                val = 4
            elif word == "cinq":
                val = 5
            elif word == "six":
                val = 6
            elif word == "sept":
                val = 7
            elif word == "huit":
                val = 8
            elif word == "neuf":
                val = 9
            elif word == "dix":
                val = 10
            if val:
                if count < (len(aWords) - 1):
                    wordNext = aWords[count+1]
                else:
                    wordNext = ""
                valNext = isFractional(wordNext)

                if valNext:
                    val = val * valNext
                    aWords[count+1] = ""

        # if val == False:
        if not val:
            # look for fractions like "2/3"
            aPieces = word.split('/')
            # if (len(aPieces) == 2 and is_numeric(aPieces[0])
            #   and is_numeric(aPieces[1])):
            if look_for_fractions(aPieces):
                val = float(aPieces[0]) / float(aPieces[1])
            elif andPass:
                # added to value, quit here
                val = valPreAnd
                break
            else:
                count += 1
                continue

        aWords[count] = ""

        if (andPass):
            aWords[count-1] = ''     # remove "and"
            val += valPreAnd
        elif count+1 < len(aWords) and aWords[count+1] == 'and':
            andPass = True
            valPreAnd = val
            val = False
            count += 2
            continue
        elif count+2 < len(aWords) and aWords[count+2] == 'and':
            andPass = True
            valPreAnd = val
            val = False
            count += 3
            continue

        break

    # if val == False:
    if not val:
        return False

    # Return the $str with the number related words removed
    # (now empty strings, so strlen == 0)
    aWords = [word for word in aWords if len(word) > 0]
    text = ' '.join(aWords)

    return val


def extract_datetime_fr(str, currentDate=None):

    def clean_string(str):
        # cleans the input string of unneeded punctuation and capitalization
        # among other things
        str = str.lower().replace('?', '').replace('.', '').replace(',', '')\
            .replace(' the ', ' ').replace(' a ', ' ').replace(' an ', ' ')
        wordList = str.split()
        for idx, word in enumerate(wordList):
            word = word.replace("'s", "")

            ordinals = ["rd", "st", "nd", "th"]
            if word[0].isdigit():
                for ord in ordinals:
                    if ord in word:
                        word = word.replace(ord, "")
            wordList[idx] = word

        return wordList

    def date_found():
        return found or \
            (
                datestr != "" or timeStr != "" or
                yearOffset != 0 or monthOffset != 0 or
                dayOffset is True or hrOffset != 0 or
                hrAbs != 0 or minOffset != 0 or
                minAbs != 0 or secOffset != 0
            )

    if str == "":
        return None
    if currentDate is None:
        currentDate = datetime.now()

    found = False
    daySpecified = False
    dayOffset = False
    monthOffset = 0
    yearOffset = 0
    dateNow = currentDate
    today = dateNow.strftime("%w")
    currentYear = dateNow.strftime("%Y")
    fromFlag = False
    datestr = ""
    hasYear = False
    timeQualifier = ""

    timeQualifiersList = ['morning', 'afternoon', 'evening']
    markers = ['at', 'in', 'on', 'by', 'this', 'around', 'for', 'of']
    days = ['monday', 'tuesday', 'wednesday',
            'thursday', 'friday', 'saturday', 'sunday']
    months = ['january', 'february', 'march', 'april', 'may', 'june',
              'july', 'august', 'september', 'october', 'november', 'december']
    monthsShort = ['jan', 'feb', 'mar', 'apr', 'may', 'june', 'july', 'aug',
                   'sept', 'oct', 'nov', 'dec']

    words = clean_string(str)

    for idx, word in enumerate(words):
        if word == "":
            continue
        wordPrevPrev = words[idx-2] if idx > 1 else ""
        wordPrev = words[idx-1] if idx > 0 else ""
        wordNext = words[idx+1] if idx+1 < len(words) else ""
        wordNextNext = words[idx+2] if idx+2 < len(words) else ""

        # this isn't in clean string because I don't want to save back to words
        word = word.rstrip('s')
        start = idx
        used = 0
        # save timequalifier for later
        if word in timeQualifiersList:
            timeQualifier = word
            # parse today, tomorrow, day after tomorrow
        elif word == "today" and not fromFlag:
            dayOffset = 0
            used += 1
        elif word == "tomorrow" and not fromFlag:
            dayOffset = 1
            used += 1
        elif (word == "day" and
                wordNext == "after" and
                wordNextNext == "tomorrow" and
                not fromFlag and
                not wordPrev[0].isdigit()):
            dayOffset = 2
            used = 3
            if wordPrev == "the":
                start -= 1
                used += 1
            # parse 5 days, 10 weeks, last week, next week
        elif word == "day":
            if wordPrev[0].isdigit():
                dayOffset += int(wordPrev)
                start -= 1
                used = 2
        elif word == "week" and not fromFlag:
            if wordPrev[0].isdigit():
                dayOffset += int(wordPrev) * 7
                start -= 1
                used = 2
            elif wordPrev == "next":
                dayOffset = 7
                start -= 1
                used = 2
            elif wordPrev == "last":
                dayOffset = -7
                start -= 1
                used = 2
            # parse 10 months, next month, last month
        elif word == "month" and not fromFlag:
            if wordPrev[0].isdigit():
                monthOffset = int(wordPrev)
                start -= 1
                used = 2
            elif wordPrev == "next":
                monthOffset = 1
                start -= 1
                used = 2
            elif wordPrev == "last":
                monthOffset = -1
                start -= 1
                used = 2
            # parse 5 years, next year, last year
        elif word == "year" and not fromFlag:
            if wordPrev[0].isdigit():
                yearOffset = int(wordPrev)
                start -= 1
                used = 2
            elif wordPrev == "next":
                yearOffset = 1
                start -= 1
                used = 2
            elif wordPrev == "last":
                yearOffset = -1
                start -= 1
                used = 2
            # parse Monday, Tuesday, etc., and next Monday,
            # last Tuesday, etc.
        elif word in days and not fromFlag:
            d = days.index(word)
            dayOffset = (d+1)-int(today)
            used = 1
            if dayOffset < 0:
                dayOffset += 7
            if wordPrev == "next":
                dayOffset += 7
                used += 1
                start -= 1
            elif wordPrev == "last":
                dayOffset -= 7
                used += 1
                start -= 1
            # parse 15 of July, June 20th, Feb 18, 19 of February
        elif word in months or word in monthsShort and not fromFlag:
            try:
                m = months.index(word)
            except ValueError:
                m = monthsShort.index(word)
            used += 1
            datestr = months[m]
            if wordPrev[0].isdigit() or \
                    (wordPrev == "of" and wordPrevPrev[0].isdigit()):
                if wordPrev == "of" and wordPrevPrev[0].isdigit():
                    datestr += " " + words[idx-2]
                    used += 1
                    start -= 1
                else:
                    datestr += " " + wordPrev
                start -= 1
                used += 1
                if wordNext and wordNext[0].isdigit():
                    datestr += " " + wordNext
                    used += 1
                    hasYear = True
                else:
                    hasYear = False

            elif wordNext and wordNext[0].isdigit():
                datestr += " " + wordNext
                used += 1
                if wordNextNext and wordNextNext[0].isdigit():
                    datestr += " " + wordNextNext
                    used += 1
                    hasYear = True
                else:
                    hasYear = False
        # parse 5 days from tomorrow, 10 weeks from next thursday,
        # 2 months from July
        validFollowups = days + months + monthsShort
        validFollowups.append("today")
        validFollowups.append("tomorrow")
        validFollowups.append("next")
        validFollowups.append("last")
        validFollowups.append("now")
        if (word == "from" or word == "after") and wordNext in validFollowups:
            used = 2
            fromFlag = True
            if wordNext == "tomorrow":
                dayOffset += 1
            elif wordNext in days:
                d = days.index(wordNext)
                tmpOffset = (d+1)-int(today)
                used = 2
                if tmpOffset < 0:
                    tmpOffset += 7
                dayOffset += tmpOffset
            elif wordNextNext and wordNextNext in days:
                d = days.index(wordNextNext)
                tmpOffset = (d+1)-int(today)
                used = 3
                if wordNext == "next":
                    tmpOffset += 7
                    used += 1
                    start -= 1
                elif wordNext == "last":
                    tmpOffset -= 7
                    used += 1
                    start -= 1
                dayOffset += tmpOffset
        if used > 0:
            if start-1 > 0 and words[start-1] == "this":
                start -= 1
                used += 1

            for i in range(0, used):
                words[i+start] = ""

            if (start-1 >= 0 and words[start-1] in markers):
                words[start-1] = ""
            found = True
            daySpecified = True

    # parse time
    timeStr = ""
    hrOffset = 0
    minOffset = 0
    secOffset = 0
    hrAbs = 0
    minAbs = 0
    military = False

    for idx, word in enumerate(words):
        if word == "":
            continue

        wordPrevPrev = words[idx-2] if idx > 1 else ""
        wordPrev = words[idx-1] if idx > 0 else ""
        wordNext = words[idx+1] if idx+1 < len(words) else ""
        wordNextNext = words[idx+2] if idx+2 < len(words) else ""
        # parse noon, midnight, morning, afternoon, evening
        used = 0
        if word == "noon":
            hrAbs = 12
            used += 1
        elif word == "midnight":
            hrAbs = 0
            used += 1
        elif word == "morning":
            if hrAbs == 0:
                hrAbs = 8
            used += 1
        elif word == "afternoon":
            if hrAbs == 0:
                hrAbs = 15
            used += 1
        elif word == "evening":
            if hrAbs == 0:
                hrAbs = 19
            used += 1
            # parse half an hour, quarter hour
        elif word == "hour" and \
                (wordPrev in markers or wordPrevPrev in markers):
            if wordPrev == "half":
                minOffset = 30
            elif wordPrev == "quarter":
                minOffset = 15
            elif wordPrevPrev == "quarter":
                minOffset = 15
                if idx > 2 and words[idx-3] in markers:
                    words[idx-3] = ""
                words[idx-2] = ""
            else:
                hrOffset = 1
            if wordPrevPrev in markers:
                words[idx-2] = ""
            words[idx-1] = ""
            used += 1
            hrAbs = -1
            minAbs = -1
            # parse 5:00 am, 12:00 p.m., etc
        elif word[0].isdigit():
            isTime = True
            strHH = ""
            strMM = ""
            remainder = ""
            if ':' in word:
                # parse colons
                # "3:00 in the morning"
                stage = 0
                length = len(word)
                for i in range(length):
                    if stage == 0:
                        if word[i].isdigit():
                            strHH += word[i]
                        elif word[i] == ":":
                            stage = 1
                        else:
                            stage = 2
                            i -= 1
                    elif stage == 1:
                        if word[i].isdigit():
                            strMM += word[i]
                        else:
                            stage = 2
                            i -= 1
                    elif stage == 2:
                        remainder = word[i:].replace(".", "")
                        break
                if remainder == "":
                    nextWord = wordNext.replace(".", "")
                    if nextWord == "am" or nextWord == "pm":
                        remainder = nextWord
                        used += 1
                    elif wordNext == "in" and wordNextNext == "the" and \
                            words[idx+3] == "morning":
                        reaminder = "am"
                        used += 3
                    elif wordNext == "in" and wordNextNext == "the" and \
                            words[idx+3] == "afternoon":
                        remainder = "pm"
                        used += 3
                    elif wordNext == "in" and wordNextNext == "the" and \
                            words[idx+3] == "evening":
                        remainder = "pm"
                        used += 3
                    elif wordNext == "in" and wordNextNext == "morning":
                        remainder = "am"
                        used += 2
                    elif wordNext == "in" and wordNextNext == "afternoon":
                        remainder = "pm"
                        used += 2
                    elif wordNext == "in" and wordNextNext == "evening":
                        remainder = "pm"
                        used += 2
                    elif wordNext == "this" and wordNextNext == "morning":
                        remainder = "am"
                        used = 2
                    elif wordNext == "this" and wordNextNext == "afternoon":
                        remainder = "pm"
                        used = 2
                    elif wordNext == "this" and wordNextNext == "evening":
                        remainder = "pm"
                        used = 2
                    elif wordNext == "at" and wordNextNext == "night":
                        if strHH > 5:
                            remainder = "pm"
                        else:
                            remainder = "am"
                        used += 2
                    else:
                        if timeQualifier != "":
                            military = True
                            if strHH <= 12 and \
                                    (timeQualifier == "evening" or
                                        timeQualifier == "afternoon"):
                                strHH += 12
            else:
                # try to parse # s without colons
                # 5 hours, 10 minutes etc.
                length = len(word)
                strNum = ""
                remainder = ""
                for i in range(length):
                    if word[i].isdigit():
                        strNum += word[i]
                    else:
                        remainder += word[i]

                if remainder == "":
                    remainder = wordNext.replace(".", "").lstrip().rstrip()

                if (
                        remainder == "pm" or
                        wordNext == "pm" or
                        remainder == "p.m." or
                        wordNext == "p.m."):
                    strHH = strNum
                    remainder = "pm"
                    used = 1
                elif(
                        remainder == "am" or
                        wordNext == "am" or
                        remainder == "a.m." or
                        wordNext == "a.m."):
                    strHH = strNum
                    remainder = "am"
                    used = 1
                else:
                    if wordNext == "pm" or wordNext == "p.m.":
                        strHH = strNum
                        reaminder = "pm"
                        used = 1
                    elif wordNext == "am" or wordNext == "a.m.":
                        strHH = strNum
                        remainder = "am"
                        used = 1
                    elif(
                            int(word) > 100 and
                            (
                                wordPrev == "o" or
                                wordPrev == "oh"
                            )):
                        # 0800 hours (pronounced oh-eight-hundred)
                        strHH = int(word)/100
                        strMM = int(word) - strHH*100
                        military = True
                        if wordNext == "hours":
                            used += 1
                    elif(
                            wordNext == "hours" and
                            word[0] != '0' and
                            (
                                int(word) < 100 and
                                int(word) > 2400
                            )):
                        # ignores military time
                        # "in 3 hours"
                        hrOffset = int(word)
                        used = 2
                        isTime = False
                        hrAbs = -1
                        minAbs = -1

                    elif wordNext == "minutes":
                        # "in 10 minutes"
                        minOffset = int(word)
                        used = 2
                        isTime = False
                        hrAbs = -1
                        minAbs = -1
                    elif wordNext == "seconds":
                        # in 5 seconds
                        secOffset = int(word)
                        used = 2
                        isTime = False
                        hrAbs = -1
                        minAbs = -1
                    elif int(word) > 100:
                        strHH = int(word)/100
                        strMM = int(word) - strHH*100
                        military = True
                        if wordNext == "hours":
                            used += 1
                    elif wordNext[0].isdigit():
                        strHH = word
                        strMM = wordNext
                        military = True
                        used += 1
                        if wordNextNext == "hours":
                            used += 1
                    elif(
                            wordNext == "" or wordNext == "o'clock" or
                            (
                                wordNext == "in" and
                                (
                                    wordNextNext == "the" or
                                    wordNextNext == timeQualifier
                                )
                            )):
                        strHH = word
                        strMM = 00
                        if wordNext == "o'clock":
                            used += 1
                        if wordNext == "in" or wordNextNext == "in":
                            used += (1 if wordNext == "in" else 2)
                            if (
                                    wordNextNext and
                                    wordNextNext in timeQualifier or
                                    (words[words.index(wordNextNext)+1] and
                                    words[words.index(wordNextNext)+1] in timeQualifier)  # noqa
                                ):
                                if (
                                        wordNextNext == "afternoon" or
                                        (len(words) > words.index(wordNextNext) + 1 and  # noqa
                                        words[words.index(wordNextNext)+1] == "afternoon")  # noqa
                                    ):
                                    remainder = "pm"
                                if (
                                        wordNextNext == "evening" or
                                        (len(words) > (words.index(wordNextNext) + 1) and  # noqa
                                        words[words.index(wordNextNext)+1] == "evening")  # noqa
                                    ):
                                    remainder = "pm"
                                if (
                                        wordNextNext == "morning" or
                                        (len(words) > words.index(wordNextNext) + 1 and  # noqa
                                        words[words.index(wordNextNext)+1] == "morning")  # noqa
                                    ):
                                    remainder = "am"
                        if timeQualifier != "":
                            military = True
                    else:
                        isTime = False

            strHH = int(strHH) if strHH else 0
            strMM = int(strMM) if strMM else 0
            strHH = strHH+12 if remainder == "pm" and strHH < 12 else strHH
            strHH = strHH-12 if remainder == "am" and strHH >= 12 else strHH
            if strHH > 24 or strMM > 59:
                isTime = False
                used = 0
            if isTime:
                hrAbs = strHH * 1
                minAbs = strMM * 1
                used += 1
        if used > 0:
            # removed parsed words from the sentence
            for i in range(used):
                words[idx + i] = ""

            if wordPrev == "o" or wordPrev == "oh":
                words[words.index(wordPrev)] = ""

            if wordPrev == "early":
                hrOffset = -1
                words[idx-1] = ""
                idx -= 1
            elif wordPrev == "late":
                hrOffset = 1
                words[idx-1] = ""
                idx -= 1
            if idx > 0 and wordPrev in markers:
                words[idx-1] = ""
            if idx > 1 and wordPrevPrev in markers:
                words[idx-2] = ""

            idx += used-1
            found = True

    # check that we found a date
    if not date_found:
        return None

    if dayOffset is False:
        dayOffset = 0

    # perform date manipulation

    extractedDate = dateNow
    extractedDate = extractedDate.replace(microsecond=0,
                                          second=0,
                                          minute=0,
                                          hour=0)
    if datestr != "":
        temp = datetime.strptime(datestr, "%B %d")
        if not hasYear:
            temp = temp.replace(year=extractedDate.year)
            if extractedDate < temp:
                extractedDate = extractedDate.replace(year=int(currentYear),
                                                      month=int(temp.strftime("%m")),  # noqa
                                                      day=int(temp.strftime("%d")))  # noqa
            else:
                extractedDate = extractedDate.replace(year=int(currentYear)+1,
                                                      month=int(temp.strftime("%m")),  # noqa
                                                      day=int(temp.strftime("%d")))  # noqa
        else:
            extractedDate = extractedDate.replace(year=int(temp.strftime("%Y")),  # noqa
                                                 month=int(temp.strftime("%m")),  # noqa
                                                 day=int(temp.strftime("%d")))

    if timeStr != "":
        temp = datetime(timeStr)
        extractedDate = extractedDate.replace(hour=temp.strftime("%H"),
                                              minute=temp.strftime("%M"),
                                              second=temp.strftime("%S"))

    if yearOffset != 0:
        extractedDate = extractedDate + relativedelta(years=yearOffset)
    if monthOffset != 0:
        extractedDate = extractedDate + relativedelta(months=monthOffset)
    if dayOffset != 0:
        extractedDate = extractedDate + relativedelta(days=dayOffset)
    if hrAbs != -1 and minAbs != -1:

        extractedDate = extractedDate + relativedelta(hours=hrAbs,
                                                      minutes=minAbs)
        if (hrAbs != 0 or minAbs != 0) and datestr == "":
            if not daySpecified and dateNow > extractedDate:
                extractedDate = extractedDate + relativedelta(days=1)
    if hrOffset != 0:
        extractedDate = extractedDate + relativedelta(hours=hrOffset)
    if minOffset != 0:
        extractedDate = extractedDate + relativedelta(minutes=minOffset)
    if secOffset != 0:
        extractedDate = extractedDate + relativedelta(seconds=secOffset)
    for idx, word in enumerate(words):
        if words[idx] == "and" and words[idx-1] == "" and words[idx+1] == "":
            words[idx] = ""

    resultStr = " ".join(words)
    resultStr = ' '.join(resultStr.split())
    return [extractedDate, resultStr]

def look_for_fractions(split_list):
    """"
    This function takes a list made by fraction & determines if a fraction.
    Args:
        split_list (list): list created by splitting on '/'
    Returns:
        (bool): False if not a fraction, otherwise True
    """

    if len(split_list) == 2:
        if is_numeric(split_list[0]) and is_numeric(split_list[1]):
            return True

    return False


def isFractional(input_str):
    """
    This function takes the given text and checks if it is a fraction.
    Args:
        text (str): the string to check if fractional
    Returns:
        (bool) or (float): False if not a fraction, otherwise the fraction
    """
    if input_str.endswith('s', -1):
        input_str = input_str[:len(input_str)-1]		# e.g. "fifths"

    aFrac = ["whole", "half", "third", "fourth", "fifth", "sixth",
             "seventh", "eighth", "ninth", "tenth", "eleventh", "twelfth"]

    if input_str.lower() in aFrac:
        return 1.0/(aFrac.index(input_str)+1)
    if input_str == "quarter":
        return 1.0/4

    return False


def normalize(text, lang="fr-FR", remove_articles=True):
    """Prepare a string for parsing

    This function prepares the given text for parsing by making
    numbers consistent, getting rid of contractions, etc.
    Args:
        text (str): the string to normalize
        lang (str): the code for the language text is in
        remove_articles (bool): whether to remove articles (like 'a', or 'the')
    Returns:
        (str): The normalized string.
    """

    lang_lower = str(lang).lower()
    if lang_lower.startswith("en"):
        return normalize_en(text, remove_articles)
    elif lang_lower.startswith("fr"):
        return normalize_fr(text, remove_articles)

    # TODO: Normalization for other languages
    return text


def normalize_en(text, remove_articles):
    """ English string normalization """

    words = text.split()  # this also removed extra spaces
    normalized = ""
    for word in words:
        if remove_articles and word in ["the", "a", "an"]:
            continue

        # Expand common contractions, e.g. "isn't" -> "is not"
        contraction = ["ain't", "aren't", "can't", "could've", "couldn't",
                       "didn't", "doesn't", "don't", "gonna", "gotta",
                       "hadn't", "hasn't", "haven't", "he'd", "he'll", "he's",
                       "how'd", "how'll", "how's", "I'd", "I'll", "I'm",
                       "I've", "isn't", "it'd", "it'll", "it's", "mightn't",
                       "might've", "mustn't", "must've", "needn't", "oughtn't",
                       "shan't", "she'd", "she'll", "she's", "shouldn't",
                       "should've", "somebody's", "someone'd", "someone'll",
                       "someone's", "that'll", "that's", "that'd", "there'd",
                       "there're", "there's", "they'd", "they'll", "they're",
                       "they've", "wasn't", "we'd", "we'll", "we're", "we've",
                       "weren't", "what'd", "what'll", "what're", "what's",
                       "whats",  # technically incorrect but some STT does this
                       "what've", "when's", "when'd", "where'd", "where's",
                       "where've", "who'd", "who'd've", "who'll", "who're",
                       "who's", "who've", "why'd", "why're", "why's", "won't",
                       "won't've", "would've", "wouldn't", "wouldn't've",
                       "y'all", "ya'll", "you'd", "you'd've", "you'll",
                       "y'aint", "y'ain't", "you're", "you've"]
        if word in contraction:
            expansion = ["is not", "are not", "can not", "could have",
                         "could not", "did not", "does not", "do not",
                         "going to", "got to", "had not", "has not",
                         "have not", "he would", "he will", "he is", "how did",
                         "how will", "how is", "I would", "I will", "I am",
                         "I have", "is not", "it would", "it will", "it is",
                         "might not", "might have", "must not", "must have",
                         "need not", "ought not", "shall not", "she would",
                         "she will", "she is", "should not", "should have",
                         "somebody is", "someone would", "someone will",
                         "someone is", "that will", "that is", "that would",
                         "there would", "there are", "there is", "they would",
                         "they will", "they are", "they have", "was not",
                         "we would", "we will", "we are", "we have",
                         "were not", "what did", "what will", "what are",
                         "what is",
                         "what is", "what have", "when is", "when did",
                         "where did", "where is", "where have", "who would",
                         "who would have", "who will", "who are", "who is",
                         "who have", "why did", "why are", "why is",
                         "will not", "will not have", "would have",
                         "would not", "would not have", "you all", "you all",
                         "you would", "you would have", "you will",
                         "you are not", "you are not", "you are", "you have"]
            word = expansion[contraction.index(word)]

        # Convert numbers into digits, e.g. "two" -> "2"
        textNumbers = ["zero", "one", "two", "three", "four", "five", "six",
                       "seven", "eight", "nine", "ten", "eleven", "twelve",
                       "thirteen", "fourteen", "fifteen", "sixteen",
                       "seventeen", "eighteen", "nineteen", "twenty"]
        if word in textNumbers:
            word = str(textNumbers.index(word))

        normalized += " " + word

    return normalized[1:]  # strip the initial space


def normalize_en(text, remove_articles):
    """ English string normalization """

    words = text.split()  # this also removed extra spaces
    normalized = ""
    for word in words:
        if remove_articles and word in ["the", "a", "an"]:
            continue

        # Expand common contractions, e.g. "isn't" -> "is not"
        contraction = ["ain't", "aren't", "can't", "could've", "couldn't",
                       "didn't", "doesn't", "don't", "gonna", "gotta",
                       "hadn't", "hasn't", "haven't", "he'd", "he'll", "he's",
                       "how'd", "how'll", "how's", "I'd", "I'll", "I'm",
                       "I've", "isn't", "it'd", "it'll", "it's", "mightn't",
                       "might've", "mustn't", "must've", "needn't", "oughtn't",
                       "shan't", "she'd", "she'll", "she's", "shouldn't",
                       "should've", "somebody's", "someone'd", "someone'll",
                       "someone's", "that'll", "that's", "that'd", "there'd",
                       "there're", "there's", "they'd", "they'll", "they're",
                       "they've", "wasn't", "we'd", "we'll", "we're", "we've",
                       "weren't", "what'd", "what'll", "what're", "what's",
                       "whats",  # technically incorrect but some STT does this
                       "what've", "when's", "when'd", "where'd", "where's",
                       "where've", "who'd", "who'd've", "who'll", "who're",
                       "who's", "who've", "why'd", "why're", "why's", "won't",
                       "won't've", "would've", "wouldn't", "wouldn't've",
                       "y'all", "ya'll", "you'd", "you'd've", "you'll",
                       "y'aint", "y'ain't", "you're", "you've"]
        if word in contraction:
            expansion = ["is not", "are not", "can not", "could have",
                         "could not", "did not", "does not", "do not",
                         "going to", "got to", "had not", "has not",
                         "have not", "he would", "he will", "he is", "how did",
                         "how will", "how is", "I would", "I will", "I am",
                         "I have", "is not", "it would", "it will", "it is",
                         "might not", "might have", "must not", "must have",
                         "need not", "ought not", "shall not", "she would",
                         "she will", "she is", "should not", "should have",
                         "somebody is", "someone would", "someone will",
                         "someone is", "that will", "that is", "that would",
                         "there would", "there are", "there is", "they would",
                         "they will", "they are", "they have", "was not",
                         "we would", "we will", "we are", "we have",
                         "were not", "what did", "what will", "what are",
                         "what is",
                         "what is", "what have", "when is", "when did",
                         "where did", "where is", "where have", "who would",
                         "who would have", "who will", "who are", "who is",
                         "who have", "why did", "why are", "why is",
                         "will not", "will not have", "would have",
                         "would not", "would not have", "you all", "you all",
                         "you would", "you would have", "you will",
                         "you are not", "you are not", "you are", "you have"]
            word = expansion[contraction.index(word)]

        # Convert numbers into digits, e.g. "two" -> "2"
        textNumbers = ["zero", "un", "deux", "three", "four", "five", "six",
                       "seven", "eight", "nine", "ten", "eleven", "twelve",
                       "thirteen", "fourteen", "fifteen", "sixteen",
                       "seventeen", "eighteen", "nineteen", "twenty"]
        if word in textNumbers:
            word = str(textNumbers.index(word))

        normalized += " " + word

    return normalized[1:]  # strip the initial space
