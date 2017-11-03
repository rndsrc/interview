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

def Tabs(obj):
    """Convert a nested (ordered) dictionary to a Bokeh tabs widget

    Args:
        obj: a nested (ordered) dictionary where the keys are tab
            titles and the values are children of panels

    Returns:
        An instance of Bokeh Tabs

    Examples:
        >>> import bokeh.plotting as bp
        >>> import interview as iv
        >>> fig = bp.figure()
        >>> bp.show(iv.widget.Tabs({'title':fig}))
    """
    import bokeh.plotting       as bp
    import bokeh.models.widgets as bw

    if   isinstance(obj, bp.Figure):
        return obj
    elif isinstance(obj, dict):
        return bw.Tabs(tabs=[bw.Panel(child=Tabs(v), title=k)
                             for k, v in obj.items()])
    else:
        raise ValueError("Input must be a dictionary or a Bokeh figure")
