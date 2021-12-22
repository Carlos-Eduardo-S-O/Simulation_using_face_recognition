import face_recognition

def configure_recognition(original_photo):
    photo = face_recognition.load_image_file(original_photo)
    
    return face_recognition.face_encodings(photo)[0]

def compare_faces(photo1, photo2):
    result = None
    
    try: 
        photo1_encoding = configure_recognition(photo1)
        photo2_encoding = configure_recognition(photo2)
        
        result = face_recognition.compare_faces([photo1_encoding], photo2_encoding)
    except Exception as e:
        print(e)
    
    return result
    
def recognizer(visitor_photo, photos):
    count = 0
    
    for photo in photos:
        if compare_faces(visitor_photo, photo["photo"]) == [True]:
            count +=1
    result = (count > 2)
    
    return result
