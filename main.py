import cv2
import pytesseract
import os
from dateutil.parser import parse
from dateutil import parser
from dateutil.parser._parser import ParserError
import re


def get_dates(text):
    #potential_dates = re.findall(r'\b[^\s]+\b', text)
    prefix = r'due date'
    all_dates = []
    potential_dates = []

    for match in re.finditer(prefix, text, re.IGNORECASE):
        substring = text[match.end():]
        #print("-------" + repr(substring))
        #substring = text[match.group(1)]
        potential_dates = re.findall(r'\b\S+\b', substring)
        #potential_dates = re.findall(r'\b(0?[1-9]|1[0-2])/(0?[1-9]|[12][0-9]|3[01])/\d{1,2}\b', substring)
        #potential_dates = re.findall(r'\b\d{1,2}/\d{1,2}/\d{2,4}\b', substring)
        #potential_dates = parser.parse(str(substring), fuzzy = True)
        print(potential_dates)
        #if potential_date_match:
            #potential_dates.append(potential_date_match.group())
        #potential_dates = substring
        
    for item in potential_dates:
        try:
            parsed_date = parse(item, fuzzy=True)
            all_dates.append(parsed_date)
        except (ValueError, ParserError):
            continue
    return all_dates




tesseract_cmd_path = r'/usr/local/bin/tesseract'
if not os.path.isfile(tesseract_cmd_path):
    raise FileNotFoundError(f"Tesseract executable not found at {tesseract_cmd_path}")
pytesseract.pytesseract.tesseract_cmd = tesseract_cmd_path



img = cv2.imread("bill1.png")
img = cv2.resize(img, None, fx=1.5, fy=1.5)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

adaptive_threshold = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 11)
adaptive_threshold_two = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 85, 11)



text = pytesseract.image_to_string(gray)
print(text)

#cv2.imshow("original", img)
cv2.imshow("gray", gray)
cv2.imshow("adaptive thresh", adaptive_threshold)
cv2.imshow("adaptive thresh 2", adaptive_threshold_two)
#cv2.waitKey(60)


dates = get_dates(text)
print(len(dates))
for date in dates:
    print(date)

while cv2.getWindowProperty("gray", cv2.WND_PROP_VISIBLE) >= 1 or cv2.getWindowProperty("adaptive thresh", cv2.WND_PROP_VISIBLE) >= 1:
    if cv2.waitKey(100) & 0xFF == ord('q'):  
        break


