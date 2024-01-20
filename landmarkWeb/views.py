from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse
from .forms import ImageModelForm
from .models import landmarkModel

import os
import subprocess
import re

# Create your views here.

def index(request):
    return render(request, "landmarkWeb/home.html")

def detection(request):
    uploaded_image = None

    if request.method == 'POST':
        form = ImageModelForm(request.POST, request.FILES)
        if form.is_valid():
            _image = form.save()
            uploaded_image = _image.get_image_url()
            return render(request, "landmarkWeb/detection.html", {'uploaded_image': uploaded_image})
    else:
        form = ImageModelForm()

    return render(request, 'landmarkWeb/detection.html', {'form': form})
    
def detected(request):
    weights = 'runs/train/yolov7-landmark/weights/best.pt'
    img_size = 640
    conf_thres = 0.5
    if request.method == 'GET':
        img_name = request.GET.get('img_name')
        base_path = "/static/landmarkWeb/images/media/user_uploaded_images/"
        if img_name.startswith(base_path):

            img_name = img_name[len(base_path):]
            source_path = os.path.join(settings.BASE_DIR, 'landmarkWeb', 'static', 'landmarkWeb','images','media','user_uploaded_images',img_name)
           
            result = yolov7Detect2(weights, source_path, img_size, conf_thres)
            result = result['output_lines'][15]

            pattern_str = r"1 ([a-zA-Z-]+)"
            pattern = re.compile(pattern_str)
            match = pattern.search(result)

            if match:
                text = match.group(1)

                def ankaraKalesi():
                    record_by_title = landmarkModel.objects.get(title = "Ankara Kalesi")
                    return record_by_title
                def atakule():
                    record_by_title = landmarkModel.objects.get(title = "Atakule")
                    return record_by_title
                
                switch_dict = {
                'ankara-kalesi': ankaraKalesi,
                'atakule': atakule,
                }
                
                record = switch_dict.get(text)() 

                return render(request, 'landmarkWeb/detected.html', {'record': record})
            else:
                return HttpResponse("Eşleşme bulunamadı")
                
        else:
            print("base path hatalı")
         
    else:
        return HttpResponse("Invalid request method.")
    
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


def yolov7Detect2(weights_path, source_path, img_size, conf_thres):
    try:
        # Geçerli dizini alır
        cwd = os.getcwd()

        # Geçerli dizini yolov7 klasörü olarak ayarlar
        yolo_dir = os.path.join(cwd, 'landmarkWeb', 'static', 'landmarkWeb', 'yolo', 'yolov7')
        os.chdir(yolo_dir)

        # detect.py scriptini shell'den çalıştırır
        command = f"python detect.py --weights {weights_path} --source {source_path} --img-size {img_size} --conf-thres {conf_thres}"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)

        # Çıktıları saklamak için bir dizi oluştur
        output_lines = []
        i = 0
        while True:
            output_stdout = process.stdout.readline()
            output_stderr = process.stderr.readline()

            if not output_stdout and not output_stderr and process.poll() is not None:
                break

            if output_stdout:
                output_lines.append(f"{output_stdout.strip()}/{i}")
                i+=1
            if output_stderr:
                output_lines.append(output_stderr.strip())

        # tekrardan eski çalışma dizini geçerli dizin olarak ayarlar 
        os.chdir(cwd)

        # Çıktıları kullanma
        stdout_result, stderr_result = process.communicate()
        response_text = f"{stdout_result}\n"

        return {"output_lines": output_lines}

    except Exception as e:
        return {"success": False, "error_message": f"Hata: {str(e)}\n"}