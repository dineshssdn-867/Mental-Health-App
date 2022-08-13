from typing import Any, AnyStr  # Using to define the type
from .api import analyze_emotion
from django.contrib.auth.decorators import login_required  # Importing decorator for verifying the authenticated user
from django.shortcuts import render  # Jinja template engine will parse the contents using render
from django.views.generic.base import TemplateView  # Importing template class based views
from .preprocess import get_clean_data


class FormViewEmotion(TemplateView):  # Initializing template for template view
    template_name = 'predictor/sentiment_emotion_form.html'


@login_required(login_url='/users/login')  # Checking if the user is authenticated
def show_emotion(request: AnyStr) -> Any:
    experience_text = request.POST.get(
        'experience_text')  # Getting the channel/video id from the form using post method
    leisure_text = request.POST.get('leisure_text')
    failures_text = request.POST.get('failures_text')
    life_experience_text = request.POST.get('life_experience_text')

    experience_text = get_clean_data(experience_text)  # Getting the cleaned text using get_clean_data method
    leisure_text = get_clean_data(leisure_text)  # Getting the cleaned text using get_clean_data method
    failures_text = get_clean_data(failures_text)  # Getting the cleaned text using get_clean_data method
    life_experience_text = get_clean_data(life_experience_text)  # Getting the cleaned text using get_clean_data method

    emotion_predictions_experience_text = analyze_emotion(experience_text)  # predicting on the cleaned text

    emotion_predictions_leisure_text = analyze_emotion(leisure_text)  # predicting on the cleaned text

    emotion_predictions_failures_text = analyze_emotion(failures_text)  # predicting on the cleaned text

    emotion_predictions_life_experience_text = analyze_emotion(life_experience_text)  # predicting on the cleaned text

    emotion_labels = emotion_predictions_life_experience_text['emotion_labels']  # getting the labels

    emotion_predictions_experience_text = emotion_predictions_experience_text['emotion_predictions']
    emotion_predictions_leisure_text = emotion_predictions_leisure_text['emotion_predictions']
    emotion_predictions_failures_text = emotion_predictions_failures_text['emotion_predictions']
    emotion_predictions_life_experience_text = emotion_predictions_life_experience_text['emotion_predictions']

    happy = 0
    sad = 0

    emotion_predictions_experience_text_max = max(emotion_predictions_experience_text)
    emotion_predictions_leisure_text_max = max(emotion_predictions_leisure_text)
    emotion_predictions_failures_text_max = max(emotion_predictions_failures_text)
    emotion_predictions_life_experience_text_max = max(emotion_predictions_life_experience_text)

    if emotion_labels[emotion_predictions_experience_text.index(emotion_predictions_experience_text_max)] == 'LOVE' or \
            emotion_labels[
                emotion_predictions_experience_text.index(emotion_predictions_experience_text_max)] == 'JOY':
        happy = happy + emotion_predictions_experience_text_max * .50
    else:
        sad = sad + emotion_predictions_experience_text_max * .50

    if emotion_labels[emotion_predictions_experience_text.index(emotion_predictions_experience_text_max)] == 'LOVE' or \
            emotion_labels[
                emotion_predictions_experience_text.index(emotion_predictions_experience_text_max)] == 'JOY':
        happy = happy + emotion_predictions_leisure_text_max * .15
    else:
        sad = sad + emotion_predictions_leisure_text_max * .15

    if emotion_labels[emotion_predictions_experience_text.index(emotion_predictions_experience_text_max)] == 'LOVE' or \
            emotion_labels[
                emotion_predictions_experience_text.index(emotion_predictions_experience_text_max)] == 'JOY':
        happy = happy + emotion_predictions_failures_text_max * .15
    else:
        sad = sad + emotion_predictions_failures_text_max * .15

    if emotion_labels[emotion_predictions_experience_text.index(emotion_predictions_experience_text_max)] == 'LOVE' or \
            emotion_labels[
                emotion_predictions_experience_text.index(emotion_predictions_experience_text_max)] == 'JOY':
        happy = happy + emotion_predictions_life_experience_text_max * .20
    else:
        sad = sad + emotion_predictions_life_experience_text_max * .20

    if sad > happy:
        message = "You are going through a bad phase in life. But don't worry, bad times are not permanent. Try to " \
                  "seek help from a trained professional to improve your mental health. You can find nearby " \
                  "best Psychiatrist. Please click the button below "
        flag = 1
    else:
        message = \
            "Your mental health looks great! Continue enjoying life and try to help others who are struggling with " \
            "their mental health. "
        flag = 0

    context = {  # setting the context with our data
        'labels': emotion_labels,
        'probabilities_experience_text': emotion_predictions_experience_text,
        'probabilities_leisure_text': emotion_predictions_leisure_text,
        'probabilities_failures_text': emotion_predictions_failures_text,
        'probabilities_life_experience_text': emotion_predictions_life_experience_text,
        'message': message,
        'happy': happy,
        'sad': sad,
        'flag': flag

    }
    return render(request, 'predictor/results_emotion.html',
                  context=context)  # rendering template with out data using jinja template engine
