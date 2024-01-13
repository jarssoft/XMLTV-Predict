import cairo 

margin=40

def getY(minute):
    return minute/(24*60)*700

def addAxis(context, time, text):
    time-=6*60

    context.set_line_width(0.12)
    context.set_line_cap(cairo.LINE_CAP_BUTT)
    context.move_to(margin, getY(time))
    context.line_to(700+margin, getY(time))
    context.stroke()

    xbearing, ybearing, width, height, dx, dy = context.text_extents(text)
    context.set_source_rgba(0, 0, 0, 1) 
    context.select_font_face("Sans", cairo.FONT_SLANT_NORMAL)
    context.move_to(10, getY(time)+height/2)
    context.show_text(text)    

def drawBackGround(context):
    # Set a background color
    context.save()
    context.set_source_rgb(0.3, 0.3, 1.0)
    context.paint()
    context.restore()
    
    for y in range(6, 24+6):
        addAxis(context, y*60, str(y%24))


def addProgram(context, wd, start, stop, text):
    start-=6*60
    stop-=6*60
    pat = cairo.LinearGradient(0.0, 0.0, 0.0, 1.0)
    pat.add_color_stop_rgba(1, 0.7, 0.7, 0, 1)  # First stop, 50% opacity
    pat.add_color_stop_rgba(0, 0.9, 0.7, 0.2, 1)  # Last stop, 100% opacity
    context.rectangle(wd*100+margin, getY(start), 95, getY(stop-start-1)) 
    context.set_source(pat)
    context.fill()

    #https://github.com/pygobject/pycairo/blob/main/examples/cairo_snippets/snippets/text.py
    if(stop-start>=10):
        xbearing, ybearing, width, height, dx, dy = context.text_extents(text)

        context.set_source_rgba(0, 0, 0, 1) 
        context.select_font_face("Sans", cairo.FONT_SLANT_NORMAL)
        context.move_to(wd*100+margin, getY(start)+height)
        context.show_text(text)
