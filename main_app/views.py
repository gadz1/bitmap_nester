from django.shortcuts import render, redirect
from .models import nesters
from django.contrib import messages
from django.http import JsonResponse
from .models import new_in
from .models import history_m
from .genetic_algorithm import *
import os
from django.conf import settings
from svgpathtools import svg2paths

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        name = request.POST.get('name')
        
        # Check if the email already exists
        if nesters.objects.filter(mail=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('/')

        # Create a new user object
        new_user = nesters(name=name, mail=email,password=password)
        new_user.save()
        messages.success(request, 'User registered successfully.')
        return redirect('/')

    return render(request, "register.html", {})

def sign(request):
    if request.method == 'POST':
        email = request.POST.get('mail')
        password = request.POST.get('pass')
        user = nesters.objects.get(mail=email)
        if user.password == password:
            messages.success(request, f'Login successful. Email: {email}, Password: {password}')
            return redirect('home.html/')
        else:
            messages.error(request, f'Login failed. Email: {email}, Password: {password}')

    return render(request, 'sign.html')

import vtracer
def hyper(request):
    data = new_in.objects.all()
    for i, obj in enumerate(data):
        inp = obj.input_image.path
        dir=os.path.dirname(inp)
        out = os.path.join(dir , f"out{i}.svg")
        print(out)
        vtracer.convert_image_to_svg_py(
            inp,
            out,
            colormode='binary',       # ["color"] or "binary"
            hierarchical='stacked',   # ["stacked"] or "cutout"
            mode='spline',            # ["spline"] "polygon", or "none"
            filter_speckle=1,         # default: 4
            color_precision=6,        # default: 6
            layer_difference=16,      # default: 16
            corner_threshold=50,      # default: 60
            length_threshold=3.5,     # in [3.5, 10] default: 4.0
            max_iterations=10,        # default: 10
            splice_threshold=40,      # default: 45
            path_precision=10         # default: 8
        )
    if request.method == 'POST':
        w = request.POST.get('width')
        h = request.POST.get('height')
        gen = request.POST.get('gen')
        size = request.POST.get('size')

        return redirect('/result.html')
    
    return render(request, 'hyper.html')

def home(request):
    data=new_in.objects.all()
    context={"items":data}
    return render(request, 'home.html',context)

#====================================================
def point_line_distance(point, start, end):
    """
    Calculate the perpendicular distance from a point to a line.
    """
    if np.array_equal(start, end):
        return np.linalg.norm(point - start)
    return np.linalg.norm(np.cross(end - start, start - point)) / np.linalg.norm(end - start)

def rdp(points, epsilon):
    """
    The Ramer-Douglas-Peucker algorithm.
    :param points: List of points as tuples or numpy arrays.
    :param epsilon: The maximum distance threshold.
    :return: The simplified list of points.
    """
    points = np.array(points)  # Convert list of tuples to numpy array
    if len(points) < 3:
        return points

    # Find the point with the maximum distance from the line between the start and end
    dmax = 0.0
    index = 0
    for i in range(1, len(points) - 1):
        d = point_line_distance(points[i], points[0], points[-1])
        if d > dmax:
            index = i
            dmax = d

    # If max distance is greater than epsilon, recursively simplify
    if dmax > epsilon:
        # Recursive call
        results1 = rdp(points[:index + 1], epsilon)
        results2 = rdp(points[index:], epsilon)

        # Build the result list
        result = np.vstack((results1[:-1], results2))
    else:
        result = np.array([points[0], points[-1]])

    return result

#=========================================================
def result(request):
    polys=[]
    media_root = settings.MEDIA_ROOT
    for filename in os.listdir(media_root):
        if filename.endswith('.svg'):
            file_path= os.path.join(settings.MEDIA_ROOT, filename)
            paths, _ = svg2paths(file_path)
            coordinates = []
            for path in paths:
                for line in path:
                    start = (line.start.real, line.start.imag)
                    end = (line.end.real, line.end.imag)
                    coordinates.append(start)
                    coordinates.append(end)
            #ramer douglas
            poly=rdp(coordinates, 1.0)
            poly=poly.tolist()
            polys.append(poly)

            all_rotation = [0,45,90,135,180,225,270,315]
            poly_list = PolyListProcessor.getPolyObjectList(polys, all_rotation)
            nfp_assistant=NFPAssistant(polys, store_nfp=False, get_all_nfp=True, load_history=True)
            GA(760,poly_list,nfp_asst=nfp_assistant).global_best_sequence
           
    #print(polys)   
    return render(request, 'result.html')

def history(request):
    data=history_m.objects.all()
    context={"items":data}
    return render(request, 'history.html',context)

def delete_item(request,item_id):
    item=new_in.objects.get(pk=item_id)
    if os.path.exists(item.input_image.path):os.remove(item.input_image.path)
    item.delete()
    return redirect('/home.html')

from .img_proc import *
import cv2


def upload_image_view(request):
    if request.method == 'POST' and request.FILES.get('file-upload'):
        uploaded_file = request.FILES['file-upload']
        # Process the image with OpenCV
        processed_images = split_by_cont(uploaded_file)
        
        # Get the ID of the last object created in the model
        last_input_instance_id = new_in.objects.latest('id').id if new_in.objects.exists() else 0

        # Save each processed image
        for image in processed_images:
            last_input_instance_id += 1
            processed_image_name = f'out_img_{last_input_instance_id}.jpg'
            processed_image_path = os.path.join(settings.MEDIA_ROOT, processed_image_name)
            cv2.imwrite(processed_image_path, image)
            input_instance = new_in.objects.create(input_image=processed_image_name)

        return redirect('/home.html')
    else:
        return JsonResponse({'error': 'No image file provided'})
    