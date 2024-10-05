# FIFO Dynamic Priority Queue

![License](https://img.shields.io/badge/license-MIT-brightgreen) <!-- Adjust according to your license -->

## Overview

`FIFO_Dynamic_Prio` is a class that implements a FIFO (First In, First Out) queue with dynamic prioritization. This allows objects to be queued and their prioritization adjusted dynamically, enabling preference for certain queued objects when necessary.

### Key Features

- **FIFO Queue**: Follows the standard FIFO principle for object handling.
- **Dynamic Prioritization**: Adjust the priority of queued objects at any time.
- **Universal Implementation**: Designed for use in various programming environments, particularly low-level programming scenarios._Hence the written code is not optimised for the python programming language._

## Installation

Clone the repository:
   ```bash
   git clone https://github.com/KClaudius/FIFO_Dynamic_Prio.git
   cd FIFO_Dynamic_Prio
   # pip install -r requirements.txt - no dependencies
   ```

## Usage
To use the FIFO_Dynamic_Prio class, you need to import it from the source module. Below is an example of how to create an instance of the class and use its methods.

```python
from src.your_module import FIFO_Dynamic_Prio

# Create an instance of FIFO_Dynamic_Prio
fifo_queue = FIFO_Dynamic_Prio(n=5)

# Enqueue objects
fifo_queue.enqueue_object("Task 1")
fifo_queue.enqueue_object("Task 2")

# Prioritize an object
fifo_queue.prioritise_object("Task 2", prio=1)

# Serve the next object
valid, next_serve = fifo_queue.next_serve()
if valid:
    print(f"Next to serve: {next_serve}")

# Dequeue an object
fifo_queue.dequeue_object("Task 1")
```


## Testing

To ensure the functionality of the `FIFO_Dynamic_Prio` class, a series of tests are provided in the `test_FIFO_Dynamic_Prio.py` file. You can run these tests using the built-in `unittest` framework in Python.

### Running Tests

1. Make sure you have Python installed on your system.
2. Open a terminal or command prompt.
3. Navigate to the repos directory containing the `tests` directory.
4. Run the tests using the following command:

   ```bash
   python -m unittest discover -s tests
   ```

## Contributing
Any recommendations? Let me know by creating a pull request!

## License
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT) - see the LICENSE file for details.