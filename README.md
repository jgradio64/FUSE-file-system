# python-fuse-file-system

## Instructions

### Base Program

To run the base program

1. Make sure that you have created the mount and root directories.
2. Enter the following code.
    * `python passthrough.py root mp`
    * `mp` is the path to your mount folder, 
    * `root` is the path to your root folder.
3. Create or change the files in the mount folder.
4. To exit the program:
    * run `fusermount -u mp/` 
    * `mp` represents the path to your mountpoint folder 

### Testing

To run automated testing we have 2 options.

First you can run the following code which will run a suite of small built in tests.
* `python passthrough.test.py` 

Second, you can use the `run.py` script to open up a dialogue that presents a list of options.
* `python run.py`