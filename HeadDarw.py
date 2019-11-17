from reportlab.pdfgen.canvas import Canvas
from PIL import Image
from reportlab.lib.units import inch
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import reportlab

BORDER_MARGIN = 22.067
RIGHT_MARGIN = 22.067
PAGE_WIDTH = 595.27
PAGE_HEIGHT = 841.89
DEFAULT_X_SCALE = 0.72
DEFAULT_Y_SCALE = 0.9
CONTENT_LEFT_MARGIN = 42.520

TTFSearchPath = (
    'c:/winnt/fonts',
    'c:/windows/fonts',
    '/usr/lib/X11/fonts/TrueType/',
    '/usr/share/fonts/truetype',
    '/usr/share/fonts',  # Linux, Fedora
    '/usr/share/fonts/dejavu',  # Linux, Fedora
    '%(REPORTLAB_DIR)s/fonts',  # special
    '%(REPORTLAB_DIR)s/../fonts',  # special
    '%(REPORTLAB_DIR)s/../../fonts',  # special
    '%(CWD)s/fonts',  # special
    '~/fonts',
    '~/.fonts',
    '%(XDG_DATA_HOME)s/fonts',
    '~/.local/share/fonts',
    # mac os X - from
    # http://developer.apple.com/technotes/tn/tn2024.html
    '~/Library/Fonts',
    '/Library/Fonts',
    '/Network/Library/Fonts',
    '/System/Library/Fonts',
    '.',
)


# A4 = (210*mm,297*mm)


def draw_logo(canvas, logo):
    """
    绘制表格左上角的Logo，尺寸为 (4.32 mm)*(2.61 mm)
    :param canvas:
    :param logo: logo图片的地址
    :return:
    """
    move_to_left_top(canvas)
    draw_width, draw_height = 118, 74
    position_x, position_y = BORDER_MARGIN, - (draw_height + BORDER_MARGIN)
    canvas.drawImage(logo, position_x, position_y, draw_width, draw_height, mask='auto')


def move_to_left_top(canvas):
    canvas.transform(1, 0, 0, 1, 0, PAGE_HEIGHT)


def init_font(canvas):
    """
        # TODO 注册需要的字体
        # reportlab.rl_config.TTFSearchPath.append(str())
        # print(canvas.getAvailableFonts())
        # pdfmetrics.registerFont(TTFont('HelveticaNeue Bold', 'HelveticaNeue Bold.ttf'))
        # pdfmetrics.registerFont(TTFont('HelveticaNeue Light', 'HelveticaNeue Light.ttf'))
    """
    pass


def draw_Title(canvas, title, sub_title):
    """
    1、计算title的宽度，来确定放置的位置
    2、计算副标题的宽度，注意后半部分字体是斜体，但是最后的括号不是

    'Helvetica', 'Helvetica-Bold', 'Helvetica-Oblique', 'Helvetica-BoldOblique',
    标准、标准加粗、倾斜、加粗倾斜

    canvas.stringWidth

    | 189----260-----149|
    主标题：字体 HelveticaNeue， 大小 18.960 加粗
    副标题（法案）：字体：HelveticaNeue， 大小 15.834 light
    :param title:例如 Notification of changes in circumstances
    :param sub_title: (Section 104 of the Migration Act 1958)    Migration Act 1958要用斜体
    :return:
    """
    width = canvas.stringWidth(title, fontName="Helvetica-Bold", fontSize=18.960)
    width_needed = DEFAULT_X_SCALE * width
    print("width needed={0}".format(width_needed))

    x1 = PAGE_HEIGHT / 2 - width_needed / 2 - 30
    y1 = - 68

    canvas.saveState()
    canvas.setFont("Helvetica-Bold", 18.960)
    canvas.scale(DEFAULT_X_SCALE, DEFAULT_Y_SCALE)
    canvas.drawString(x1, y1, title)
    canvas.restoreState()

    canvas.saveState()
    canvas.setFont("Helvetica", 15.834)
    x2 = x1 + width / 2 - canvas.stringWidth(sub_title, fontName="Helvetica", fontSize=15.834) / 2
    y2 = y1 - 20
    canvas.scale(DEFAULT_X_SCALE, DEFAULT_Y_SCALE)
    canvas.drawString(x2, y2, sub_title)
    canvas.restoreState()


def draw_form_number(canvas, form_number):
    """
    绘制右侧的表格代号

    canvas.drawRect(x, y, width, height, stroke=1, fill=0)
    From: 字体：HelveticaNeue-MediumCond 字号：10.503 第一个字母位置：bbox="521.120,792.415,525.287,802.918"
    1022：字体：HelveticaNeue-MediumCond 字号：32.676 第一个数字位置：bbox="503.199,761.071,516.639,793.747"

    :param form_number: 字符串 1022
    :return:
    """

    box_center_x = (556.959 - 503.199) / 2 + 503.199  # 根据1022字符的起始位置和结束位置获取

    box_length = (PAGE_WIDTH - box_center_x - BORDER_MARGIN) * 2

    distance_2_right_border = PAGE_WIDTH - box_center_x

    box_center_y = - distance_2_right_border

    x0 = box_center_x - box_length / 2
    y0 = box_center_y - box_length / 2

    canvas.rect(x0, y0, box_length, box_length)

    form_x = 521.120
    form_y = 792.415 - PAGE_HEIGHT

    canvas.saveState()
    canvas.setFont("Helvetica", 10.503)
    # canvas.scale(DEFAULT_X_SCALE, DEFAULT_Y_SCALE)
    canvas.drawString(form_x, form_y, "Form")
    canvas.restoreState()

    number_x = 503.199
    number_y = 761.071 - PAGE_HEIGHT

    canvas.saveState()
    canvas.setFont("Helvetica-Bold", 32.676)
    canvas.scale(0.72, 0.8)
    canvas.drawString(number_x / 0.72, number_y / 0.8, form_number)
    canvas.restoreState()


def draw_sep_line(canvas):
    """
    canvas.line(x1, y1, x2, y2)
    绘制分隔线
    根据下方的 Please open this form 字符串的高度来计算这条线的高度
    42.520,707.931,47.080,718.676
    :return:
    """

    canvas.setStrokeColorRGB(0, 0, 0)
    x1 = BORDER_MARGIN
    x2 = PAGE_WIDTH - BORDER_MARGIN
    y1 = y2 = (718.676 + 5) - PAGE_HEIGHT
    canvas.line(x1, y1, x2, y2)


def draw_remind(canvas):
    """
    绘制提醒信息
    Please open this form using Adobe Acrobat Reader.
    Either type(in English) in the fields provided or print this form
    and complete it(in English) using pen and BLOCK LETTERS.
    Tick where applicable 框✔
    第一行开始
    HelveticaNeue-LightCond" bbox="42.520,707.931,47.080,718.676" size="10.745">P</text>
    第二行开始
    HelveticaNeue-LightCond" bbox="42.520,696.531,46.738,707.276" size="10.745">E</text>

    第四行
    HelveticaNeue-LightCond" bbox="42.520,669.057,46.738,679.802" size="10.745">T</text>

    最后一个字母结束的位置，来控制checkbox的位置
    bbox="111.119,669.057,115.166,679.802" size="10.745">e
    :param canvas:
    :return:
    """
    text_line1 = "Please open this form using Adobe Acrobat Reader."
    text_line2 = "Either type(in English) in the fields provided or print this form"
    text_line3 = "and complete it(in English) using pen and BLOCK LETTERS."
    text_line4 = "Tick where applicable "
    x1, y1 = 45.52, 707.931 - PAGE_HEIGHT
    line_margin = 707.931 - 696.531
    canvas.saveState()
    canvas.setFont("Helvetica", 10.745)
    canvas.scale(0.72, 1)
    canvas.drawString(x1, y1, text_line1)
    canvas.drawString(x1, y1 - line_margin, text_line2)
    canvas.drawString(x1, y1 - 2 * line_margin, text_line3)
    canvas.drawString(x1, y1 - 3 * line_margin - 6, text_line4)
    canvas.restoreState()

    canvas.saveState()
    canvas.scale(0.72, 0.75)
    checkbox_width = 15
    checkbox_x = 115.166 + 40
    checkbox_y = (669.057 - 4 - PAGE_HEIGHT) / 0.75
    canvas.drawImage("resources\\images\\remind_check.png", checkbox_x, checkbox_y, checkbox_width, checkbox_width, mask='auto')
    canvas.restoreState()


def draw_content_title(canvas, title):
    """
    绘制表格内容体中的标题

    GaramondITCbyBT-BookCondItalic" bbox="42.520,631.946,49.448,650.218" size="18.272">Y</text>
    :param canvas:
    :param title:
    :return:
    """
    x = CONTENT_LEFT_MARGIN
    y = 631.946 - PAGE_HEIGHT
    canvas.saveState()
    canvas.translate(x, y)
    canvas.setFont("Courier-Oblique", 18.272)
    canvas.scale(0.72, 1)
    canvas.drawString(0, 0, title)
    canvas.restoreState()


def draw_head(canvas, logo, title, sub_title, form_number):
    """
    绘制表格头，包含LOGO，标题，副标题，表格编号，分隔线
    :param canvas:
    :param logo:
    :param title:
    :param sub_title:
    :param form_number:
    :return:
    """
    draw_logo(canvas, logo)
    init_font(canvas)
    draw_Title(canvas, title, sub_title)
    draw_form_number(canvas, form_number)
    print(canvas.absolutePosition(0, 0))
    draw_sep_line(canvas)