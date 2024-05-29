from django.shortcuts import render
from rest_framework.views import APIView
from django.http import FileResponse
import os

from .controllers.pdf_controller import PDFController
from .forms import FileUploadForm

MEDIA_ROOT = 'media/uploads'


class PDFProcess(APIView):
    def get(self, request):
        return render(request, "index.html")

    def post(self, request):
        edu_pdf_con = PDFController()
        
        form = FileUploadForm(request.POST, request.FILES)
        pdf_file_path = os.path.join(MEDIA_ROOT, form.files['file'].name)

        if form.is_valid():
            if os.path.exists(pdf_file_path):
                os.remove(pdf_file_path)
            form.save()
        else:
            return render(request, 'fail.html', {'form': '파일이 없습니다.'})

        # PDF file 데이터 전처리 구간
        files, pages = edu_pdf_con.pdf_parsing_pages(pdf_file_path)
        txt_path = f"{pdf_file_path.split('.')[0]}.txt"

        if os.path.exists(txt_path):
            os.remove(txt_path)

        page_count = 1
        for page in pages:
            print("현재 페이지: ", page_count)
            page_count += 1
            page_table_list, page_find_table_list, page_info = (
                edu_pdf_con.pdf_parsing_txt_and_table(page)
            )

            if len(page_table_list) > 0:
                try:
                    for idx, (table, table_find) in enumerate(
                        zip(page_table_list, page_find_table_list)
                    ):

                        label_count = edu_pdf_con.pdf_search_label_location_count(table)
                        label_list = edu_pdf_con.pdf_table_label_parsing(label_count, table)

                        if label_count == 0:
                            result = edu_pdf_con.pdf_table_result_label_list(label_list)
                        else:
                            result = edu_pdf_con.pdf_table_result_list(label_count, label_list, table)
                            result = edu_pdf_con.result_cleaning(result)

                        page_info = edu_pdf_con.total_pdf_parsing(
                            result, page_table_list, page_info, table_find.bbox, idx, txt_path
                        )
                except:
                    files.close() 
                    return  render(request, 'fail.html', {'form': f'인쇄 페이지 기준으로 {page_count-1}페이지의 테이블 라벨이 잘못 되었습니다.'})
        
        files.close() 
        return FileResponse(open(txt_path, 'rb'), as_attachment=True, filename=txt_path.split('/')[-1])