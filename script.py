# 

import argparse
import xml.etree.ElementTree as ET
import os

RESET = '\033[0m'
def get_color_escape(r, g, b, background=False):
    return '\033[{};2;{};{};{}m'.format(48 if background else 38, r, g, b)

def build_parser():
    parser = argparse.ArgumentParser(description='Input the target path, specify if it is a file or a folder, the output path and the method (show_colors|change_colors)')
    parser.add_argument('--path', type=str, help='Path to the target file', required=True)
    parser.add_argument('--pathType', type=str, help='Type of the target path (file|folder)', choices=['file', 'folder'], required=True)
    parser.add_argument('--output', type=str, help='Path to the output file', default='./')
    parser.add_argument('--method', type=str, help='Method to be used (show_colors|change_colors)', choices=['show_colors', 'change_colors'])
    parser.add_argument('--colors', type=str, help='List of colors to be changed, each couple sourceColor:targetColor must separated by commas', default=None)
    return parser

def make_dir_if_not_exists(path):
    import os
    if not os.path.exists(path):
        os.makedirs(path)
        
def show_colors(image):
    for block in image.iter():
        #Get both style and fill, just in case
        style = block.attrib.get('style')
        if style is None:
            continue
        fill = style.strip("style='fill: ")[:7]
        rgb = tuple(int(fill.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        print(get_color_escape(rgb[0], rgb[1], rgb[2], False) + fill + RESET)
        
def svg2xml(image):
    tree = ET.parse(image)
    root = tree.getroot()
    return root

def change_colors(image, sourceColor, targetColor):
    return image.replace('style="fill: {};'.format(sourceColor), 'style="fill: {};'.format(targetColor))

def check_file_exists(path):
    try:
        with open(path) as f:
            pass
    except IOError as e:
        return False
    return True

def __main__():
    parser = build_parser()
    args = parser.parse_args()
    #print arguments to test
    files = []
    #check if the path is folder
    if args.pathType == 'folder':
        #list all files in the folder
        files = os.listdir(args.path)
        #add the path to the file
        files = [args.path + '/' + file for file in files]
    else:
        files.append(args.path)
        
    for file in files:
        #Check if the file exists
        if not check_file_exists(file):
            print('File: {file} does not exist'.format(file=file))
            continue
        #Open the image
        if args.method == 'show_colors':
            image = svg2xml(file)
            show_colors(image)
        elif args.method == 'change_colors':
            if args.colors is None:
                print('Color list not provided')
                return
            else:
                with open(file, 'rt') as image:
                    image = image.read()
                    colorList = args.colors.split(',')
                    for color in colorList:
                        sourceColor, targetColor = color.split(':')
                        image = change_colors(image, sourceColor, targetColor)      
                    make_dir_if_not_exists(args.output)
                    with open(args.output + '/' + file.split('/')[-1] + '-' + targetColor, 'wt') as f:
                        f.write(image)
        else:
            print('Method not implemented')
            return
    
__main__()