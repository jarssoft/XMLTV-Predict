import cairo 

def addProgram(context, wd, start, stop, text):
    start-=6*60
    stop-=6*60
    pat = cairo.LinearGradient(0.0, 0.0, 0.0, 1.0)
    pat.add_color_stop_rgba(1, 0.7, 0, 0, 1)  # First stop, 50% opacity
    pat.add_color_stop_rgba(0, 0.9, 0.7, 0.2, 1)  # Last stop, 100% opacity
    context.rectangle(wd*100, start/(24*60)*700, 100, (stop-start)/(24*60)*700-1) 
    context.set_source(pat)
    context.fill()

    #https://github.com/pygobject/pycairo/blob/main/examples/cairo_snippets/snippets/text.py
    if(stop-start>=10):
        xbearing, ybearing, width, height, dx, dy = context.text_extents(text)

        context.set_source_rgba(0, 0, 0, 1) 
        context.select_font_face("Sans", cairo.FONT_SLANT_NORMAL)
        context.move_to(wd*100, start/(24*60)*700+height)
        context.show_text(text)

# creating a SVG surface 
# here geek is file name & 700, 700 is dimension 
with cairo.SVGSurface("geek.svg", 700, 700) as surface: 
  
    # creating a cairo context object 
    context = cairo.Context(surface) 
  
    # creating a rectangle(square) for left eye 
    addProgram(context, 0, 13*60+10, 13*60+ 5, "Yle Uutiset")
    addProgram(context, 4, 20*60+00, 20*60+29, "Rahusen punatäh.")
    addProgram(context, 4, 20*60+29, 20*60+51, "Yle Uutiset")
    addProgram(context, 4, 20*60+51, 21*60+00, "Urheiluruutu")
    addProgram(context, 4, 21*60+00, 22*60+00, "Presidentinvaalit")

    context.scale(700, 700)  

    context.set_source_rgb(0, 0, 0)
    context.set_line_width(0.01)
    context.stroke()
  
# printing message when file is saved 
print("File Saved") 
