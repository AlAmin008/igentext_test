from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import cv2
import pytesseract
from ocrapi.models import PdfFiles,PdfDetails
from authapi.models import User
import fitz
from PIL import Image
import os
from django.conf import settings
from rest_framework.parsers import MultiPartParser
from datetime import datetime
import random
from rest_framework.permissions import IsAuthenticated




#extracting text from image
def text_extraction(image_path):
    img = cv2.imread(image_path)

    # Convert image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #Binarize
    thresh,im_bw=cv2.threshold(gray,200,230,cv2.THRESH_BINARY)

    # Configuration for Bengali language
    custom_config = r'-l eng+ben --psm 6'

    # Perform OCR
    txt = pytesseract.image_to_string(im_bw, config=custom_config)
    
    return txt

def pdf2Image(pdf_file_instance):

    # Open the PDF file
    pdf_document = fitz.open(pdf_file_instance.file_location)
    total_page = 0
    # Loop through each page in the PDF
    for page_number in range(pdf_document.page_count):
        page = pdf_document.load_page(page_number)
        total_page +=1

        # Convert the page to an image
        image = page.get_pixmap(matrix=fitz.Matrix(300 / 72, 300 / 72))

        # Create a Pillow (PIL) image from the PyMuPDF image
        pil_image = Image.frombytes("RGB", [image.width, image.height], image.samples)
        # file = 
        path = pdf_file_instance.file_location.rsplit('/', 1)[0]
        folder_path = os.path.join(settings.BASE_DIR, f"{path}/pdf_Image/")

        # Ensure the folder exists, create it if necessary
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Construct the complete file path with the folder
        image_filename = os.path.join(folder_path, f"page_{page_number+1}.jpg")
        pil_image.save(image_filename)

        #Reducing DPI
        target_DPI = 114
        img = Image.open(image_filename)
        current_dpi = img.info.get("dpi", (72, 72))
        scale_factor = target_DPI / current_dpi[0]
        new_size = tuple(int(dim * scale_factor) for dim in img.size)
        resized_img_dpi = img.resize(new_size)
        # resized_img_dpi.save(name,format="JPEG",dpi=(target_DPI,target_DPI))

        # Reduce BPP
        img_8bit = resized_img_dpi.convert("P", palette=Image.ADAPTIVE, colors=256)
        img_rgb = img_8bit.convert("RGB")
        img_rgb.save(image_filename,format="JPEG", dpi = (target_DPI,target_DPI))

        file_instance = pdf_file_instance

        pdf_details_instance= PdfDetails(
        pdf_file_id_id= pdf_file_instance.id,
        page_number= page_number+1,
        image_location = image_filename,
        text = ""
        )
        pdf_details_instance.save()

    # Close the PDF document
    pdf_document.close()
    pdf_file_instance.total_page = total_page
    pdf_file_instance.save()
    

# def pdf2text(pdf_file_instance):

#     incomplete = False
#     # Open the PDF file
#     pdf_document = fitz.open(pdf_file_instance.file_location)
#     total_page = 0
#     # Loop through each page in the PDF
#     for page_number in range(pdf_document.page_count):
#         page = pdf_document.load_page(page_number)
#         total_page +=1

#         # Convert the page to an image
#         image = page.get_pixmap(matrix=fitz.Matrix(300 / 72, 300 / 72))

#         # Create a Pillow (PIL) image from the PyMuPDF image
#         pil_image = Image.frombytes("RGB", [image.width, image.height], image.samples)
#         # file = 
#         path = pdf_file_instance.file_location.rsplit('\\', 1)[0]
#         folder_path = os.path.join(settings.BASE_DIR, f"{path}\pdf_Image")

#         # Ensure the folder exists, create it if necessary
#         if not os.path.exists(folder_path):
#             os.makedirs(folder_path)

#         # Construct the complete file path with the folder
#         image_filename = os.path.join(folder_path, f"page_{page_number+1}.jpg")
#         pil_image.save(image_filename)

#         #Reducing DPI
#         target_DPI = 114
#         img = Image.open(image_filename)
#         current_dpi = img.info.get("dpi", (72, 72))
#         scale_factor = target_DPI / current_dpi[0]
#         new_size = tuple(int(dim * scale_factor) for dim in img.size)
#         resized_img_dpi = img.resize(new_size)
#         # resized_img_dpi.save(name,format="JPEG",dpi=(target_DPI,target_DPI))

#         # Reduce BPP
#         img_8bit = resized_img_dpi.convert("P", palette=Image.ADAPTIVE, colors=256)
#         img_rgb = img_8bit.convert("RGB")
#         img_rgb.save(image_filename,format="JPEG", dpi = (target_DPI,target_DPI))

        
#         result = text_extraction(image_filename)
       
#         if not result:
#             incomplete = True

#         file_instance = pdf_file_instance

#         pdf_details_instance= PdfDetails(
#         pdf_file_id_id= file_instance.id,
#         page_number= page_number+1,
#         image_location = image_filename,
#         text = result
#         )
#         pdf_details_instance.save()

#     # Close the PDF document
    
#     pdf_document.close()
#     pdf_file_instance.total_page = total_page
#     if incomplete:
#         pdf_file_instance.extraction_status = 'incomplete'
#     else:
#         pdf_file_instance.extraction_status = 'complete'
#     pdf_file_instance.save()
#     return pdf_file_instance.id

def store_file(file_obj,file_name,user_instance,random_number):
    folder = f"{random_number}{file_name}"
    folder_path = os.path.join(settings.BASE_DIR, f"media/{user_instance.name}/{folder}/")
    # Ensure the folder exists, create it if necessary
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    
    file_path = os.path.join(folder_path,f"{random_number}{file_name}")
    with open(file_path, 'wb') as destination_file:
        for chunk in file_obj.chunks():
            destination_file.write(chunk)
    total_size = os.path.getsize(file_path)
    total_size = round (total_size/1024,2)
    # adding file in database 
      
    pdf_file_instance = PdfFiles(
    pdf_file_name= file_name,
    total_page = 0,
    total_size=total_size,
    file_location= file_path,
    uploaded_by=user_instance,
    uploaded_date=datetime.today(),
    uploaded_time = datetime.now().strftime('%H:%M:%S'),
    extraction_status='pending',
    )
    #Save the instance to the database
    pdf_file_instance.save()
    values = [pdf_file_instance.id,pdf_file_instance.file_location]
    return values


# Create your views here.


class UploadFileView(APIView):

    parser_classes = (MultiPartParser,)
    permission_classes=[IsAuthenticated]


    def post(self, request,uid, *args, **kwargs):
        file_obj = request.FILES.get('file')
        if file_obj:
            if file_obj.name.lower().endswith(".pdf"):
                #get file info 
                result = PdfFiles.objects.filter(pdf_file_name = file_obj.name,uploaded_by_id=uid)
                if result:
                    return Response({'error': 'A file with the same name exist',"file_name":file_obj.name}, status=status.HTTP_406_NOT_ACCEPTABLE)
                user_instance = User.objects.get(id=uid)
                random_number = random.randint(100,999)
                values = store_file(file_obj,file_obj.name,user_instance,random_number)
                return Response({'message': 'File successfully Stored','id':values[0],'pdfLocation':values[1]}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Please Provide PDf files only'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'file doesn\'t exist'}, status=status.HTTP_204_NO_CONTENT)
        
class Pdf2ImageView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request,fileid):
        file = PdfFiles.objects.get(id = fileid)
        if file:
            pdf2Image(file)
            return Response({'message': 'Pdf to Image Successful'}, status=status.HTTP_200_OK)
        return Response({'error': 'Pdf to Image UnSuccessful'}, status=status.HTTP_400_BAD_REQUEST)

            
class Image2TextView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request,fileid):
        images = PdfDetails.objects.filter(pdf_file_id=fileid)
        incomplete = False
        if images:
            for image in images:
                extracted_text = text_extraction(image.image_location)
                if not extracted_text:
                    incomplete = True
                image.text=extracted_text
                image.save()
            file = PdfFiles.objects.get(id=fileid)
            if incomplete:
                file.extraction_status="incomplete"
            else:
                file.extraction_status="complete"
            file.save()
            return Response({"message":"Text Extraction Sucessful"},status=status.HTTP_200_OK)
        return Response({'error': 'Pdf to text UnSuccessful'}, status=status.HTTP_400_BAD_REQUEST)


class UploadSimilarNamedFileView(APIView):
    parser_classes = (MultiPartParser,)
    permission_classes=[IsAuthenticated]


    def post(self, request,uid, *args, **kwargs):
        file_obj = request.FILES.get('file')

        if file_obj:
            if file_obj.name.lower().endswith(".pdf"):
                user_instance = User.objects.get(id=uid)
                random_number = random.randint(100,999)
                values = store_file(file_obj,file_obj.name,user_instance,random_number)
                return Response({'message': 'File successfully Stored','id':values[0],'pdfLocation':values[1]}, status=status.HTTP_200_OK)

            else:
                return Response({'error': 'Please Provide PDf files only'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'file doesn\'t exist'}, status=status.HTTP_400_BAD_REQUEST)
