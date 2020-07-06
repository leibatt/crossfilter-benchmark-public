#!/bin/bash

vl2svg laptop-response-rate.vl.json > laptop-response-rate.svg
vl2svg laptop-mean-duration-with-errorbars.vl.json laptop-mean-duration-with-errorbars.svg
cairosvg laptop-response-rate.svg -o laptop-response-rate.pdf
cairosvg laptop-mean-duration-with-errorbars.svg -o laptop-mean-duration-with-errorbars.pdf
