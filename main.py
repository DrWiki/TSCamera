import cv2
import argparse
from collections import deque
from time import perf_counter

import numpy as np

import pyqtgraph as pg
import pyqtgraph.functions as fn
import pyqtgraph.parametertree as ptree
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets
data = []
default_pen = pg.mkPen()
class MonkeyCurveItem(pg.PlotCurveItem):
    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)
        self.monkey_mode = ''

    def setMethod(self, param, value):
        self.monkey_mode = value

    def paint(self, painter, opt, widget):
        if self.monkey_mode not in ['drawPolyline']:
            return super().paint(painter, opt, widget)

        painter.setRenderHint(painter.RenderHint.Antialiasing, self.opts['antialias'])
        painter.setPen(pg.mkPen(self.opts['pen']))

        if self.monkey_mode == 'drawPolyline':
            painter.drawPolyline(fn.arrayToQPolygonF(self.xData, self.yData))

app = pg.mkQApp("Plot Speed Test")
pw = pg.PlotWidget()
pw.setWindowTitle('pyqtgraph example: PlotSpeedTest')
pw.setLabel('bottom', 'Index', units='B')
curve = MonkeyCurveItem(pen=default_pen, brush='b')
pw.addItem(curve)
rollingAverageSize = 1000
elapsed = deque(maxlen=rollingAverageSize)
splitter = QtWidgets.QSplitter()
splitter.addWidget(pw)
splitter.show()
def update():
    options = ['antialias', 'connect', 'skipFiniteCheck']
    # kwds = { k : params[k] for k in options }
    kwds = "antialias"
    # if kwds['connect'] == 'array':
    #     kwds['connect'] = connect_array

    # Measure
    # t_start = perf_counter()
    curve.setData(np.array(data))
    app.processEvents(QtCore.QEventLoop.ProcessEventsFlag.AllEvents)
    t_end = perf_counter()
    # elapsed.append(t_end - t_start)
    # ptr = (ptr + 1) % data.shape[0]
    #
    # # update fps at most once every 0.2 secs
    # if t_end - fpsLastUpdate > 0.2:
    #     fpsLastUpdate = t_end
    #     average = np.mean(elapsed)
    #     fps = 1 / average
    #     pw.setTitle('%0.2f fps - %0.1f ms avg' % (fps, average * 1_000))

video = cv2.VideoCapture(1)
def update2():
        ret, frame = video.read()

        cv2.imshow("frame", frame)

        data.append(np.sum(np.sum(frame,axis=1),axis=0)[1]/(frame.shape[0]*frame.shape[1]))
        print(data)
        cv2.waitKey(1)

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(0)


timer2 = QtCore.QTimer()
timer2.timeout.connect(update2)
timer2.start(1)

if __name__ == '__main__':
    pg.exec()

