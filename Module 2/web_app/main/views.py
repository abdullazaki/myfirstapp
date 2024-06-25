from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import joblib
from sklearn.svm import SVC
from .models import Disease
from .models import UserPredictions


def home(request):
    return render(request, 'index.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        passwrd = request.POST.get('passwrd')

        user = authenticate(request, username = username, password = passwrd)
        if user is not None:
            login(request, user)
            messages.success(request, "Loged In Successfully!")
            return redirect('home')
        else:
            messages.error(request, "Invalid Credentials!")
            return HttpResponseRedirect(request.path_info)
        
    return render(request, 'login.html')


def user_signup(request):
    if request.method=='POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'Password and confirm passowrd must be same!')
            return HttpResponseRedirect(request.path_info)
        else:
            user = User.objects.create(
                first_name = name, 
                username = username, 
                email = email, 
                )
            user.set_password(password1)
            user.save()
            messages.success(request, "Registration successfull!")
            return redirect('user_login')
        
    return render(request, 'signup.html')


def createDiseaseObjects(request):
    diseaselist=['Fungal infection','Allergy','GERD','Chronic cholestasis','Drug Reaction','Peptic ulcer diseae','AIDS','Diabetes ',
  'Gastroenteritis','Bronchial Asthma','Hypertension ','Migraine','Cervical spondylosis','Paralysis (brain hemorrhage)',
  'Jaundice','Malaria','Chicken pox','Dengue','Typhoid','hepatitis A', 'Hepatitis B', 'Hepatitis C', 'Hepatitis D',
  'Hepatitis E', 'Alcoholic hepatitis','Tuberculosis', 'Common Cold', 'Pneumonia', 'Dimorphic hemmorhoids(piles)',
  'Heart attack', 'Varicose veins','Hypothyroidism', 'Hyperthyroidism', 'Hypoglycemia', 'Osteoarthristis',
  'Arthritis', '(vertigo) Paroymsal  Positional Vertigo','Acne', 'Urinary tract infection', 'Psoriasis', 'Impetigo']
    for disease in diseaselist:
        obj = Disease.objects.create(name = disease)
        obj.save()
    return HttpResponse("disease objects created successfully!")
    

def checkdisease(request): 
    diseaselist=['Fungal infection','Allergy','GERD','Chronic cholestasis','Drug Reaction','Peptic ulcer diseae','AIDS','Diabetes ',
  'Gastroenteritis','Bronchial Asthma','Hypertension ','Migraine','Cervical spondylosis','Paralysis (brain hemorrhage)',
  'Jaundice','Malaria','Chicken pox','Dengue','Typhoid','hepatitis A', 'Hepatitis B', 'Hepatitis C', 'Hepatitis D',
  'Hepatitis E', 'Alcoholic hepatitis','Tuberculosis', 'Common Cold', 'Pneumonia', 'Dimorphic hemmorhoids(piles)',
  'Heart attack', 'Varicose veins','Hypothyroidism', 'Hyperthyroidism', 'Hypoglycemia', 'Osteoarthristis',
  'Arthritis', '(vertigo) Paroymsal  Positional Vertigo','Acne', 'Urinary tract infection', 'Psoriasis', 'Impetigo']


    symptomslist=['itching','skin_rash','nodal_skin_eruptions','continuous_sneezing','shivering','chills','joint_pain',
    'stomach_pain','acidity','ulcers_on_tongue','muscle_wasting','vomiting','burning_micturition','spotting_ urination',
    'fatigue','weight_gain','anxiety','cold_hands_and_feets','mood_swings','weight_loss','restlessness','lethargy',
    'patches_in_throat','irregular_sugar_level','cough','high_fever','sunken_eyes','breathlessness','sweating',
    'dehydration','indigestion','headache','yellowish_skin','dark_urine','nausea','loss_of_appetite','pain_behind_the_eyes',
    'back_pain','constipation','abdominal_pain','diarrhoea','mild_fever','yellow_urine',
    'yellowing_of_eyes','acute_liver_failure','fluid_overload','swelling_of_stomach',
    'swelled_lymph_nodes','malaise','blurred_and_distorted_vision','phlegm','throat_irritation',
    'redness_of_eyes','sinus_pressure','runny_nose','congestion','chest_pain','weakness_in_limbs',
    'fast_heart_rate','pain_during_bowel_movements','pain_in_anal_region','bloody_stool',
    'irritation_in_anus','neck_pain','dizziness','cramps','bruising','obesity','swollen_legs',
    'swollen_blood_vessels','puffy_face_and_eyes','enlarged_thyroid','brittle_nails',
    'swollen_extremeties','excessive_hunger','extra_marital_contacts','drying_and_tingling_lips',
    'slurred_speech','knee_pain','hip_joint_pain','muscle_weakness','stiff_neck','swelling_joints',
    'movement_stiffness','spinning_movements','loss_of_balance','unsteadiness',
    'weakness_of_one_body_side','loss_of_smell','bladder_discomfort','foul_smell_of urine',
    'continuous_feel_of_urine','passage_of_gases','internal_itching','toxic_look_(typhos)',
    'depression','irritability','muscle_pain','altered_sensorium','red_spots_over_body','belly_pain',
    'abnormal_menstruation','dischromic _patches','watering_from_eyes','increased_appetite','polyuria','family_history','mucoid_sputum',
    'rusty_sputum','lack_of_concentration','visual_disturbances','receiving_blood_transfusion',
    'receiving_unsterile_injections','coma','stomach_bleeding','distention_of_abdomen',
    'history_of_alcohol_consumption','fluid_overload','blood_in_sputum','prominent_veins_on_calf',
    'palpitations','painful_walking','pus_filled_pimples','blackheads','scurring','skin_peeling',
    'silver_like_dusting','small_dents_in_nails','inflammatory_nails','blister','red_sore_around_nose',
    'yellow_crust_ooze']
    
    disease_precautions = {
    'Drug Reaction': ['stop irritation', 'consult nearest hospital', 'stop taking drug', 'follow up'],
    'Malaria': ['Consult nearest hospital', 'avoid oily food', 'avoid non veg food', 'keep mosquitos out'],
    'Allergy': ['apply calamine', 'cover area with bandage', 'use ice to compress itching'],
    'Hypothyroidism': ['reduce stress', 'exercise', 'eat healthy', 'get proper sleep'],
    'Psoriasis': ['wash hands with warm soapy water', 'stop bleeding using pressure', 'consult doctor', 'salt baths'],
    'GERD': ['avoid fatty spicy food', 'avoid lying down after eating', 'maintain healthy weight', 'exercise'],
    'Chronic cholestasis': ['cold baths', 'anti itch medicine', 'consult doctor', 'eat healthy'],
    'hepatitis A': ['Consult nearest hospital', 'wash hands through', 'avoid fatty spicy food', 'medication'],
    'Osteoarthristis': ['acetaminophen', 'consult nearest hospital', 'follow up', 'salt baths'],
    '(vertigo) Paroymsal  Positional Vertigo': ['lie down', 'avoid sudden change in body', 'avoid abrupt head movement', 'relax'],
    'Hypoglycemia': ['lie down on side', 'check in pulse', 'drink sugary drinks', 'consult doctor'],
    'Acne': ['bath twice', 'avoid fatty spicy food', 'drink plenty of water', 'avoid too many products'],
    'Diabetes': ['have balanced diet', 'exercise', 'consult doctor', 'follow up'],
    'Impetigo': ['soak affected area in warm water', 'use antibiotics', 'remove scabs with wet compressed cloth', 'consult doctor'],
    'Hypertension': ['meditation', 'salt baths', 'reduce stress', 'get proper sleep'],
    'Peptic ulcer disease': ['avoid fatty spicy food', 'consume probiotic food', 'eliminate milk', 'limit alcohol'],
    'Dimorphic hemorrhoids(piles)': ['avoid fatty spicy food', 'consume witch hazel', 'warm bath with epsom salt', 'consume aloe vera juice'],
    'Common Cold': ['drink vitamin C rich drinks', 'take vapor', 'avoid cold food', 'keep fever in check'],
    'Chicken pox': ['use neem in bathing', 'consume neem leaves', 'take vaccine', 'avoid public places'],
    'Cervical spondylosis': ['use heating pad or cold pack', 'exercise', 'take OTC pain reliever', 'consult doctor'],
    'Hyperthyroidism': ['eat healthy', 'massage', 'use lemon balm', 'take radioactive iodine treatment'],
    'Urinary tract infection': ['drink plenty of water', 'increase vitamin C intake', 'drink cranberry juice', 'take probiotics'],
    'Varicose veins': ['lie down flat and raise the leg high', 'use ointments', 'use vein compression', 'don’t stand still for long'],
    'AIDS': ['avoid open cuts', 'wear PPE if possible', 'consult doctor', 'follow up'],
    'Paralysis (brain hemorrhage)': ['massage', 'eat healthy', 'exercise', 'consult doctor'],
    'Typhoid': ['eat high-calorie vegetables', 'antibiotic therapy', 'consult doctor', 'medication'],
    'Hepatitis B': ['consult nearest hospital', 'vaccination', 'eat healthy', 'medication'],
    'Fungal infection': ['bath twice', 'use Dettol or neem in bathing water', 'keep infected area dry', 'use clean cloths'],
    'Hepatitis C': ['Consult nearest hospital', 'vaccination', 'eat healthy', 'medication'],
    'Migraine': ['meditation', 'reduce stress', 'use polaroid glasses in sun', 'consult doctor'],
    'Bronchial Asthma': ['switch to loose clothing', 'take deep breaths', 'get away from triggers', 'seek help'],
    'Alcoholic hepatitis': ['stop alcohol consumption', 'consult doctor', 'medication', 'follow up'],
    'Jaundice': ['drink plenty of water', 'consume milk thistle', 'eat fruits and high fibrous food', 'medication'],
    'Hepatitis E': ['stop alcohol consumption', 'rest', 'consult doctor', 'medication'],
    'Dengue': ['drink papaya leaf juice', 'avoid fatty spicy food', 'keep mosquitos away', 'keep hydrated'],
    'Hepatitis D': ['consult doctor', 'medication', 'eat healthy', 'follow up'],
    'Heart attack': ['call ambulance', 'chew or swallow aspirin', 'keep calm', ''],
    'Pneumonia': ['consult doctor', 'medication', 'rest', 'follow up'],
    'Arthritis': ['exercise', 'use hot and cold therapy', 'try acupuncture', 'massage'],
    'Gastroenteritis': ['stop eating solid food for a while', 'try taking small sips of water', 'rest', 'ease back into eating'],
    'Tuberculosis': ['cover mouth', 'consult doctor', 'medication', 'rest']
    }


    alphabaticsymptomslist = sorted(symptomslist)
    model = joblib.load('main/svc_model')


    if request.method == 'GET':
        return render(request,'checkdisease.html', {"symptoms_list":alphabaticsymptomslist})
  
    elif request.method == 'POST':
        symptom1 = request.POST.get('symptom1')
        symptom2 = request.POST.get('symptom2')
        symptom3 = request.POST.get('symptom3')
        symptom4 = request.POST.get('symptom4')
        symptom5 = request.POST.get('symptom5')
        symptom6 = request.POST.get('symptom6')
        print(symptom1)
        print(symptom2)
        print(symptom3)
        print(symptom4)
        print(symptom5)
        print(symptom6)
        
        encoded_list = symptomslist
        for idx, symptom in enumerate(symptomslist):
            if symptom == symptom1:
                encoded_list[idx] = 1
            elif symptom == symptom2:
                encoded_list[idx] = 1
            elif symptom == symptom3:
                encoded_list[idx] = 1
            elif symptom == symptom4:
                encoded_list[idx] = 1
            elif symptom == symptom5:
                encoded_list[idx] = 1
            elif symptom == symptom6:
                encoded_list[idx] = 1
            else:
                encoded_list[idx] = 0
        
        # prediction = model.predict([encoded_list])
        # Predict disease label
        prediction_label = model.predict([encoded_list])[0]  # Get the predicted label
        prediction_index = list(model.classes_).index(prediction_label)  # Get the index of the predicted label

        # Get probabilities for all classes
        probabilities = model.predict_proba([encoded_list])[0]

    # Get probability for the predicted class
        probability_of_prediction = probabilities[prediction_index]
        probablity_percentage = round(probability_of_prediction * 100)
        print("probability",probablity_percentage)
        precautions = disease_precautions[prediction_label]
        print(precautions)

        predObj = UserPredictions.objects.create(
         user = request.user,
         disease = prediction_label,
         probablity = probablity_percentage,
         symptom1 = symptom1,
         symptom2 = symptom2,
         symptom3 = symptom3,
         symptom4 = symptom4,
         symptom5 = symptom5,
         symptom6 = symptom6,
        )
        predObj.save()
        return JsonResponse({'predicteddisease': prediction_label,
                         'confidencescore': probablity_percentage,
                         'precautions': precautions})