import ltdraw
import cairo 
import xmltvtime

class LongTerm:
  def __init__(self, filename):
    self.surface = cairo.SVGSurface(filename, 740, 700)
    self.context = cairo.Context(self.surface)
    ltdraw.drawBackGround(self.context)

  def addProgram(self, start, stop, title, correct):
    minstart=xmltvtime.hour(start)*60+xmltvtime.minute(start)
    minstop=xmltvtime.hour(stop)*60+xmltvtime.minute(stop)
    day=xmltvtime.day(start)-21
    print(minstart, minstop)
    ltdraw.addProgram(self.context, day, minstart, minstop, title, correct)

  def save(self):
    self.context.save()
    #snippet.draw_func(cr, 740, 700)
    self.context.restore()
    self.context.show_page()
    self.surface.finish()

"""
lt = LongTerm("out.svg")
lt.addProgram("20040112200000", "20040112202900", "Rahusen punatäh.")
lt.addProgram("20040112202900", "20040112205100", "Yle Uutiset")
lt.addProgram("20040112205100", "20040112210000", "Urheiluruutu")
lt.addProgram("20040112210000", "20040112220000", "Presidentinvaalit")
lt.addProgram("20040113194500", "20040113202900", "Midsomer Murders")
lt.addProgram("20040113202900", "20040113204500", "Yle Uutiset")
lt.addProgram("20040113204500", "20040113210000", "Urheiluruutu")
lt.addProgram("20040113210000", "20040113221500", "Hengaillaan")
lt.save()"""