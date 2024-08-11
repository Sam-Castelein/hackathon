import cv2
import pytesseract
import os
from dateutil.parser import parse
from dateutil.parser._parser import ParserError
import re


def get_dates(text):
    #potential_dates = re.findall(r'\b[^\s]+\b', text)
    prefix = r'due date'
    all_dates = []

    for match in re.finditer(due_date_pattern, text, re.IGNORECASE):
        substring = text[match.end():]
        potential_dates = re.findall(r'\b\S+\b', substring)
        
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
for date in dates:
    print(date)

while cv2.getWindowProperty("gray", cv2.WND_PROP_VISIBLE) >= 1 or cv2.getWindowProperty("adaptive thresh", cv2.WND_PROP_VISIBLE) >= 1:
    if cv2.waitKey(100) & 0xFF == ord('q'):  
        break


