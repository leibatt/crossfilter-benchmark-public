#!/bin/bash

vl2svg server-response-rate.vl.json > server-response-rate.svg
vl2svg server-mean-duration-with-errorbars.vl.json server-mean-duration-with-errorbars.svg
cairosvg server-response-rate.svg -o server-response-rate.pdf
cairosvg server-mean-duration-with-errorbars.svg -o server-mean-duration-with-errorbars.pdf
