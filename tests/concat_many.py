import numpy as np
import torch
import torch.nn as nn
from torch.autograd import Variable
from pytorch2keras.converter import pytorch_to_keras


class TestConcatMany(nn.Module):
    """Module for Concatenation (2 or many layers) testing
    """

    def __init__(self, inp=10, out=16, kernel_size=3, bias=True):
        super(TestConcatMany, self).__init__()
        self.conv2_1 = nn.Conv2d(inp, out, kernel_size=kernel_size, bias=bias)
        self.conv2_2 = nn.Conv2d(inp, out, kernel_size=kernel_size, bias=bias)
        self.conv2_3 = nn.Conv2d(inp, out, kernel_size=kernel_size, bias=bias)

    def forward(self, x):
        x = torch.cat([
            self.conv2_1(x),
            self.conv2_2(x),
            self.conv2_3(x)
        ], dim=1)
        return x


if __name__ == '__main__':
    max_error = 0
    for i in range(100):
        kernel_size = np.random.randint(1, 7)
        inp = np.random.randint(kernel_size + 1, 100)
        out = np.random.randint(1, 100)

        model = TestConcatMany(inp, out, kernel_size, inp % 2)

        input_np = np.random.uniform(0, 1, (1, inp, inp, inp))
        input_var = Variable(torch.FloatTensor(input_np))
        output = model(input_var)

        k_model = pytorch_to_keras(model, input_var, (inp, inp, inp,), verbose=True)

        pytorch_output = output.data.numpy()
        keras_output = k_model.predict(input_np)

        error = np.max(pytorch_output - keras_output)
        print(error)
        if max_error < error:
            max_error = error

    print('Max error: {0}'.format(max_error))
