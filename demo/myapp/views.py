# from django.shortcuts import render, redirect, get_object_or_404
# from .models import Book
# from .forms import BookForm

# # List view (Read)
# def book_list(request):
#     books = Book.objects.all()
#     return render(request, 'myapp/book_list.html', {'books': books})

# # Create view
# def book_create(request):
#     form = BookForm(request.POST or None)
#     if form.is_valid():
#         form.save()
#         return redirect('book_list')
#     return render(request, 'myapp/book_form.html', {'form': form})

# # Update view
# def book_update(request, pk):
#     book = get_object_or_404(Book, pk=pk)
#     form = BookForm(request.POST or None, instance=book)
#     if form.is_valid():
#         form.save()
#         return redirect('book_list')
#     return render(request, 'myapp/book_form.html', {'form': form})

# # Delete view
# def book_delete(request, pk):
#     book = get_object_or_404(Book, pk=pk)
#     if request.method == 'POST':
#         book.delete()
#         return redirect('book_list')
#     return render(request, 'myapp/book_confirm_delete.html', {'book': book})
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from ultralytics import YOLO
import os
from django.http import StreamingHttpResponse
import cv2
# Load YOLO Model
model = YOLO('myapp/media/best.pt')  # Ensure 'best.pt' is in the 'media' folder

def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']
        fs = FileSystemStorage(location='myapp/media/uploads/')
        file_path = fs.save(uploaded_file.name, uploaded_file)
        
        # YOLO Prediction
        input_path = fs.path(file_path)
        output_dir = 'myapp/media/outputs'
        os.makedirs(output_dir, exist_ok=True)
        model.predict(source=input_path, save=True, project=output_dir, name=uploaded_file.name)
        
        return render(request, 'myapp/upload_file.html', {
            'input_file': f'/media/uploads/{uploaded_file.name}',
            'output_file': f'/media/outputs/{uploaded_file.name}/{uploaded_file.name}'

        })
    return   render(request, 'myapp/upload_file.html')


def list_files(request):
    uploads = os.listdir('myapp/media/uploads/')
    outputs = os.listdir('myapp/media/outputs/')
    return render(request, 'myapp/file_list.html', {'uploads': uploads, 'outputs': outputs})
 
def gen_frames():
    # Open the webcam (device 0 by default)
    video_capture = cv2.VideoCapture(0)
    while True:
        success, frame = video_capture.read()
        if not success:
            break
        else:
            # Perform YOLO prediction on the frame
            results = model(frame)  # Run YOLO inference
            
            # Iterate over the predictions and draw boxes with labels
            for result in results:
                for box, conf, cls in zip(result.boxes.xyxy, result.boxes.conf, result.boxes.cls):
                    x1, y1, x2, y2 = map(int, box[:4])  # Get bounding box coordinates
                    
                    # Get the class label and confidence score
                    class_name = model.names[int(cls)]  # Get the class name
                    confidence = round(float(conf), 2)  # Confidence score
                    
                    # Draw the bounding box
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    
                    # Put the label (class name and confidence)
                    if(class_name=='helmet' and confidence<0.7):
                        class_name='no helmet'
                    label = f'{class_name} {confidence}'
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(frame, label, (x1, y1 - 10), font, 0.6, (0, 0, 0), 2)
            
            # Convert the frame to byte data for streaming
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Yield the frame to the client
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def webcam_prediction(request):
    return StreamingHttpResponse(gen_frames(), content_type='multipart/x-mixed-replace; boundary=frame')

def webcam_view(request):
    return render(request, 'myapp/webcam_view.html')
def index(request):
    return render(request, 'myapp/index.html')