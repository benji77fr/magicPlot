# -*- coding: utf-8 -*-


import pyqtgraph as pg
import numpy as np
import PyQt5
from PyQt5 import QtCore, QtWidgets, QtGui


def find_the_closest(sorted_list, key):
    ''' 
    Cherche dans une list, l'élément le plus proche en fonction de la clé
    '''

    if key in sorted_list:
        return key
    else:
        for cpt in range(len(sorted_list) - 1):
            if key > sorted_list[cpt] and key < sorted_list[cpt + 1]:
                if abs(sorted_list[cpt] - key) >= abs(
                        sorted_list[cpt + 1] - key):
                    return sorted_list[cpt + 1]
                else:
                    return sorted_list[cpt]

class Crosshair(pg.PlotItem):
    '''
    Class Crosshair

    PlotItem qui vient s'ajouter sur le graphique principale, affichant un repère synchronisé avec
    les mouvements de la souris dans le champs de vision du graphique.
    Permet de récupérer les coordonnées et d'obtenir les valeurs d'un point sur le graphique.

    :param
        plot: PlotItem contennant les données des courbes affichées
    '''
    def __init__(self, plot):
        super(Crosshair, self).__init__()

        self.data_list = []
        self.data_list_x_sorted = []
        self.plot = plot

        self.vline = pg.InfiniteLine(angle=90, movable=False, pen=pg.mkPen('w'))
        self.hline = pg.InfiniteLine(angle=0, movable=False, pen=pg.mkPen('w'))

        self.labelx = pg.TextItem(
            border=pg.mkPen('#ffaa55'),
            fill=pg.mkBrush(0, 0, 0, 210), anchor=(0.5, 1.0))
        self.labely = pg.TextItem(
            border=pg.mkPen('#ffaa55'),
            fill=pg.mkBrush(0, 0, 0, 210), anchor=(0.0, 0.5))
        
        self.label = pg.LabelItem(justify="right")
        
        self.plot.addItem(self.vline, ignoreBounds=True)
        self.plot.addItem(self.hline, ignoreBounds=True)
        self.plot.addItem(self.labelx, ignoreBounds=True)
        self.plot.addItem(self.labely, ignoreBounds=True)

        self.view_box = self.plot.getViewBox()
        self.vb_range = self.view_box.viewRange()

        # self.hideAxis('left')
        # self.hideAxis('bottom')
        # self.hideAxis('right')
        # self.hideAxis('top')

        self.vline.hide()
        self.hline.hide()
        self.labelx.hide()
        self.labely.hide()

        self.min_x = None
        self.max_x = None
        self.min_y = None
        self.max_y = None

        self.y_text_list = []
        self.ycircle_list = []

        self.plot.scene().sigMouseMoved.connect(self.mouse_moved)
        self.proxyMouseClicked = pg.SignalProxy(self.plot.scene().sigMouseClicked, slot=self.mouse_clicked)
        self.proxyRange = pg.SignalProxy(self.plot.sigRangeChanged, slot=self.range_changed)

    def update(self):

        curvce_id = 0
        for plot_data_item in self.plot.listDataItems():
            (self.x_data, y_data) = plot_data_item.getData()
            self.x_data = self.x_data.tolist()
            x_data_log = [10**val for val in self.x_data]
            y_data = y_data.tolist()
            color = plot_data_item.curve.opts['pen'].color().getRgb()
            
            self.data_list.append(
                {
                    'color':color,
                    'data': {round(self.x_data[cpt], 2): {'x': self.x_data[cpt],
                                                     'xlog': x_data_log[cpt],
                                                     'y': y_data[cpt]}
                             for cpt in range(len(x_data_log))},
                    'txt_pos': {'x': None, 'y': None}
                }
            )

            self.data_list_x_sorted.append(
                sorted(self.data_list[curvce_id]['data'].keys())
                )
            
            
            curvce_id += 1
        
        if len(self.data_list) > 0:
            list_x = [data['x'] for data in self.data_list[0]['data'].values()]
            list_y = [data['y'] for data in self.data_list[0]['data'].values()]
            try:
                self.min_x = min(list_x)
                self.max_x = max(list_x)
                self.min_y = min(list_y)
                self.max_y = max(list_y)
            except ValueError:
                self.min_x = None
                self.max_x = None
                self.min_y = None
                self.max_y = None
        
        else:
            self.min_x = None
            self.max_x = None
            self.min_y = None
            self.max_y = None
        
        for data in self.data_list:
            self.y_text_list.append(
                pg.TextItem(
                    border=pg.mkPen(
                        color=(data['color'][0],
                               data['color'][1],
                               data['color'][2])),
                    fill=pg.mkBrush(0, 0, 0, 210),
                    anchor=(-0.1, 0.5)
                    )
                )
            html_cross = '<span style="color: #%s; \
            font-size: 12px;"><mark><b>X</b>' \
            % pg.colorStr(pg.mkColor('#ffaa55'))[:-2]
            html_cross += '</mark></span>'

            self.ycircle_list.append(
                pg.TextItem(html=html_cross,
                             anchor=(0.45, 0.5)))
            

        for item in self.y_text_list:
            self.plot.addItem(item)
            item.hide()
        
        for item in self.ycircle_list:
            self.plot.addItem(item)
            item.hide()

    def mouse_moved(self, pos):
        if self.plot.sceneBoundingRect().contains(pos):
            mousePoint = self.view_box.mapSceneToView(pos)

            self.moved(mousePoint)
            self.vb_range = self.view_box.viewRange()

    def size_ROI(self, viewRange):
        diffx = viewRange[0][1] - viewRange[0][0]
        diffy = viewRange[1][1] - viewRange[1][0]
        sizex = 0.005 * diffx
        sizey = 0.05 * diffy
        return (sizex, sizey)
    
    def mouse_clicked(self, ev):
        if ev[0].button() == 1:
            x = self.vline.pos().x()
            x_log = 10 ** x
            x = round(x)
            if 0 <= x and x < len(self.x_data):
                y = self.hline.pos().y()
                (sizex, sizey) = self.size_ROI(self.vb_range)
                roi = pg.ROI((x,y), size=(sizex, sizey), removable=True)
                roi.addTranslateHandle((1,1))
                roi.setAcceptedMouseButtons(QtCore.Qt.LeftButton)
                text = pg.TextItem("x: " + "{:.2e}".format(x_log) + " y: %.2f" % y,
                                   color='w', anchor=(0, 2), fill="b")
                text.setParentItem(roi)
                roi.sigRemoveRequested.connect(self.remove_roi)
                roi.sigRegionChanged.connect(self.move_roi)
                roi.sigClicked.connect(self.clicked_roi)
                self.plot.addItem(roi)
    
    def range_changed(self, arg):
        vb = arg[0]
        if vb == self.vb_range:
            viewRange = arg[1]
            (sizex,sizey) = self.size_ROI(viewRange)
            for item in self.plot.items:
                if isinstance(item, pg.ROI):
                    item.setSize((sizex, sizey))
    
    def remove_roi(self, roi):
        self.plot.removeItem(roi)
    
    def move_roi(self, roi):
        for item in self.plot.items:
            if isinstance(item, pg.ROI):
                item.setZValue(0)
        roi.setZValue(1)
        x = roi.pos()[0]
        x_log = 10 ** x
        x = round(x)
        if x < 0:
            x = 0
        elif x >= len(self.x_data):
            x = self.vline.pos().x() - 1
        y = self.hline.pos().y()
        roi.setPos((x, y), update=False)
        for item in roi.childItems():
            if isinstance(item, pg.TextItem):
                item.setText("x: " + "{:.2e}".format(x_log) + " y: %.2f" % y, color='w')

    def clicked_roi(self, roi, ev):
        for item in self.plot.items:
            if isinstance(item, pg.ROI):
                item.setZValue(0)
        roi.setZValue(1)

    def moved(self, mousePoint):

        x_value = mousePoint.x()
        x_value_log = round((10**x_value))
        y_value = mousePoint.y()

        if x_value >= self.vb_range[0][0] and\
                x_value <= self.vb_range[0][1] and\
                y_value >= self.vb_range[1][0] and\
                y_value <= self.vb_range[1][1]:

            self.vline.show()
            self.hline.show()

            self.vline.setPos(x_value)
            self.hline.setPos(y_value)

            self.set_line_text(x_value, y_value, x_value_log)

            # if self.min_x is not None and self.max_x is not None:
            #     if x_value >= self.min_x and\
            #             x_value <= self.max_x:
            #         cpt = 0
            #         for data in self.data_list:
            #             try:
            #                 self.ycircle_list[cpt].show()

            #                 key = find_the_closest(
            #                     self.data_list_x_sorted[cpt],
            #                     round(x_value, 2)
            #                 )

            #                 posx = data['data'][key]['x']
            #                 posy = data['data'][key]['y']

            #                 pixel_point = self.view_box.mapViewToScene(
            #                     QtCore.QPointF(posx, posy)
            #                 )
            #                 self.ycircle_list[cpt].setPos(posx, posy)

            #                 self.set_cross_text(posx, posy, data['color'],
            #                                      cpt, pixel_point)
            #             except KeyError:
            #                 pass

            #             cpt += 1

                    # self.unoverlap()

                # else:
                #     for item in self.ycircle_list:
                #         item.hide()
                #     for item in self.y_text_list:
                #         item.hide()

        else:
            self.vline.hide()
            self.hline.hide()
            for item in self.ycircle_list:
                item.hide()
            
            self.labelx.hide()
            self.labely.hide()
            for item in self.y_text_list:
                item.hide()
    
    def set_line_text(self, x_value, y_value, x_value_log=None):

        textx = "{:.2e}".format(x_value_log)
        texty = '%.3f' % y_value
        
        html = '<span style="color: #%s; \
                 font-size: 12px;"><mark>' %\
            pg.colorStr(pg.mkColor('#ffaa55'))[:-2]
        self.labelx.setHtml('%s%s%s' % (html, textx, '</mark></span>'))
        self.labely.setHtml('%s%s%s' % (html, texty, '</mark></span>'))

        self.labelx.show()
        self.labely.show()

        self.labelx.setPos(x_value, self.vb_range[1][0])
        self.labely.setPos(self.vb_range[0][0], y_value)

    # def set_cross_text(self, posx, posy, color, cpt, pixel_point):

    #     html = '<span style="color: rgb(%s,%s,%s);\
    #              font-size: 12px;"><mark>' %\
    #         (color[0], color[1], color[2])

    #     text = 'x: %.3f<br>y: %.3f' % (posx, posy)
    #     self.y_text_list[cpt].show()
    #     self.y_text_list[cpt].setHtml(
    #         html + text + '</mark></span>'
    #     )

    #     self.data_list[cpt]['txt_pos']['x'] = pixel_point.x()
    #     self.data_list[cpt]['txt_pos']['y'] = pixel_point.y()

    def unoverlap(self):

        length = len(self.data_list)
        pos_dic = {
            self.data_list[i]['txt_pos']['y']: i for i in range(length)
        }
        pos_list = sorted(pos_dic.keys())

        try:
            for cpt in range(length - 1):
                id1 = pos_dic[pos_list[cpt]]
                id2 = pos_dic[pos_list[cpt + 1]]

                while pos_list[cpt] + 2 >= pos_list[cpt + 1]:
                    pos_list[cpt + 1] += 1

                self.data_list[id1]['txt_pos']['y'] = pos_list[cpt]
                self.data_list[id2]['txt_pos']['y'] = pos_list[cpt + 1]

                pos_dic = {
                    self.data_list[i]['txt_pos']['y']: i for i in range(length)
                }
        except IndexError:
            pass

        self.set_pos()

    def set_pos(self):

        for curve_id in range(len(self.data_list)):
            pos_x = self.data_list[curve_id]['txt_pos']['x']
            pos_y = self.data_list[curve_id]['txt_pos']['y']

            pts = self.view_box.mapSceneToView(QtCore.QPointF(pos_x, pos_y))
            self.y_text_list[curve_id].setPos(pts.x(), pts.y())
