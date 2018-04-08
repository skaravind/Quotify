from django.shortcuts import render
from keras.models import load_model
from .quoteGetter import quotify
from django.core.files.storage import FileSystemStorage
import os
import numpy as np
from keras.applications.resnet50 import preprocess_input, decode_predictions
from PIL import Image
from keras import backend as K

def initialize_model():
	model = load_model('detection/resnet50.hd5')
	model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
	return model

def cleanup():
	files = [f for f in os.listdir('media/')]
	for f in files:
		os.remove('media/'+f)


def home(request):
	result = ["Couldn't ","Quotify"," this image","S K Aravind"]
	prediction = 'Nothing'
	if request.method == 'POST':
		cleanup()
		try:
			request.FILES['image']
		except:
			return render(request, 'detection/home.html')
		if 'model' in locals():
			pass
		else:
			model = initialize_model()
		myfile = request.FILES['image']
		fs = FileSystemStorage()
		filename = fs.save(myfile.name, myfile)
		fname = myfile.name
		uploaded_file_url = fs.url(filename)
		if not (fname.endswith('.jpg') or fname.endswith('.jpeg') or fname.endswith('.JPG')):
			if (fname.endswith('.PNG') or fname.endswith('.png')):
				img = img = Image.open('media/'+myfile.name).resize((224,224))
				img = np.array(img).astype('float64')
				img = img[:,:,:3]
				img = np.expand_dims(img, axis=0)
				img = preprocess_input(img)
			else:
				pass
		else:
			img = Image.open('media/'+myfile.name).resize((224,224))
			img = np.array(img).astype('float64')
			img = np.expand_dims(img, axis=0)
			img = preprocess_input(img)
		try:
			preds = model.predict(img)
			prediction = decode_predictions(preds, top=1)[0][0][1].replace("_"," ").replace("-"," ")
			result = quotify(prediction)
			print(prediction)
			if result == 0:
				result = ["Couldn't ","Quotify"," this image","S K Aravind"]
		except:
			result = ["Couldn't ","Quotify"," this image","S K Aravind"]
		K.clear_session()
		return render(request, 'detection/home.html', {
			'uploaded_file_url': uploaded_file_url,
			'first' : result[0],
			'keyword' : result[1],
			'second' : result[2],
			'author' : result[3],
			'prediction' : prediction
		})
	K.clear_session()
	return render(request, 'detection/home.html')



