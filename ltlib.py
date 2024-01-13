import drawlongterm
import cairo 

class LongTerm:
  def __init__(self, filename):
    self.surface = cairo.SVGSurface(filename, 740, 700)
    self.context = cairo.Context(self.surface)
    drawlongterm.drawBackGround(self.context)

  def addProgram(self, weekday, start, stop, title):
    drawlongterm.addProgram(self.context, weekday, start, stop, title)

  def save(self):
    self.context.save()
    #snippet.draw_func(cr, 740, 700)
    self.context.restore()
    self.context.show_page()
    self.surface.finish()

lt = LongTerm("out.svg")
lt.addProgram(4, 20*60+00, 20*60+29, "Rahusen punatäh.")
lt.addProgram(4, 20*60+29, 20*60+51, "Yle Uutiset")
lt.addProgram(4, 20*60+51, 21*60+00, "Urheiluruutu")
lt.addProgram(4, 21*60+00, 22*60+00, "Presidentinvaalit")
lt.addProgram(5, 19*60+45, 20*60+29, "Midsomer Murders")
lt.addProgram(5, 20*60+29, 20*60+45, "Yle Uutiset")
lt.addProgram(5, 20*60+45, 21*60+00, "Urheiluruutu")
lt.addProgram(5, 21*60+00, 22*60+15, "Hengaillaan")
lt.save()