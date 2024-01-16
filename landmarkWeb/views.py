from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse
from .forms import ImageModelForm

import os
import subprocess


# Create your views here.

def index(request):
    return render(request, "landmarkWeb/home.html")

    
def upload_image(request):
    if request.method == 'POST':
        form = ImageModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("/")
    else:
        form = ImageModelForm()
    return render(request, 'landmarkWeb/upload_image.html', {'form': form})

def yolov7Detect(weights_path, source_path, img_size, conf_thres):
    # YOLOv7 komutunu çalıştırmak için kullanılacak parametreler
    '''weights_path = 'runs\\train\yolov7-landmark\weights\last.pt'
    source_path = 'inference\landmarks\\atakule-deneme1.jpg'
    img_size = 640
    conf_thres = 0.5'''

    #shell'de çalıştılacak komut
    command = f"python detect.py --weights {weights_path} --source {source_path} --img-size {img_size} --conf-thres {conf_thres}"
    
    try:
        #Geçerli dizini alır
        cwd = os.getcwd()

        #Geçerli dizini yolov7 klasörü olarak ayarlar
        yolo_dir = os.path.join(cwd, 'landmarkWeb','static','landmarkWeb', 'yolo', 'yolov7')
        os.chdir(yolo_dir)

        #detect.py scriptini shell'den çalıştırır
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        #tekrardan eski çalışma dizini geçerli dizin olarak ayarlar 
        os.chdir(cwd)

        # Çıktıları kullanma
        stdout = result.stdout.decode('utf-8')
        stderr = result.stderr.decode('utf-8')

        # İsterseniz çıktıları HttpResponse ile gönderebilirsini
        response_text = f"Stdout:\n{stdout}\n"
        return response_text
    except Exception as e:
        return f"Error: {str(e)}\n"
