from __future__ import  absolute_import

from itertools import chain

from bokeh.models.annotations import Legend, Arrow, BoxAnnotation, Span, Label
from bokeh.models import ColumnDataSource
from bokeh.core.enums import (
    NamedColor as Color, LineJoin, LineCap, FontStyle, TextAlign,
    TextBaseline)

FILL = ["fill_color", "fill_alpha"]
LINE = ["line_color", "line_width", "line_alpha", "line_join", "line_cap",
        "line_dash", "line_dash_offset"]
TEXT = ["text_font", "text_font_size", "text_font_style", "text_color",
        "text_alpha", "text_align", "text_baseline"]
ANGLE = ["angle", "angle_units"]
PROPS = ["name", "tags"]

def prefix(prefix, props):
    return [prefix + p for p in props]

def check_props(annotation, *props):
    expected = set(chain(PROPS, *props))
    found = set(annotation.properties())
    missing = expected.difference(found)
    extra = found.difference(expected)
    assert len(missing) == 0, "Properties missing: {0}".format(", ".join(sorted(missing)))
    assert len(extra) == 0, "Extra properties: {0}".format(", ".join(sorted(extra)))

def check_fill(annotation, prefix="", fill_color='#ffffff', fill_alpha=1.0):
    assert getattr(annotation, prefix + "fill_color") == fill_color
    assert getattr(annotation, prefix + "fill_alpha") == fill_alpha

def check_line(annotation, prefix="", line_color=Color.black, line_width=1.0, line_alpha=1.0):
    assert getattr(annotation, prefix + "line_color") == line_color
    assert getattr(annotation, prefix + "line_width") == line_width
    assert getattr(annotation, prefix + "line_alpha") == line_alpha
    assert getattr(annotation, prefix + "line_join") == LineJoin.miter
    assert getattr(annotation, prefix + "line_cap") == LineCap.butt
    assert getattr(annotation, prefix + "line_dash") == []
    assert getattr(annotation, prefix + "line_dash_offset") == 0

def check_text(annotation, prefix="", font_size='12pt', baseline='bottom'):
    assert getattr(annotation, prefix + "text_font") == "helvetica"
    assert getattr(annotation, prefix + "text_font_size") == {"value": font_size}
    assert getattr(annotation, prefix + "text_font_style") == FontStyle.normal
    assert getattr(annotation, prefix + "text_color") == "#444444"
    assert getattr(annotation, prefix + "text_alpha") == 1.0
    assert getattr(annotation, prefix + "text_align") == TextAlign.left
    assert getattr(annotation, prefix + "text_baseline") == baseline

def test_Legend():
    legend = Legend()
    assert legend.plot is None
    assert legend.location == 'top_right'
    assert legend.label_standoff == 15
    assert legend.label_height == 20
    assert legend.label_width == 50
    assert legend.glyph_height == 20
    assert legend.glyph_width == 20
    assert legend.legend_padding == 10
    assert legend.legend_spacing == 3
    assert legend.legends == []
    yield check_line, legend, "border_"
    yield check_text, legend, "label_", "10pt", "middle"
    yield check_fill, legend, "background_"
    yield (check_props, legend, [
        "plot",
        "location",
        "orientation",
        "label_standoff",
        "label_height",
        "label_width",
        "glyph_height",
        "glyph_width",
        "legend_padding",
        "legend_spacing",
        "legends",
        "level"],
        prefix('label_', TEXT),
        prefix('border_', LINE),
        prefix('background_', FILL))

def test_Arrow():
    arrow = Arrow()
    assert arrow.plot is None
    assert arrow.tail_x is None
    assert arrow.tail_y is None
    assert arrow.head_x is None
    assert arrow.head_y is None
    assert arrow.head_size == 25
    assert arrow.tail_units == 'data'
    assert arrow.head_units == 'data'
    assert arrow.tail_style is None
    assert arrow.head_style == 'open'
    assert isinstance(arrow.source, ColumnDataSource)
    assert arrow.source.data == {}
    assert arrow.x_range_name == "default"
    assert arrow.y_range_name == "default"
    yield check_line, arrow, "body_"
    yield check_line, arrow, "tail_border_"
    yield check_line, arrow, "head_border_"
    yield check_fill, arrow, "tail_body_", "black"
    yield check_fill, arrow, "head_body_", "black"
    yield (check_props, arrow, [
        "plot",
        "level",
        "tail_x",
        "tail_y",
        "head_x",
        "head_y",
        "head_size",
        "tail_units",
        "head_units",
        "tail_style",
        "head_style",
        "source",
        "x_range_name",
        "y_range_name"],
        prefix('body_', LINE),
        prefix('tail_border_', LINE),
        prefix('head_border_', LINE),
        prefix('tail_body_', FILL),
        prefix('head_body_', FILL))

def test_BoxAnnotation():
    box = BoxAnnotation()
    assert box.plot is None
    assert box.left == None
    assert box.left_units == 'data'
    assert box.right == None
    assert box.right_units == 'data'
    assert box.bottom == None
    assert box.bottom_units == 'data'
    assert box.top == None
    assert box.top_units == 'data'
    assert box.x_range_name == 'default'
    assert box.y_range_name == 'default'
    assert box.level == 'annotation'
    yield check_line, box, "", '#cccccc', 1, 0.3
    yield check_fill, box, "", "#fff9ba", 0.4
    yield (check_props, box, [
        "render_mode",
        "plot",
        "left",
        "left_units",
        "right",
        "right_units",
        "bottom",
        "bottom_units",
        "top",
        "top_units",
        "x_range_name",
        "y_range_name",
        "level",
    ], LINE, FILL)

def test_Label():
    label = Label()
    assert label.plot is None
    assert label.level == 'annotation'
    assert label.x is None
    assert label.y is None
    assert label.x_units == 'data'
    assert label.y_units == 'data'
    assert label.text ==  'text'
    assert label.angle == 0
    assert label.x_offset == 0
    assert label.y_offset == 0
    assert label.render_mode == 'canvas'
    assert label.x_range_name == 'default'
    assert label.y_range_name == 'default'
    assert isinstance(label.source, ColumnDataSource)
    assert label.source.data == {}
    yield check_text, label
    yield check_fill, label, "background_", None, 1.0
    yield check_line, label, "border_", None, 1.0, 1.0
    yield (check_props, label, [
        "plot",
        "level",
        "x",
        "y",
        "x_units",
        "y_units",
        "text",
        "angle",
        "x_offset",
        "y_offset",
        "render_mode",
        "x_range_name",
        "y_range_name",
        "source"],
        TEXT,
        ANGLE,
        prefix('border_', LINE),
        prefix('background_', FILL))

def test_Span():
    line = Span()
    assert line.plot is None
    assert line.location is None
    assert line.location_units == 'data'
    assert line.dimension == 'width'
    assert line.x_range_name == 'default'
    assert line.y_range_name == 'default'
    assert line.level == 'annotation'
    assert line.render_mode == 'canvas'
    yield check_line, line, "", 'black', 1.0
    yield (check_props, line, [
        "plot",
        "location",
        "location_units",
        "dimension",
        "x_range_name",
        "y_range_name",
        "level",
        "render_mode"
    ], LINE)
