from matplotlib.colors import Normalize
import randomDataGeter as rdg
from tensorflow import keras
import numpy
import matplotlib.pyplot as plt

testData_path = r"D:\Desktop\Prog\L3\BE\WorkBench\test_data_storage"
test_file = "2021-04-22_K222303001.csv"
neural_network = r"./network_storage"

# model is the neural network, base_seq a list of measurements and pred_len is the size of the output list


def predict(model_path, base_seq, pred_len):
    seq_len = len(base_seq)
    pred_seq = [base_seq[-1][0]]
    model = keras.models.load_model(model_path)

    for i in range(0, pred_len):
        pred = model.predict(numpy.array([base_seq[-1*seq_len:]]))
        base_seq.append([pred[0][0]])
        pred_seq.append(pred[0][0])

    return pred_seq


st = rdg.load_file(testData_path, test_file, 0)
st, minST, maxST = rdg.normalize_array(st)

context_size = 50
sub_seq_start = 50
prediction_len = 24
sub_seq_len = 24 + prediction_len

sub_seq = []
for i in range(0, sub_seq_len):
    sub_seq.append([st[sub_seq_start+i][0]])
pred = predict(neural_network, sub_seq[:24], 24)

x = numpy.arange(sub_seq_start-context_size,
                 sub_seq_start+sub_seq_len+context_size)
plt.plot(x, st[sub_seq_start-context_size: sub_seq_start +
         sub_seq_len+context_size], color='blue')

x = numpy.arange(sub_seq_start, sub_seq_start+24)
plt.plot(x, sub_seq[:24], color='green')

x = numpy.arange(sub_seq_start+sub_seq_len - prediction_len-1,
                 sub_seq_start+sub_seq_len)
plt.plot(x, pred, color='red')

plt.show()
