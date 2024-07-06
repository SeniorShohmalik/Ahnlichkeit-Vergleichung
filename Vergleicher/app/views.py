from django.shortcuts import render
from app.models import Y_ISH
import fitz 
from .tasks import count_widgets
from django.http import HttpResponse

def djacel(request):
    result = count_widgets.delay()
    if result.ready():
        print(result.get())
    return HttpResponse(result.get())

def percent(text1:list,text2:list):
    o = []
    for j in range(len(text1)):
        if text1[j] in text2 and text1[j] not in o:
            o.append(text1[j])

    result = len(o)
    return round(len(text2)/result,2)

def extract_text_from_pdf(pdf_path):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)

    # Initialize an empty string to store text
    text = ""

    # Iterate through each page in the PDF
    for page_number in range(pdf_document.page_count):
        page = pdf_document[page_number]

        text += page.get_text()

    # Close the PDF document
    pdf_document.close()

    return text

def find_text_page(pdf_path, target_text):
    dictionary = {}
    doc = fitz.open(pdf_path)
    for page_number in range(1,doc.page_count+1):
        page = doc[page_number]
        text = page.get_text()
        for t_text in target_text:
            if t_text in text:
                if dictionary.page_number:
                    m = dictionary[page_number]
                    dictionary[page_number] = m + '    |    ' + t_text  
                else :
                    dictionary[page_number] = t_text

    doc.close()
    print(dictionary)
    return dictionary

def index(request):

    nomzodlar = Y_ISH.objects.all()
    content = {'nomzodlar':nomzodlar} 
    return render(request,'app/index.html',content)


def main(request,pk):
    files = {}
    nomzod = Y_ISH.objects.get(id = pk)
    nomzod_ishi = nomzod.pdf_ish.path
    text = extract_text_from_pdf(nomzod_ishi)
    nomzod_ishi_text = text.split()
    uzunlik_nomzod_ishi = len(nomzod_ishi_text)
    ultimate_result = {}
    boshqalar = Y_ISH.objects.exclude(nomzod = nomzod) 
    highlighten = []
    boshqalar_ishi = []
    common_elements = []
    for boshqa in boshqalar:
        boshqaning_ishi = boshqa.pdf_ish.path
        boshqaning_ishi_text = extract_text_from_pdf(boshqaning_ishi)
        boshqaning_ishi_text_split = boshqaning_ishi_text.split()
        if boshqaning_ishi_text == text:
            common_elements = 100
        else:
            common_elements = percent(nomzod_ishi_text,boshqaning_ishi_text_split)
        ultimate_result[boshqa.nomzod]=common_elements
        boshqalar_ishi.append(boshqaning_ishi_text_split)

        files[boshqa.nomzod]=len(boshqaning_ishi_text_split)

    for word_index in range(0,uzunlik_nomzod_ishi,1):
        wanted_word =  nomzod_ishi_text[word_index:word_index+5]
        for boshqa_ishi in boshqalar_ishi:
            for index in range(len(boshqa_ishi)):
                if boshqa_ishi[index:index+5]==wanted_word:
                    wanted_words = ' '.join(wanted_word)
                    highlighten.append(wanted_words)
                    break
                else:
                    continue
    proper = []
    invalid = []
    for item_index in range(len(highlighten)):
        if highlighten[item_index] in proper:
            invalid.append(highlighten[item_index])
        else:
            proper.append(highlighten[item_index])
    
    result = find_text_page(nomzod.pdf_ish.path,proper)
    print(result)
    


    return render(request, 'app/main.html',{'proper':proper,'nomzod_ishi':text,'result':ultimate_result,'nomzod':nomzod,'results':result})



            








        

                    






    







            

















