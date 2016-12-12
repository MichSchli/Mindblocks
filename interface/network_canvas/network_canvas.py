import imp

components = imp.load_source('graphics','components/component.py')
tmp_c = imp.load_source('constant','components/basic/network/constant.py')
tmp_o = imp.load_source('constant','components/basic/network/output.py')

abstract = imp.load_source('abstract','interface/drawable_canvas.py')

class NetworkCanvas(abstract.DrawableCanvas):

    available_components = [tmp_c.Constant(), tmp_o.Output()]
