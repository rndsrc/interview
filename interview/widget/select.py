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

def Select(ps, a, opts, backend="python"):
    """Create a selector with callback for plots "ps" with glyph attribute "a"

    Args:
        ps:      a list of plots
        a:       glyph attribute
        opts:    a dictionary where the keys are data source columns and
            values are selector labels.
        backend: choose callback backend; the only supported backend is
            "python"

    Returns:
        An instance of Bokeh Select

    Examples:
        >>> import interview as iv
        >>> ...
        >>> plt = fig.circle(...)
        >>> sel = iv.widget.Select(plt, 'x', opts)
    """
    import bokeh.models.widgets as bw

    if not isinstance(ps, list):
        ps = [ps]

    s = bw.Select(title  =a.upper()+" Axis",
                  options=list(opts.values()),
                  value  =opts[getattr(ps[0].glyph, a)])

    if backend == "python":
        def callback(attr, old, new):
            for p in ps:
                setattr(p.glyph, a,
                        list(opts.keys())[list(opts.values()).index(new)])
        s.on_change("value", callback)
    else:
        raise ValueError('the only supported backend is "python"')

    return s
