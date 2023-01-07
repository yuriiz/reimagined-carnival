from random import randint

import cv2
import numpy as np
from cellpose import models
from django.http import HttpResponse
from django.shortcuts import render

from .forms import InputForm


def home(request):
    form = InputForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        # decode image as grayscale
        img = cv2.imdecode(
            np.asarray(bytearray(form.cleaned_data["image"].read())), 0)
        model = models.Cellpose(gpu=False,
                                model_type=form.cleaned_data["type"])
        (masks, ), flows, styles, diams = model.eval(
            [img], diameter=form.cleaned_data["diameter"])
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        for cell in range(1, masks.max() + 1):
            # draw contour around each cell with random colour
            contours, hierarchy = cv2.findContours(
                (masks == cell).astype(np.uint8), cv2.RETR_TREE,
                cv2.CHAIN_APPROX_SIMPLE)
            cv2.drawContours(
                img,
                contours,
                -1,
                (randint(0, 255), randint(0, 255), randint(0, 255)),
                3,
            )
        ok, array = cv2.imencode(".png", img)
        return HttpResponse(array.tobytes(), "image/png")
    return render(request, "base.html", {"form": form})
