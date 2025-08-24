from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt6.QtCharts import QBarCategoryAxis,QBarSeries,QChart, QChartView, QLineSeries, QCategoryAxis, QValueAxis, QBarSet
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import QEasingCurve,Qt
import sys
import random

# class LineChart(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("LineChart")
#         self.resize(1280,720)
#         series = QLineSeries()
#         series.append(0,random.randint(100,50000))
#         series.append(1,random.randint(100,50000))
#         series.append(2,random.randint(100,50000))
#         series.append(3,random.randint(100,50000))
#         series.append(4,random.randint(100,50000))
#         series.append(5,random.randint(100,50000))
#         series.append(6,random.randint(100,50000))
#         series.append(7,random.randint(100,50000))
#         series.append(8,random.randint(100,50000))
#         series.append(9,random.randint(100,50000))
#         series.append(10,random.randint(100,50000))
#         series.append(11,random.randint(100,50000))
    
#         axisX = QCategoryAxis()
#         axisX.append("Jan", 0)
#         axisX.append("Feb", 1)
#         axisX.append("Mar", 2)
#         axisX.append("Apr", 3)
#         axisX.append("May", 4)
#         axisX.append("Jun", 5)
#         axisX.append("Jul", 6)
#         axisX.append("Aug", 7)
#         axisX.append("Sep", 8)
#         axisX.append("Oct", 9)
#         axisX.append("Nov", 10)
#         axisX.append("Dec", 11)
#         axisX.setRange(0, 11)

#         values = [point.y() for point in series.points()]
#         values = max(values) * 1.1
#         axisY = QValueAxis()
#         axisY.setRange(0,values)
#         axisY.setTitleText("USD")

#         chart = QChart()
#         chart.addSeries(series)
#         chart.addAxis(axisX,Qt.AlignmentFlag.AlignBottom)
#         chart.addAxis(axisY, Qt.AlignmentFlag.AlignLeft)
#         series.attachAxis(axisY)
#         series.attachAxis(axisX)
#         chart.setAnimationOptions(QChart.AnimationOption.AllAnimations)
#         chart.setAnimationDuration(2000)
#         chart.setAnimationEasingCurve(QEasingCurve.Type.OutSine)
#         chart.setTitle("Monthly Revenue")

#         view = QChartView(chart)
#         view.setRenderHint(QPainter.RenderHint.Antialiasing)
#         self.setCentralWidget(view)

# class BarChart(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("BarChart")
#         self.resize(1280,720)
#         set0 = QBarSet("Revenue")
#         for _ in range(12):
#             set0.append(random.randint(100,50000))

#         series = QBarSeries()
#         series.append(set0)

#         months = ["Jan","Feb","March","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

#         axisX = QBarCategoryAxis()
#         axisX.append(months)
#         max_value = max(set0) * 1.1
#         axisY = QValueAxis()
#         axisY.setRange(0,max_value)
#         axisY.setTitleText("USD")

#         chart = QChart()
#         chart.addSeries(series)
#         chart.addAxis(axisX, Qt.AlignmentFlag.AlignBottom)
#         chart.addAxis(axisY , Qt.AlignmentFlag.AlignLeft)
#         series.attachAxis(axisX)
#         series.attachAxis(axisY)

#         chart.setTitle("BarChart")
#         chart.

# app = QApplication(sys.argv)
# w = LineChart(); w.show(); sys.exit(app.exec())
from PyQt6.QtCharts import QPieSeries
from PyQt6.QtWidgets import QVBoxLayout
class PieChart(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Piechart")
        self.resize(1280,720)

        series = QPieSeries()
        series.append("Apple",252)
        series.append("Banana",500)
        series.append("Pear",1000)
        series.append("Cherry",100)

        # Cho lát "C" hiện label
        for slice in series.slices():
            slice.setLabel(f"{slice.label()} - {round(slice.percentage()*100)}%")
            slice.setLabelVisible(False)

        series.hovered.connect(self.on_hover)

        chart = QChart()
        chart.addSeries(series)
        chart.setAnimationOptions(QChart.AnimationOption.AllAnimations)

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.addWidget(chart_view)
        self.setCentralWidget(central_widget)

    def on_hover(self,slice,state):
        if state:
            slice.setExploded(True)
            slice.setExplodeDistanceFactor(0.10)
            slice.setLabelVisible(True)
        else:
            slice.setExploded(False)
            slice.setLabelVisible(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PieChart()
    window.show()
    sys.exit(app.exec())