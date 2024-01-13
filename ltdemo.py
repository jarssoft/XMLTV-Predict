import drawlongterm
import cairo 

# creating a SVG surface 
# here geek is file name & 700, 700 is dimension 
with cairo.SVGSurface("geek.svg", 700+drawlongterm.margin, 700) as surface: 
  
    # creating a cairo context object 
    context = cairo.Context(surface) 

    drawlongterm.drawBackGround(context)

    # creating a rectangle(square) for left eye 
    drawlongterm.addProgram(context, 4, 20*60+00, 20*60+29, "Rahusen punatäh.")
    drawlongterm.addProgram(context, 4, 20*60+29, 20*60+51, "Yle Uutiset")
    drawlongterm.addProgram(context, 4, 20*60+51, 21*60+00, "Urheiluruutu")
    drawlongterm.addProgram(context, 4, 21*60+00, 22*60+00, "Presidentinvaalit")
    
    drawlongterm.addProgram(context, 5, 19*60+45, 20*60+29, "Midsomer Murders")
    drawlongterm.addProgram(context, 5, 20*60+29, 20*60+45, "Yle Uutiset")
    drawlongterm.addProgram(context, 5, 20*60+45, 21*60+00, "Urheiluruutu")
    drawlongterm.addProgram(context, 5, 21*60+00, 22*60+15, "Hengaillaan")


    context.scale(700, 700)  

    context.set_source_rgb(0, 0, 0)
    context.set_line_width(0.01)
    context.stroke()
  
# printing message when file is saved 
print("File Saved") 
