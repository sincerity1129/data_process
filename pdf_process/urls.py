from django.urls import path
from pdf_process.views import PDFProcess
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('data_process', PDFProcess.as_view(), name='pdf_process'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)