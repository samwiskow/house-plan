from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).parent
OUTPUT = ROOT / 'output/pdf/two-storey-linked-pavilion-option.pdf'
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
pdfmetrics.registerFont(TTFont('PlanArial', '/System/Library/Fonts/Supplemental/Arial.ttf'))
pdfmetrics.registerFont(TTFont('PlanArialBold', '/System/Library/Fonts/Supplemental/Arial Bold.ttf'))

WIDTH, HEIGHT = 420, 297
COLORS = {
    'ink': '#25332c', 'muted': '#58665e', 'line': '#bcc8bf',
    'room': '#efeeea', 'family': '#e6ede8', 'shared': '#f4eadb',
    'work': '#e2ebef', 'garden': '#e5eedf', 'glass': '#edf3f0',
    'paper': '#ffffff', 'route': '#267d83', 'furniture': '#d7d8d0',
}
c = canvas.Canvas(str(OUTPUT), pagesize=(WIDTH * mm, HEIGHT * mm))
c.setTitle('Two-storey option C - linked work pavilion')
c.setAuthor('House plan working study')


def color(key):
    return HexColor(COLORS.get(key, key))


def text(x, y, value, size=3, bold=False, align='left', fill='ink'):
    c.setFillColor(color(fill))
    c.setFont('PlanArialBold' if bold else 'PlanArial', size * mm)
    draw = {'left': c.drawString, 'center': c.drawCentredString, 'right': c.drawRightString}[align]
    draw(x * mm, (HEIGHT - y) * mm, value)


def line(x1, y1, x2, y2, fill='line', weight=.25, dash=None):
    c.setStrokeColor(color(fill))
    c.setLineWidth(weight * mm)
    c.setDash(dash or [])
    c.line(x1 * mm, (HEIGHT - y1) * mm, x2 * mm, (HEIGHT - y2) * mm)
    c.setDash([])


def rect(x, y, w, h, fill=None, stroke='ink', dash=None):
    c.setLineWidth(.25 * mm)
    c.setDash(dash or [])
    if fill:
        c.setFillColor(color(fill))
    if stroke:
        c.setStrokeColor(color(stroke))
    c.rect(x * mm, (HEIGHT - y - h) * mm, w * mm, h * mm,
           fill=bool(fill), stroke=bool(stroke))
    c.setDash([])


def paragraph(x, y, lines, step=5.2, size=3):
    for value in lines:
        text(x, y, value, size)
        y += step


def header(number, title, subtitle):
    text(14, 12, 'TWO-STOREY OPTION C / CONNECTED WORK PAVILION', 2.7, fill='muted')
    text(14, 23, title, 6.6, bold=True)
    text(14, 31, subtitle, 3, fill='muted')
    line(14, 36, 406, 36)
    line(14, 281, 406, 281)
    text(14, 287, 'LOW-FIDELITY CONCEPT | Not to scale. No measured areas or construction details implied.', 2.6, fill='muted')
    text(406, 287, f'{number} / 2', 2.6, align='right', fill='muted')


class Diagram:
    def __init__(self, ox=19, oy=61, scale=10.7):
        self.ox, self.oy, self.scale = ox, oy, scale

    def xy(self, x, y):
        return self.ox + x * self.scale, self.oy + y * self.scale

    def label(self, x, y, lines, size=3):
        xx, yy = self.xy(x, y)
        for i, value in enumerate(lines):
            text(xx, yy + i * 4.2, value, size, align='center')

    def box(self, x, y, w, h, fill='room', lines=(), dashed=False):
        xx, yy = self.xy(x, y)
        rect(xx, yy, w * self.scale, h * self.scale,
             None if dashed else fill, 'muted' if dashed else 'ink', [1.5, 1] if dashed else None)
        if lines:
            self.label(x + w / 2, y + h / 2 - ((len(lines) - 1) * 2.1 - 1) / self.scale, lines)

    def gap(self, x, y, w, vertical=False):
        a = self.xy(x, y)
        b = self.xy(x + (0 if vertical else w), y + (w if vertical else 0))
        line(*a, *b, 'paper', 1.1)

    def route(self, points):
        for a, b in zip(points, points[1:]):
            line(*self.xy(*a), *self.xy(*b), 'route', .5, [1.6, 1])
        x, y = self.xy(*points[-1])
        line(x, y, x - 1.3, y + 2, 'route', .5)
        line(x, y, x + 1.3, y + 2, 'route', .5)

    def stairs(self, upper=False):
        self.box(3.5, 6, 2, 3, 'room')
        self.gap(4.05, 6, .9)
        self.gap(4.05, 9, .9)
        for i in range(7):
            y = 6.4 + i * .35
            line(*self.xy(3.6, y), *self.xy(5.4, y), 'muted', .12)
        x, y = self.xy(4.5, 7.5)
        c.saveState()
        c.translate(x * mm, (HEIGHT - y) * mm)
        c.rotate(90)
        c.setFillColor(color('ink'))
        c.setFont('PlanArial', 2.8 * mm)
        c.drawCentredString(0, 0, 'STAIRS DOWN' if upper else 'STAIRS UP')
        c.restoreState()


header(1, 'Home and work, with space between',
       'Ground floor | A two-storey main house and a single-storey office / gym pavilion linked across a garden gap')
d = Diagram()
d.label(5, -.9, ['MAIN HOUSE'], 3.1)
d.label(18, 4.2, ['WORK PAVILION'], 3.1)
d.box(10, 0, 5, 9, 'garden')
d.label(12.5, 6.1, ['Planted garden', 'between buildings'])
d.box(0, 0, 10, 5, 'shared', ['OPEN LIVING / DINING', 'Kitchen towards the service rooms'])
d.box(10, 2, 3, 3, 'glass', ['Small', 'orangery'])
d.gap(10, 3, .9, True)
d.box(0, 5, 3, 2.5, 'shared', ['Reading /', 'play snug'])
d.box(0, 7.5, 3, 3.5, 'family', ['Guest bedroom', '+ shower'])
d.box(3, 5, 3, 6, 'paper')
d.gap(3, 6, .8, True)
d.gap(3, 8.7, .8, True)
d.gap(4.1, 5, .8)
d.box(6, 5, 4, 4, 'room', ['SERVICE ROOM GROUP', 'Pantry / separate laundry', 'Boot room / visitor WC'])
d.box(6, 9, 4, 2, 'paper')
d.label(8, 9.65, ['Arrival hall'])
d.gap(6, 9.4, 1.1, True)
d.gap(8.2, 9, .8)
d.gap(8, 5, .8)
d.gap(7.5, 11, 1)
d.box(10, 9, 5, 2, 'glass')
d.label(12.5, 8.55, ['Enclosed garden passage'], 2.8)
d.gap(10, 9.55, 1, True)
d.box(15, 5, 6, 4, 'work', ['OFFICE / GAMING', 'No bedrooms above or beside'])
d.box(15, 9, 6, 2, 'paper')
d.box(18, 9, 3, .65, 'room', ['Storage'])
d.label(18.5, 10.45, ['Lobby'], 2.8)
d.box(15, 11, 6, 4, 'room', ['GYM', 'Separate door from lobby'])
d.gap(15, 9.55, 1, True)
d.gap(16.1, 9, .9)
d.gap(16.1, 11, .9)
d.route([(8, 10.65), (8, 10.1), (16.55, 10.1), (16.55, 8.6)])
d.stairs()
d.box(0, 12.5, 6, 3.5, lines=['Solar carport', '2 household cars'], dashed=True)
d.box(6.7, 12.5, 3.3, 3.5, lines=['Guest car'], dashed=True)
d.label(5, 11.85, ['ARRIVAL / PARKING SIDE'], 2.7)

text(260, 55, 'The organising idea', 4, bold=True)
paragraph(260, 65, [
    'All bedrooms belong to the main house.',
    'The office sits in its own low pavilion,',
    'across an open garden gap.',
    '',
    'A short enclosed passage gives an indoor',
    'route from arrival hall to office. It avoids',
    'the bedroom stairs and main living room.',
    '',
    'Office and gym have separate lobby doors.',
    'Storage and circulation sit between them.'
])
text(260, 126, 'Ground-floor programme retained', 4, bold=True)
paragraph(260, 136, [
    'Generous shared kitchen / dining / living.',
    'Guest bedroom with a nearby shower.',
    'Reading / play snug and small orangery.',
    'Pantry, separate laundry, boot room and WC.',
    'Dedicated office and indoor-connected gym.',
    'Two covered household bays plus a guest bay.'
])
text(260, 177, 'What changes from the U', 4, bold=True)
paragraph(260, 187, [
    'An offset pair of buildings creates a garden',
    'pocket instead of the original formal U.',
    'The orangery opens from shared living;',
    'it is separate from the work passage.',
    '',
    'The passage adds circulation and external',
    'wall area. Footprint savings are not assumed.'
])
line(19, 246, 243, 246)
line(20, 254, 35, 254, 'route', .5, [1.6, 1])
text(40, 255, 'Route from arrival to office', 3)
paragraph(19, 266, ['Openings show intended connections. Service rooms and stairs are reserved',
                    'as groups; their detailed subdivisions and clearances are not yet fitted.'], size=2.8)
c.showPage()

header(2, 'Family upstairs; work stays apart',
       'Upper floor | Bedrooms occupy the main house only | Same diagram coordinates and stair position as the ground floor')
d = Diagram()
d.label(5, -.9, ['FAMILY SLEEPING FLOOR'], 3.1)
d.box(10, 0, 5, 9, 'garden')
d.label(12.5, 6.1, ['Open garden', 'below'])
d.box(10, 2, 3, 3, lines=['Orangery', 'roof below'], dashed=True)
d.box(10, 9, 5, 2, lines=['Low passage roof'], dashed=True)
d.box(15, 5, 6, 10, dashed=True)
d.label(18, 8.1, ['OFFICE / GYM', 'ROOF BELOW'], 3.1)
d.label(18, 11.25, ['No upper floor', 'over the work pavilion'])
d.box(0, 0, 10, 11, 'paper')
d.box(0, 0, 5, 5, 'family', ['PARENTS', 'Bedroom + walk-in wardrobe', '+ ensuite'])
for i in range(3):
    d.box(6, i * 3, 4, 3, 'family', [f'CHILD {i + 1}'])
    d.gap(6, i * 3 + 1, .8, True)
d.box(0, 5, 3, 3, 'room', ['Family', 'bathroom'])
d.box(0, 8, 3, 3, 'room', ['Linen /', 'storage'])
d.box(6, 9, 4, 2, 'paper', ['Landing'])
d.gap(6, 9.5, 1, True)
d.gap(5, 2, .8, True)
d.gap(3, 6.1, .8, True)
d.gap(3, 9.1, .8, True)
d.stairs(upper=True)
d.label(5.5, 4.6, ['Hall'], 2.4)

text(260, 55, 'Separation in three dimensions', 4, bold=True)
paragraph(260, 65, [
    'Parents and all three children share a floor.',
    'The family bathroom serves the children;',
    'parents retain their own ensuite and wardrobe.',
    '',
    'The ground-floor guest room also stays in',
    'the main house, away from the work pavilion.',
    'No bedroom shares a wall or floor with',
    'the office or gym.'
])
text(260, 118, 'Architectural direction', 4, bold=True)
paragraph(260, 128, [
    'A taller family house with a low work wing',
    'and a light garden passage between them.',
    'Warm timber, pale masonry and planting',
    'could give the two forms a shared character.',
    '',
    'Roof form and window orientation remain open.',
    'Direct office views towards the side garden',
    'could help privacy from upstairs bedrooms.'
])
text(260, 181, 'Next design checks', 4, bold=True)
paragraph(260, 191, [
    'Fit the full room schedule and an actual stair.',
    'Test landings, access and furniture clearance.',
    'Resolve acoustic separation and gym vibration.',
    'Coordinate structural and service routes.',
    'Test sunlight, privacy and roof drainage on a site.',
    'Then compare total area and footprint with',
    'the single-storey concept 05.'
])
line(19, 246, 243, 246)
paragraph(19, 255, [
    'Dashed outlines are lower roofs, not upper rooms or roof terraces.',
    'This is a separate design option. The single-storey concept 05 remains',
    'the measured baseline; its geometry checks do not apply to this diagram.'
], size=2.8)
c.save()
print(OUTPUT)
