from .Block import BuildingBlock
# import Block
from tensorflow.keras.layers import Layer
from tensorflow.keras import Sequential
from tensorflow.keras import Model
from tensorflow.keras.layers import Layer, Input, Add, Dense, Activation, ZeroPadding2D, BatchNormalization, Flatten, Conv2D, AveragePooling2D, MaxPooling2D, GlobalMaxPooling2D, GlobalAveragePooling2D
from tensorflow.keras.initializers import glorot_uniform

class ResLayer(Layer):
  def __init__(self, filter, num_block, use_BottleNeck = False):
    super(ResLayer, self).__init__()

    self.net = Sequential()

    for i in range(num_block):
      if (i == 0):
        self.net.add(BuildingBlock(filter, stride = 2, use_BottleNeck = use_BottleNeck, use_DownSample = True))
      else:
        self.net.add(BuildingBlock(filter, stride = 1, use_BottleNeck = use_BottleNeck, use_DownSample = False))

  def call(self,input_tensor, *args, **kwargs):
    return self.net(input_tensor, *args, **kwargs)

class ResNet(Model):
  def __init__(self, layers, classes, use_BottleNeck = False):
    super(ResNet, self).__init__()

    self.net = Sequential([
                           Conv2D(filters = 64, kernel_size= (7,7), strides = (2,2), padding = 'same'),
                           BatchNormalization(axis = 3),
                           Activation('relu'),
                           MaxPooling2D(pool_size = (3,3), strides = (2,2))
                          ])
    filters = [64, 128, 256, 512]
    for i in range(len(filters)):
        self.net.add(ResLayer(filter = filters[i], num_block = layers[i], use_BottleNeck = use_BottleNeck))

    self.net.add(AveragePooling2D(pool_size=(2, 2), name="avg_pool"))
    self.net.add(Flatten())
    self.net.add(Dense(classes, activation='softmax', kernel_initializer = glorot_uniform(seed=0)))

  def call(self, input_tensor, *args, **kwargs):
    X = self.net(input_tensor, *args, **kwargs)

    return X

class ResNet18(ResNet):
  def __init__(self, num_classes):
    super().__init__(layers=[2, 2, 2, 2],classes=num_classes, use_BottleNeck=False)
class ResNet34(ResNet):
  def __init__(self, num_classes):
    super().__init__(layers=[3, 4, 6, 3],classes=num_classes, use_BottleNeck=False)
class ResNet50(ResNet):
  def __init__(self, num_classes):
    super().__init__(layers=[3, 4, 6, 3],classes=num_classes, use_BottleNeck=True)
class ResNet101(ResNet):
  def __init__(self, num_classes):
    super().__init__(layers=[3, 4, 23, 3],classes=num_classes, use_BottleNeck=True)
class ResNet152(ResNet):
  def __init__(self, num_classes):
    super().__init__(layers=[3, 8, 36, 3],classes=num_classes, use_BottleNeck=True)
