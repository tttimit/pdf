from reportlab.pdfgen import canvas
from HeadDarw import *

c = canvas.Canvas("out.pdf")
print(c.getAvailableFonts())

draw_head(c, "resources\\images\\dept-of-home-affairs.png", "Notification of changes in circumstances",
          '(Section 104 of the Migration Act 1958)', "1022")

draw_remind(c)

draw_content_title(c, "Your details")





c.showPage()
c.save()
