# OOSA Final Code Project - Reading and Manipulating LVIS data

This repo contains code spread over 5 'Tasks' designed to read a series of h5 files and process them into a set of raster tifs ready for manipulation.

## Table of Contents
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Usage](#usage)

---

## Introduction

The pine island glacier is an area of scientific importance attributed to its state of flux. The implications of anthropogenic climate change on it's elevation profile 
is a critical element of concern. The LVIS (Land, Vegetation and Ice Sensor) was used during NASA's Operation Ice Bridge to produce DEMs using LiDAR return information, 
specifically over areas with existing data gaps. - Our data was collected for the years 2009 and 2015, in the form of h3 files which are to be converted to tif extents 
using specialised python methods.

---

## Installation

Steps to install and run the project locally:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/OOSAB277937.git



## Usage

The repository contains a series of python files. (Task1.py, Task2.py, Task3.py, Task4.py, Task5.py), correspond to the tasks listed in the assignment whereas the remaining
files contain methods and dependancies which ensure the correct functioning of the code.

It is important that the data in question is sourced from the corect location within Netdata which is as follows:

"/geos/netdata/oosa/assignment/lvis"

- This will ensure the code runs correctly

# Task 1

Task 1 contains code to plot a single LVIS waveform as specified in the command line. Users should ensure matplotlib is installed within your environment. As no argument
parser is used users should simply run and follow the command prompt to select their waveform of choice. - The expected output will be matplotlib line graph.

# Task 2

Task 2 takes a pair of parsable arguments corresponding to file path and output resolution. These are handled as follows:

{"file"} {input filepath location} {output file resolution}

The expected output will be a tif file saved to working directory giving elevation of the extent covered by the h3 file over the glacier boundaries

# Task 3

Task 3 follows the same parseing conventions as Task 2 however the file path should specifiy either the 2009 or 2015 folder as
opposed to a specific h3 file 

The expected output will be a tif file containing every tif extent within the alloted glacier bounds 

# Task 4

Task 4 includes an additional arguments to be parsed which specifies the pixel distance around the extant non naN values which will be interpolated using the GapFillfunction.
The following format is to be used:

{"file"} {input filepath location} --searchdist {search distance} {output file resolution}

The expected output will take the form of a tif file containing the interpolated flight path elevation extents.

# Task 5

Task 5 includes an additional arugment which identifies the filepath for the additional file which is to be used 

{"file"} {input filepath location} --filename2 {input filepath location 2} {output file resolution}

The expect output will take the form of a tif file illustrating elevation change between the years 2009 and 2015