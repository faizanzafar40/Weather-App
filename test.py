import requests
import tkinter as tk
import io
from PIL import ImageTk, Image
import urllib3
import urllib.request 
import urllib
from tkinter.messagebox import showinfo


root = tk.Tk()

root.title("Simple Weather App")
root.resizable(0, 0)
root.wm_attributes('-topmost', 1)
root.geometry("350x200")

window_info = tk.StringVar()

main_weather = tk.Message(root, textvariable=window_info, width=200)
window_info.set("Your weather right now?")
main_weather.grid(row=1, column=1)

image_address = 'http://openweathermap.org/img/w/13n.png'
f = open('default.jpg','wb')
f.write(requests.get(image_address).content)
f.close()
path = 'default.jpg'
image_png = Image.open(path)
image_tk = ImageTk.PhotoImage(image_png.convert("RGB"))
label_img = tk.Label(root,image=image_tk)
label_img.grid(row=1, column=2)


def get_weather():
    
    api_address = 'http://api.openweathermap.org/data/2.5/weather?appid=8cc06465ffba9e86e4ba55347a804264&units=imperial&zip='
    country_code = ',de'
    post_code = e.get()

    url = api_address + post_code + country_code
    json_data = requests.get(url).json()

    if 'message' in json_data:

        window_info.set('Sorry, invalid post code :(')

    else:

        city = json_data['name']
        description = json_data['weather'][0]['description']
        icon = json_data['weather'][0]['icon']
        temperature = str(json_data['main']['temp']) + u'\u00b0' + " F"

        window_info.set(city + "\n" + description + "\n" + temperature)

        image_main = 'http://openweathermap.org/img/w/'
        image_address = image_main + str(icon) + '.png'
        
        f = open('current_weather.jpg','wb')
        f.write(requests.get(image_address).content)
        f.close()
        
        path = 'current_weather.jpg'
        image_png = Image.open(path)
        image_tk2 = ImageTk.PhotoImage(image_png.convert("RGB"))
        label_img.configure(image=image_tk2)
        label_img.image = image_tk2


label = tk.Label(root, text='Enter your postal code to find out\ne.g. 52062')
label.grid(row=3, column=1, sticky='E')



e = tk.Entry(root)
e.grid(row=3, column=2, pady=10)
e.bind("<Return>", (lambda event: get_weather()))

sub = tk.Button(root, text='Go!', command=(lambda: get_weather()))
sub.grid(row=4, column=2)

label1 = tk.Label(root, text='PS: I\'ve built this app to work for Germany only for now!')
label1.grid(column=1, columnspan=2, pady=20)

root.mainloop()