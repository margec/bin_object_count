# Detect object count from bin image

In this project, we train a computer vision CNN model with images from the 'Amazon Bin Image Dataset', and deploy the model, so we can call the inference endpoint, to predict the number of objects given an input bin image.

Below is a list of AWS services used, when integrated we can create an end-to-end system:

* SageMaker for training the model, tuning hyperparameters, and deploying the trained model
* Lambda for invoking the deployed model inference endpoint
* API Gateway for provisioning a public endpoint for accessing the system via Lambda
* S3 for storing the training and testing images

## Project Set Up and Installation

This project is developed on AWS SageMaker Studio JupyterLab, other than having to create a lab space, there is no other special set up needed.

## Dataset

### Overview

Training images are a subset (10,441 images) from the ‘Amazon Bin Image Dataset’ on AWS Data Exchange, documented at https://registry.opendata.aws/amazon-bin-imagery, which has >500,000 JPEG images of bins with different object counts, and the respective JSON metadata files. 

For each JPEG image, there is a corresponding JSON metadata file that describes the contents of the bin, such as object name, and dimensions, although only the object count (‘EXPECTED_QUANTITY’) datapoint is used.

### Access

We use file_list.json and the code from the starter files, to download the subset of 10,441 images from the source dataset, and arrange them in a way that is ready for training, then we upload the files and clone the structure in S3, so SageMaker can access them during training.

```
aws s3 cp 'enhanced_bin_images' {s3_uri} --recursive
```

## Model Training

Our model is based on a pre-trained RESNET34 CNN, leveraging transfer learning, to give us a model that has pre-learned a lot of general features from ImageNet, and we only train the last FC layer with our relatively smaller subset of bin images.

We have asked SageMaker to tune 3 hyperparameters: 1. epochs (number of iterations), 2. batch size, and 3. learning rate. How many times we go back to update the weights is important, while batch size and learning rate are highly correlated and hence are tuned together.

Our model has only attained an accuracy of 0.33, in other words, it has failed to achieve our benchmark accuracy of 0.80, but it is not un-expected given the quality of the training images.

## Machine Learning Pipeline

* download 10,441 training images from 'Amazon Bin Image Dataset'
* split them into 3 sets: train, validate, test
* improve contrast
* upload the enhanced images to S3
* start a SageMaker hyperparameter tuning job
* query the best hyperparameters from the tuner
* start a SageMaker training job to train the model with the set of best hyperparameters
* deploy the model

For an end-to-end system, we add:

* create a Lambda Function to invoke inference endpoint
* create a public internet facing API at API Gateway and integrate this API with the above Lambda Function