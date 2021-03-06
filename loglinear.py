import numpy as np
from math import sqrt


STUDENT = {'name': 'Ofir Bitron',
           'ID': '200042414'}


def softmax(x):
    """
    Compute the softmax vector.
    x: a n-dim vector (numpy array)
    returns: an n-dim vector (numpy array) of softmax values
    """
    x -= np.max(x)
    x = np.exp(x) / np.sum(np.exp(x))
    return x


def classifier_output(x, params):
    """
    Return the output layer (class probabilities) 
    of a log-linear classifier with given params on input x.
    """
    W, b = params
    return softmax(np.array(x).dot(W) + b)

def predict(x, params):
    """
    Returns the prediction (highest scoring class id) of a
    a log-linear classifier with given parameters on input x.
    """
    return np.argmax(classifier_output(x, params))


def loss_and_gradients(x, y, params):
    """
    Compute the loss and the gradients at point x with given parameters.
    y is a scalar indicating the correct label.

    returns:
        loss,[gW,gb]

    loss: scalar
    gW: matrix, gradients of W
    gb: vector, gradients of b
    """
    probs = classifier_output(x, params)
    W, b = params
    values = np.array(x).dot(W) + b
	
    gb = np.zeros(b.shape)
    it = np.nditer(gb, flags=["f_index"], op_flags=["readwrite"])
    exp_sum = np.sum(np.exp(values))
    spec_exp = []
    while not it.finished:
        i = it.index
        if len(spec_exp) <= i:
            spec_exp.append(np.exp(values[i]))
        gb[i] = spec_exp[i] / exp_sum
        if i == y:
            gb[i] -= 1
        it.iternext()

    gW = np.zeros(W.shape)
    it = np.nditer(gW, flags=["multi_index"], op_flags=["readwrite"])
    while not it.finished:
        dot = it.multi_index
        i = dot[0]
        j = dot[1]
        gW[dot] = (spec_exp[j] * x[i]) / exp_sum
        if j == y:
            gW[dot] -= x[i]
        it.iternext()
    loss = -np.log(probs[y])
    return loss, [gW, gb]


def create_classifier(in_dim, out_dim):
    """
    returns the parameters (W,b) for a log-linear classifier
    with input dimension in_dim and output dimension out_dim.
    """
    glW = sqrt(6) / (in_dim + out_dim)
    glB = sqrt(6) / (out_dim + 1)

    W = np.random.uniform(-glW, glW, (in_dim, out_dim))
    b = np.random.uniform(-glB, glB, (out_dim))
    return [W, b]


if __name__ == '__main__':
    # Sanity checks for softmax. If these fail, your softmax is definitely wrong.
    # If these pass, it may or may not be correct.
    test1 = softmax(np.array([1, 2]))
    print test1
    assert np.amax(np.fabs(test1 - np.array([0.26894142, 0.73105858]))) <= 1e-6
    test2 = softmax(np.array([1001, 1002]))
    print test2
    assert np.amax(np.fabs(test2 - np.array([0.26894142, 0.73105858]))) <= 1e-6

    test3 = softmax(np.array([-1001, -1002]))
    print test3
    assert np.amax(np.fabs(test3 - np.array([0.73105858, 0.26894142]))) <= 1e-6

    # Sanity checks. If these fail, your gradient calculation is definitely wrong.
    # If they pass, it is likely, but not certainly, correct.
    from grad_check import gradient_check

    W, b = create_classifier(3, 4)


    def _loss_and_W_grad(W):
        global b
        loss, grads = loss_and_gradients([1, 2, 3], 0, [W, b])
        return loss, grads[0]


    def _loss_and_b_grad(b):
        global W
        loss, grads = loss_and_gradients([1, 2, 3], 0, [W, b])
        return loss, grads[1]


    for _ in xrange(10):
        W = np.random.randn(W.shape[0], W.shape[1])
        b = np.random.randn(b.shape[0])
        gradient_check(_loss_and_b_grad, b)
        gradient_check(_loss_and_W_grad, W)
