import drawlongterm
import cairo 

def draw():

    filename = "out.svg"
    surface = cairo.SVGSurface(filename, 740, 700)
    context = cairo.Context(surface)

    drawlongterm.drawBackGround(context)

    drawlongterm.addProgram(context, 4, 20*60+00, 20*60+29, "Rahusen punatäh.")
    drawlongterm.addProgram(context, 4, 20*60+29, 20*60+51, "Yle Uutiset")
    drawlongterm.addProgram(context, 4, 20*60+51, 21*60+00, "Urheiluruutu")
    drawlongterm.addProgram(context, 4, 21*60+00, 22*60+00, "Presidentinvaalit")
    
    drawlongterm.addProgram(context, 5, 19*60+45, 20*60+29, "Midsomer Murders")
    drawlongterm.addProgram(context, 5, 20*60+29, 20*60+45, "Yle Uutiset")
    drawlongterm.addProgram(context, 5, 20*60+45, 21*60+00, "Urheiluruutu")
    drawlongterm.addProgram(context, 5, 21*60+00, 22*60+15, "Hengaillaan")

    context.save()
    #snippet.draw_func(cr, 740, 700)
    context.restore()
    context.show_page()
    surface.finish()

draw()