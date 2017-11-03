# Copyright (C) 2017 Chi-kwan Chan
# Copyright (C) 2017 Harvard-Smithsonian Center for Astrophysics
#
# This file is part of interview.
#
# Interview is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Interview is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with interview.  If not, see <http://www.gnu.org/licenses/>.

def Select(p, a, opts):
    """Create a selector with its callback

for plot "p" with glyph attribute "a"

    Args:
        p:    plot
        a:    glyph attribute
        opts: a dictionary where the keys are data source columns and
            values are selector labels.

    Returns:
        An instance of Bokeh Select

    Examples:
        >>> import interview as iv
        >>> ...
        >>> plt = fig.circle(...)
        >>> sel = iv.widget.Select(plt, 'x', opts)
    """
    import bokeh.models.widgets as bw

    s = bw.Select(title  =a.upper()+" Axis",
                  options=list(opts.values()),
                  value  =opts[getattr(p.glyph, a)])

    def callback(attr, old, new):
        setattr(p.glyph, a,
                list(opts.keys())[list(opts.values()).index(new)])
    s.on_change("value", callback)
    return s
