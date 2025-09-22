# Kian Spalla
# Sample NITELITE data pipeline
# A simple data pipeline that collects brightness data from night sky images
# and converts them into a histogram and CSV file.

#basic imports
import glob #file collection
import os #file paths
import numpy #array and math functions
import pandas #dataframe and csv
from PIL import Image #image handling
import matplotlib.pyplot as plt #plotting

#Collect images
image_files = (glob.glob("data/*.jpg") + glob.glob("data/*.jpeg") + glob.glob("data/*.png"))

#Check if images were found
if not image_files:
    print("No images found in the 'data' folder.")
    raise SystemExit

#Path to results folder
results_dir = "results"

#Create results folder if it doesnt exist
if not os.path.exists(results_dir):
    os.makedirs(results_dir)

#List to hold results for CSV
results = []

#Loop through images 
for image_path in image_files:
    #Open image and create array
    img = Image.open(image_path)
    arr = numpy.array(img)

    #Store basic stats about image
    minVal = numpy.min(arr)
    maxVal = numpy.max(arr)
    avgVal = round(numpy.mean(arr), 2)

    #Output on console (this isnt necessary)
    print(f"\nAnalyzing: {image_path}")
    print("Format:", img.format)
    print("Size (width, height):", img.size)
    print("Mode:", img.mode)
    print("Min:", minVal, "Max:", maxVal, "Avg:", avgVal)

    #Create and save histogram plot
    filename_only = os.path.splitext(os.path.basename(image_path))[0]
    hist_path = os.path.join(results_dir, f"{filename_only}_hist.png")

    plt.figure()
    plt.hist(arr.flatten(), bins=256)
    plt.xlabel("Pixel Value (0 = dark, 255 = bright)")
    plt.ylabel("Count")
    plt.title(f"Histogram for {filename_only}")
    plt.savefig(hist_path)
    plt.close()

    #Store results for CSV
    results.append({
        "filename": image_path,
        "format": img.format,
        "width": img.size[0],
        "height": img.size[1],
        "mode": img.mode,
        "min_pixel": minVal,
        "max_pixel": maxVal,
        "avg_pixel": avgVal
    })

#Save csv file in results folder
csv_path = os.path.join(results_dir, "image_results.csv")
df = pandas.DataFrame(results)
df.to_csv(csv_path, index=False)

print(f"\nResults saved to {csv_path}")
print(f"Histogram PNGs saved in {results_dir}/")