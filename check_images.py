#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# */AIPND/intropylab-classifying-images/check_images.py
#                                                                             
# TODO: 0. Fill in your information in the programming header below
# PROGRAMMER:
# DATE CREATED:
# REVISED DATE:             <=(Date Revised - if any)
# REVISED DATE: 05/14/2018 - added import statement that imports the print 
#                           functions that can be used to check the lab
# PURPOSE: Check images & report results: read them in, predict their
#          content (classifier), compare prediction to actual value labels
#          and output results
#
# Use argparse Expected Call with <> indicating expected user input:
#      python check_images.py --dir <directory with images> --arch <model>
#             --dogfile <file that contains dognames>
#   Example call:
#    python check_images.py --dir pet_images/ --arch vgg --dogfile dognames.txt
##

# Imports python modules
import argparse
from time import time, sleep
from os import listdir

# Imports classifier function for using CNN to classify images 
from classifier import classifier 

# Imports print functions that check the lab
from print_functions_for_lab_checks import *

# Main program function defined below
def main():
    # TODO: 1. Define start_time to measure total program runtime by
    # collecting start time
    start_time = time()
    
    # TODO: 2. Define get_input_args() function to create & retrieve command
    # line arguments
    in_arg = get_input_args()
    
    # TODO: 3. Define get_pet_labels() function to create pet image labels by
    # creating a dictionary with key=filename and value=file label to be used
    # to check the accuracy of the classifier function
    answers_dic = get_pet_labels(in_arg.dir)

    # TODO: 4. Define classify_images() function to create the classifier 
    # labels with the classifier function uisng in_arg.arch, comparing the 
    # labels, and creating a dictionary of results (result_dic)
    result_dic = classify_images(in_arg.dir, answers_dic, in_arg.arch)
    
    
    print("\n       MATCH:")
    n_match = 0
    n_notmatch = 0
    for key in result_dic:
        if result_dic[key][2] == 1:
            n_match += 1;
            print("Real : %-26s  Classifier: %-30s" % (result_dic[key][0],
                                                       result_dic[key][1]))
    
    print("\n NOT A MATCH:")
    for key in result_dic:
        if result_dic[key][2] == 0:
            n_notmatch += 1;
            print("Real : %-26s  Classifier: %-30s" % (result_dic[key][0],
                                                       result_dic[key][1]))
                  
    print("\n # Total images", n_match + n_notmatch, "# matches: ", 
          n_match, "# not matches: ", n_notmatch)
            
    # TODO: 5. Define adjust_results4_isadog() function to adjust the results
    # dictionary(result_dic) to determine if classifier correctly classified
    # images as 'a dog' or 'not a dog'. This demonstrates if the model can
    # correctly classify dog images as dogs (regardless of breed)
    adjust_results4_isadog(result_dic, in_arg.dogfile)

    # TODO: 6. Define calculates_results_stats() function to calculate
    # results of run and puts statistics in a results statistics
    # dictionary (results_stats_dic)
    results_stats_dic = calculates_results_stats(result_dic)

    # TODO: 7. Define print_results() function to print summary results, 
    # incorrect classifications of dogs and breeds if requested.
    print_results(result_dic, results_stats_dic, in_arg.arch)

    # TODO: 1. Define end_time to measure total program runtime
    # by collecting end time
    end_time = time()

    # TODO: 1. Define tot_time to computes overall runtime in
    # seconds & prints it in hh:mm:ss format
    tot_time = start_time - end_time
    print("\n** Total Elapsed Runtime:", tot_time)



# TODO: 2.-to-7. Define all the function below. Notice that the input 
# paramaters and return values have been left in the function's docstrings. 
# This is to provide guidance for acheiving a solution similar to the 
# instructor provided solution. Feel free to ignore this guidance as long as 
# you are able to acheive the desired outcomes with this lab.

def get_input_args():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir', type=str, default='pet_images/', 
                        help='path to folder of images')
    parser.add_argument('--arch', default="vgg")
    parser.add_argument('--dogfile', default="dognames.txt")
    
    return parser.parse_args()
    """
    Retrieves and parses the command line arguments created and defined using
    the argparse module. This function returns these arguments as an
    ArgumentParser object. 
     3 command line arguements are created:
       dir - Path to the pet image files(default- 'pet_images/')
       arch - CNN model architecture to use for image classification(default-
              pick any of the following vgg, alexnet, resnet)
       dogfile - Text file that contains all labels associated to dogs(default-
                'dognames.txt'
    Parameters:
     None - simply using argparse module to create & store command line arguments
    Returns:
     parse_args() -data structure that stores the command line arguments object  
    """
    


def get_pet_labels(dirPath):
    in_files = listdir(dirPath)
    
    # Processes each of the files to create a dictionary where the key
    # is the filename and the value is the picture label (below).
 
    # Creates empty dictionary for the labels
    petlabels_dic = dict()
   
    # Processes through each file in the directory, extracting only the words
    # of the file that contain the pet image label
    for idx in range(0, len(in_files), 1):
       
       # Skips file if starts with . (like .DS_Store of Mac OSX) because it 
       # isn't an pet image file
       if in_files[idx][0] != ".":
           
           # Uses split to extract words of filename into list image_name 
           image_name = in_files[idx].split("_")
       
           # Creates temporary label variable to hold pet label name extracted 
           pet_label = ""
           
           # Processes each of the character strings(words) split by '_' in 
           # list image_name by processing each word - only adding to pet_label
           # if word is all letters - then process by putting blanks between 
           # these words and putting them in all lowercase letters
           for word in image_name:
               
               # Only add to pet_label if word is all letters add blank at end
               if word.isalpha():
                   pet_label += word.lower() + " "
                   
           # strips off trailing whitespace
           pet_label = pet_label.strip()
           
           # If filename doesn't already exist in dictionary add it and it's
           # pet label - otherwise print an error message because indicates 
           # duplicate files (filenames)
           if in_files[idx] not in petlabels_dic:
              petlabels_dic[in_files[idx]] = pet_label
              
           else:
               print("Warning: Duplicate files exist in directory", 
                     in_files[idx])
 
    # returns dictionary of labels
    return(petlabels_dic)
                
           
           
           
        
        
    
    """
    Creates a dictionary of pet labels based upon the filenames of the image 
    files. Reads in pet filenames and extracts the pet image labels from the 
    filenames and returns these label as petlabel_dic. This is used to check 
    the accuracy of the image classifier model.
    Parameters:
     image_dir - The (full) path to the folder of images that are to be
                 classified by pretrained CNN models (string)
    Returns:
     petlabels_dic - Dictionary storing image filename (as key) and Pet Image
                     Labels (as value)  
    """
    


def classify_images(images_dir, petlabel_dic, model):

    results_dic = dict()

    # Process all files in the petlabels_dic - use images_dir to give fullpath
    for key in petlabel_dic:
       
       # Runs classifier function to classify the images classifier function 
       # inputs: path + filename  and  model, returns model_label 
       # as classifier label
       pathDog = "./" + images_dir +"/" + key
       model_label = classifier(pathDog, model)
       
       # Processes the results so they can be compared with pet image labels
       # set labels to lowercase (lower) and stripping off whitespace(strip)
       model_label = model_label.lower()
       model_label = model_label.strip()
       
       # defines truth as pet image label and trys to find it using find() 
       # string function to find it within classifier label(model_label).
       truth = petlabel_dic[key]
       found = model_label.find(truth)
       
       # If found (0 or greater) then make sure true answer wasn't found within
       # another word and thus not really found, if truely found then add to 
       # results dictionary and set match=1(yes) otherwise as match=0(no)
       if found >= 0:
           if ( (found == 0 and len(truth)==len(model_label)) or
                (  ( (found == 0) or (model_label[found - 1] == " ") )  and
                   ( (found + len(truth) == len(model_label)) or   
                      (model_label[found + len(truth): found+len(truth)+1] in 
                     (","," ") ) 
                   )      
                )
              ):
               # found label as stand-alone term (not within label)
               if key not in results_dic:
                   results_dic[key] = [truth, model_label, 1]
                   
           # found within a word/term not a label existing on its own 
           else:
               if key not in results_dic:
                   results_dic[key] = [truth, model_label, 0]
                   
       # if not found set results dictionary with match=0(no)
       else:
           if key not in results_dic:
               results_dic[key] = [truth, model_label, 0]
               
    # Return results dictionary
    return(results_dic)
                  
                        
                        
                        
                        
                        
                  
    """
    Creates classifier labels with classifier function, compares labels, and 
    creates a dictionary containing both labels and comparison of them to be
    returned.
     PLEASE NOTE: This function uses the classifier() function defined in 
     classifier.py within this function. The proper use of this function is
     in test_classifier.py Please refer to this program prior to using the 
     classifier() function to classify images in this function. 
     Parameters: 
      images_dir - The (full) path to the folder of images that are to be
                   classified by pretrained CNN models (string)
      petlabel_dic - Dictionary that contains the pet image(true) labels
                     that classify what's in the image, where its' key is the
                     pet image filename & it's value is pet image label where
                     label is lowercase with space between each word in label 
      model - pretrained CNN whose architecture is indicated by this parameter,
              values must be: resnet alexnet vgg (string)
     Returns:
      results_dic - Dictionary with key as image filename and value as a List 
             (index)idx 0 = pet image label (string)
                    idx 1 = classifier label (string)
                    idx 2 = 1/0 (int)   where 1 = match between pet image and 
                    classifer labels and 0 = no match between labels
    """
        
              


def adjust_results4_isadog(result_dic, dogsfile):
    dog_name_dic = dict()
                  
    with open(dogsfile, "r") as infile:
        line = infile.readline()
                        
        while line != "":
            line = line.rstrip()
            if line not in dog_name_dic:
                dog_name_dic[line] = 1
            else:
                print("# Warning : Duplicate dog names ")
                  
            line = infile.readline()
                  
                  
    for key in result_dic:
        if result_dic[key][0] in dog_name_dic:
            if result_dic[key][1] in dog_name_dic:
                result_dic[key].extend((1,1))
            else:
                result_dic[key].extend((1,0))
                  
        else:
            if result_dic[key][1] in dog_name_dic:
                result_dic[key].extend((0,1))
            else:
                result_dic[key].extend((0,0))
                            
                    
                  
                  
    """
    Adjusts the results dictionary to determine if classifier correctly 
    classified images 'as a dog' or 'not a dog' especially when not a match. 
    Demonstrates if model architecture correctly classifies dog images even if
    it gets dog breed wrong (not a match).
    Parameters:
      results_dic - Dictionary with key as image filename and value as a List 
             (index)idx 0 = pet image label (string)
                    idx 1 = classifier label (string)
                    idx 2 = 1/0 (int)  where 1 = match between pet image and 
                            classifer labels and 0 = no match between labels
                    --- where idx 3 & idx 4 are added by this function ---
                    idx 3 = 1/0 (int)  where 1 = pet image 'is-a' dog and 
                            0 = pet Image 'is-NOT-a' dog. 
                    idx 4 = 1/0 (int)  where 1 = Classifier classifies image 
                            'as-a' dog and 0 = Classifier classifies image  
                            'as-NOT-a' dog.
     dogsfile - A text file that contains names of all dogs from ImageNet 
                1000 labels (used by classifier model) and dog names from
                the pet image files. This file has one dog name per line
                dog names are all in lowercase with spaces separating the 
                distinct words of the dogname. This file should have been
                passed in as a command line argument. (string - indicates 
                text file's name)
    Returns:
           None - results_dic is mutable data type so no return needed.
    """           
    


def calculates_results_stats(results_dic):
    results_stats = dict()
    
    results_stats["n_dogs_img"] = 0
    results_stats["n_match"]=0
    results_stats["n_correct_dogs"]=0
    results_stats["n_correct_notdogs"]=0
    results_stats["n_correct_breed"]=0
    
    for key in results_dic:
        if results_dic[key][2] == 1:
            results_stats["n_match"] += 1
        
        if sum(results_dic[key][2:]) == 2:
            results_stats["n_correct_breed"] += 1
            
        if results_dic[key][3] == 1:
            results_stats["n_dogs_img"] += 1
            
            if results_dic[key][4] == 1:
                results_stats["n_correct_dogs"] += 1
                
        else:
            if results_dic[key][4] == 0:
                results_stats["n_correct_notdogs"] += 1
       
    
    results_stats["n_images"] = len(results_dic)
    
    results_stats["n_notdogs_img"] = (results_stats["n_images"] - results_stats["n_dogs_img"])
    
    results_stats["pct_match"] = (results_stats["n_match"]/results_stats["n_images"]) * 100
    
    results_stats["pct_correct_dogs"] = (results_stats["n_correct_breed"]/results_stats["n_dogs_img"]) * 100
    
    if results_stats["n_notdogs_img"] > 0:
        results_stats["pct_correct_notdogs"] = (results_stats["n_correct_notdogs"] / results_stats["n_notdogs_img"])*100
        
    else:
        results_stats["pct_correct_notdogs"] = 0.0;
        
    return results_stats
        
            
    
    """
    Calculates statistics of the results of the run using classifier's model 
    architecture on classifying images. Then puts the results statistics in a 
    dictionary (results_stats) so that it's returned for printing as to help
    the user to determine the 'best' model for classifying images. Note that 
    the statistics calculated as the results are either percentages or counts.
    Parameters:
      results_dic - Dictionary with key as image filename and value as a List 
             (index)idx 0 = pet image label (string)
                    idx 1 = classifier label (string)
                    idx 2 = 1/0 (int)  where 1 = match between pet image and 
                            classifer labels and 0 = no match between labels
                    idx 3 = 1/0 (int)  where 1 = pet image 'is-a' dog and 
                            0 = pet Image 'is-NOT-a' dog. 
                    idx 4 = 1/0 (int)  where 1 = Classifier classifies image 
                            'as-a' dog and 0 = Classifier classifies image  
                            'as-NOT-a' dog.
    Returns:
     results_stats - Dictionary that contains the results statistics (either a
                     percentage or a count) where the key is the statistic's 
                     name (starting with 'pct' for percentage or 'n' for count)
                     and the value is the statistic's value 
    """
    


def print_results(results_dic, results_stats, model, print_incorrect_dogs = False, print_incorrect_breeds = False):
    print("\n\n*** Results Summary for CNN Model Architecture", model.upper(), "***")
    print("%20s: %3d" % ("N Images", results_stats["n_images"]))
    print("%20s: %3d" % ("N Dog Images", results_stats["n_dogs_img"]))
    print("%20s: %3d" % ("N Not-Dog Images", results_stats["n_notdogs_img"]))
    
    
    print("   ")
    for key in results_stats:
        if key[0] == "p":
            print("%20s: %5.1f" % (key, results_stats[key]))
            
    
    if (print_incorrect_dogs and ((results_stats["n_correct_dogs"] + results_stats["n_correct_notdogs"]) != results_stats["n_images"])):
        print("\n Correct Dog/Not Dog assignment")
        
        for key in results_dic:
            if sum(results_dic[key][3:]) == 1:
                print("Real: %-26s Classifier: %-30s" % (results_dic[key][0], results_dic[key][1]))
    
    if (print_incorrect_breeds and (results_stats["n_correct_dogs"] != results_stats["n_correct_breed"])):
        print("\n Incorrect dog breed assignment")
        
        for key in results_dic:
            if(sum(results_dic[key][3:]) == 2 and results[key][2] == 0):
                print("Real: %-26s            Classifier: %-30s" % (results_dic[key][0], results_dic[key][1]))
               
               
    """
    Prints summary results on the classification and then prints incorrectly 
    classified dogs and incorrectly classified dog breeds if user indicates 
    they want those printouts (use non-default values)
    Parameters:
      results_dic - Dictionary with key as image filename and value as a List 
             (index)idx 0 = pet image label (string)
                    idx 1 = classifier label (string)
                    idx 2 = 1/0 (int)  where 1 = match between pet image and 
                            classifer labels and 0 = no match between labels
                    idx 3 = 1/0 (int)  where 1 = pet image 'is-a' dog and 
                            0 = pet Image 'is-NOT-a' dog. 
                    idx 4 = 1/0 (int)  where 1 = Classifier classifies image 
                            'as-a' dog and 0 = Classifier classifies image  
                            'as-NOT-a' dog.
      results_stats - Dictionary that contains the results statistics (either a
                     percentage or a count) where the key is the statistic's 
                     name (starting with 'pct' for percentage or 'n' for count)
                     and the value is the statistic's value 
      model - pretrained CNN whose architecture is indicated by this parameter,
              values must be: resnet alexnet vgg (string)
      print_incorrect_dogs - True prints incorrectly classified dog images and 
                             False doesn't print anything(default) (bool)  
      print_incorrect_breed - True prints incorrectly classified dog breeds and 
                              False doesn't print anything(default) (bool) 
    Returns:
           None - simply printing results.
    """    
    

                
                
# Call to main function to run the program
if __name__ == "__main__":
    main()
