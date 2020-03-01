import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve

def random_color_hex():
    return "#" + ("%06x" % np.random.randint(0, 0xffffff))
    
def add_plot_model_predictions(fig, layout, xs, model, title, axis = None, heat_map = False):
  ys = model.predict(xs)

  res = fig.add_subplot(layout)
  res.title.set_text(title)
  
  if heat_map:
    xx, yy = np.meshgrid(
      np.arange(axis[0]-0.1, axis[1] + 0.1, 0.1), 
      np.arange(axis[2] - 0.1, axis[3] + 0.1, 0.1))
    Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = np.array(Z).reshape(xx.shape)
    res.contourf(xx, yy, Z, cmap=plt.cm.RdBu, alpha=.75)

  res.scatter(*xs.T, c = ys.ravel())

  if not axis is None:
    res.axis(axis)

  return res
  
def add_plot_data_2d(fig, layout, xs, ys, title, axis = None):
  res = fig.add_subplot(layout)
  res.title.set_text(title)
  
  scatter = res.scatter(*xs.T, c = ys.ravel())
  
  legend1 = res.legend(*scatter.legend_elements(), title="Classes")

  if not axis is None:
    res.axis(axis)

  return res
  
def add_plot_with_error_distrib(fig, layout, error):
  res = fig.add_subplot(layout)
  res.title.set_text("Error")
  x = np.arange(len(error))
  res.plot(x, error)
  return res
  
def add_plot_with_roc_curve(fig, layout, actual, predicted, title = 'Receiver Operating Characteristic (ROC) Curve'):
    fpr, tpr, thresholds = roc_curve(actual, predicted)
    res = fig.add_subplot(layout)
    res.title.set_text(title)
    res.plot(fpr, tpr, color='orange', label='ROC')
    res.plot([0, 1], [0, 1], color='darkblue', linestyle='--')
    res.set_xlabel('False Positive Rate')
    res.set_ylabel('True Positive Rate')
    res.legend()
    