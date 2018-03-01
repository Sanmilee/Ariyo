
import tensorflow as tf


from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)


#learning_rate = 0.0001
#epochs = 10
#batch_size = 50





# input - 28 x 28 pixels = 784 - the flattened image data
# reshape input to 4D to use TF conv and pooling functions: conv2d() n max_pool() 


x = tf.placeholder(tf.float32, [None, 784])

x_image = tf.reshape(x, [-1, 28, 28, 1])





#The format of the data to be supplied is [i, j, k, l] where i is the number of training samples, 
# j is the height of the image, k is the weight and l is the channel number
#tf.reshape() allows us to put -1 in place of i and it will dynamically reshape based on the number of training samples


y_ = tf.placeholder(tf.float32, [None, 10])





#Parameter Initialization

def weight_variable(shape): 
	initial = tf.truncated_normal(shape, stddev=0.1) 
	return tf.Variable(initial)


def bias_variable(shape): 
	initial = tf.constant(0.1, shape=shape) 
	return tf.Variable(initial)






#Convolution Initialization

def conv2d(x, W): 
	return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')


#The filter stride moves in steps of 1 in both the x and y directions
#The first and last values are always equal to 1, if they were not, 
#we would be moving the filter between training samples or between channels






#pooling Initialization


#pooling layer with 2 x 2 strides
def max_pool_2x2(x): 
	return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')


#The pooling function takes its first input as the tensor over which to perform the pooling. 
#The next two arguments are the pooling filter size and strides 
#The first and last values of filter and stride are set to 1











#First Convolutional Layer

#6 features for each 5x5 patch, the third dimension is number of input channels
#bias vector has a component for each output channel.


W_conv1 = weight_variable([5, 5, 1, 6]) 

b_conv1 = bias_variable([6])



h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
 
h_pool1 = max_pool_2x2(h_conv1)












#Second Convolutional Layer

#The second layer will have 16 features for each 5x5 patch.

W_conv2 = weight_variable([5, 5, 6, 16]) 

b_conv2 = bias_variable([16])



h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2) 

h_pool2 = max_pool_2x2(h_conv2)













#Densely Connected Layer

#Now that the image size has been reduced to 5x5


W_fc1 = weight_variable([5 * 5 * 16, 120]) 

b_fc1 = bias_variable([120]) 

h_pool2_flat = tf.reshape(h_pool2, [-1, 5*5*16]) 

h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)





#Dropout

#we apply dropout To reduce overfitting before the readout layer. 
#We create a placeholder for the probability that a neuron's output is kept during dropout. 
#This allows us to turn dropout on during training, and turn it off during testing.



keep_prob = tf.placeholder(tf.float32) 

h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)






#Softmax Layer

W_fc2 = weight_variable([120, 10]) 

b_fc2 = bias_variable([10]) 

y_conv=tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)








#Train and Evaluate the Model

#We include the keep_prob parameter in feed_dict to control the dropout rate.
#We will add logging to every 100th iteration in the training process.
#It does 20,000 training iterations and may take a while (possibly up to half an hour).




cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y_conv), reduction_indices=[1])) 

train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy) 

correct_prediction = tf.equal(tf.argmax(y_conv,1), tf.argmax(y_,1)) 

accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32)) 




sess = tf.InteractiveSession()
sess.run(tf.global_variables_initializer()) 

for i in range(20000): 
	batch = mnist.train.next_batch(50) 
	if i%100 == 0: 
		train_accuracy = accuracy.eval(feed_dict={ x:batch[0], y_: batch[1], keep_prob: 1.0}) 
		print("step %d, training accuracy %g"%(i, train_accuracy)) 

	train_step.run(feed_dict={x: batch[0], y_: batch[1], keep_prob: 0.5}) 




print("test accuracy %g"%accuracy.eval(feed_dict={ x: mnist.test.images, y_: mnist.test.labels, keep_prob: 1.0}))


#The final test set accuracy after running this code should be approximately 99.2%.


